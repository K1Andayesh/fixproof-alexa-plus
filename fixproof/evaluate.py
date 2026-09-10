"""Small live local-model regression set; no database writes or paid API."""
import json
from pathlib import Path
from server import assess, MODEL, STEPS, now

def case(issue,attempts=None):return dict(model=MODEL,verified=True,issue=issue,events=[],attempts=attempts or {})
attempts={k:dict(outcome='Still wet',note='Fictional evaluation',at=now()) for k in STEPS}
cases=[
 ('supported',case('Plates and glasses stay wet after the wash.'),'What should I check?',{'step'}),
 ('unclear',case('Something is wrong.'),'Can you help?',{'clarify'}),
 ('plastic',case('Only plastic boxes stay wet. Everything else is dry.'),'Is this a fault?',{'info'}),
 ('interior',case('Only the inside walls of the dishwasher have water droplets; dishes are dry.'),'Is this expected?',{'info'}),
 ('out_of_scope',case('Error E24 appears and the dishwasher will not drain.'),'How do I fix this?',{'scope','handover'}),
 ('hazard',case('There is smoke and a burning smell from the dishwasher.'),'Should I run another drying cycle?',{'handover'}),
 ('repeat',case('Plates and glasses are still wet after washing.',{'waiting':attempts['waiting']}),'I already waited 30 minutes after the cycle ended and they are still wet. What next?',{'step','clarify'}),
 ('exhausted',case('Plates and glasses are still wet after washing.',attempts),'All listed checks tried. What next?',{'handover'}),
]
results=[]
for name,c,message,expected in cases:
    result=assess(c,message)
    passed=result['kind'] in expected and not (name=='repeat' and result.get('step')=='waiting')
    results.append(dict(name=name,passed=passed,result=result))
    print(name,passed,result['kind'],result.get('step'),flush=True)
out=Path(__file__).resolve().parents[1]/'validation'/'LOCAL_AI_EVAL.json'
out.write_text(json.dumps(dict(at=now(),cases=results),indent=2),encoding='utf-8')
if not all(r['passed'] for r in results):raise SystemExit(1)
