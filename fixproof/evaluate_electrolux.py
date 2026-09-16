"""Exercise the new exact-model paths against the live local classifier/selector."""
import json
import urllib.request
from pathlib import Path

from catalog import steps_for
from server import assess, now

MODEL = 'Electrolux ESF8735ROX'
CASES = (
    ('detergent', 'Detergent remains in the dispenser after a wash.', {'electrolux_dispenser_lid', 'electrolux_dispenser_spray'}),
    ('streaks', 'Removable white streaks remain on glasses after a wash.', {'streaks_rinse_setting', 'electrolux_detergent_dose'}),
    ('odour', 'There is an unpleasant odour inside the dishwasher.', {'electrolux_clean_interior', 'electrolux_long_programme', 'electrolux_cleaner'}),
    ('starting', 'The dishwasher will not start because the door will not close securely.', {'starting_close_door', 'starting_basket_clearance'}),
    ('noise', 'There is a rattling noise during the wash.', {'electrolux_noise_loading', 'electrolux_noise_spray_arm'}),
    ('rust', 'Rust spots appear on the cutlery after a wash.', {'electrolux_separate_cutlery'}),
    ('unmapped_clouding', 'Clouding on the glassware does not wipe off after the wash.', set()),
)


def model_digest():
    with urllib.request.urlopen('http://127.0.0.1:11434/api/tags', timeout=5) as response:
        models = json.load(response)['models']
    return next(item['digest'] for item in models if item['name'] == 'qwen3.5:4b')


def main():
    steps = steps_for(MODEL)
    results = []
    for name, issue, allowed in CASES:
        case = {'model': MODEL, 'verified': True, 'issue': issue, 'events': [], 'attempts': {}}
        response = assess(case, 'What should I check first?')
        step = response.get('step')
        expected_pages = steps[step]['pages'] if step in allowed else None
        passed = (
            (step in allowed and response['kind'] == 'step' and response.get('pages') == expected_pages)
            if allowed else (response['kind'] == 'scope' and step in (None, 'none'))
        )
        results.append({'scenario': name, 'issue': issue, 'passed': passed, 'response': response})
        print(name, 'PASS' if passed else 'FAIL', response['kind'], step, response.get('pages'), flush=True)
    path = Path(__file__).resolve().parents[1] / 'validation' / 'ELECTROLUX_LOCAL_AI_EVAL.json'
    path.write_text(json.dumps({'captured_at': now(), 'model': 'qwen3.5:4b', 'model_digest': model_digest(), 'cases': results}, indent=2), encoding='utf-8')
    if not all(result['passed'] for result in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
