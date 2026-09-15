"""Original concise summaries, not redistributed manufacturer manuals."""
import re

MODEL = 'Bosch SMS6HAI02A/01'
SOURCE = {
    'title': 'Bosch SMS6HAI02A · Australian English user manual',
    'url': 'https://media3.bsh-group.com/Documents/9001676154_A.pdf',
    'service_url': 'https://www.bosch-home.com.au/en/productservice/SMS6HAI02A-01',
    'document': '9001676154 (010805) 650 V1',
    'verified': '2026-09-15',
    'sha256': 'af965b35d3447c81adfc56bf652f75f8da565d47a9d4dc9c1e55030ae521a47c',
    'coverage': 'Exact /01 service page links to this manual; cover names SMS6HAI02A.'
}
STEP_DEFINITIONS = {
    'programme': {'workflow': 'drying', 'title': 'Check the programme', 'text': 'Check whether the selected programme includes drying. Shortening options can reduce drying performance.', 'pages': [40]},
    'rinse_aid': {'workflow': 'drying', 'title': 'Check rinse aid', 'text': 'Check the rinse aid indicator and dosage. Use the cited pages for filling or adjusting it; use only domestic dishwasher rinse aid.', 'pages': [40, 23]},
    'loading': {'workflow': 'drying', 'title': 'Check pooled water', 'text': 'Where possible, angle items so water can drain from their recesses.', 'pages': [41]},
    'waiting': {'workflow': 'drying', 'title': 'Allow drying to finish', 'text': 'Let the programme finish, then wait 30 minutes before removing the tableware.', 'pages': [41]},
    'food_spacing': {'workflow': 'food', 'title': 'Check spacing and contact', 'text': 'Arrange tableware with enough space for spray jets to reach the surfaces, and avoid points of contact.', 'pages': [42]},
    'food_spray_arm': {'workflow': 'food', 'title': 'Check spray-arm movement', 'text': 'Arrange tableware so it does not block the spray arms from rotating.', 'pages': [42]},
    'food_filters': {'workflow': 'food', 'title': 'Check the filters', 'text': 'Check the filters for residue and clean them under running water as described in the manual.', 'pages': [42, 36, 37]},
    'food_programme': {'workflow': 'food', 'title': 'Check wash intensity', 'text': 'Select a more intensive washing programme for stubborn food remnants.', 'pages': [42]},
    'detergent_tray': {'workflow': 'detergent', 'title': 'Clear the tablet collecting tray', 'text': 'Arrange the top basket so tableware does not obstruct the tablet collecting tray, and keep tableware and fragrance dispensers out of the tray.', 'pages': [42]},
    'detergent_position': {'workflow': 'detergent', 'title': 'Reposition the detergent tablet', 'text': 'Position the detergent tablet transversely in the dispenser rather than vertically.', 'pages': [42]},
    'streaks_rinse_setting': {'workflow': 'streaks', 'title': 'Lower the rinse aid setting', 'text': 'If the rinse aid dosage is set too high, set the rinse aid system to a lower setting.', 'pages': [44]},
    'streaks_add_rinse_aid': {'workflow': 'streaks', 'title': 'Check for rinse aid', 'text': 'If no rinse aid has been added, fill the rinse aid dispenser as described in the manual.', 'pages': [44, 23]},
    'streaks_tray': {'workflow': 'streaks', 'title': 'Clear the tablet collecting tray', 'text': 'Arrange the top basket so tableware does not block the detergent dispenser lid, and keep tableware and fragrance dispensers out of the tablet collecting tray.', 'pages': [44, 27]},
    'streaks_prerinse': {'workflow': 'streaks', 'title': 'Avoid intensive pre-rinsing', 'text': 'Remove only large food remnants before loading; do not pre-rinse the tableware.', 'pages': [45]},
    'noise_spray_arm': {'workflow': 'noise', 'title': 'Check spray-arm clearance', 'text': 'Arrange tableware so the spray arms do not strike it during the wash.', 'pages': [48]},
    'noise_load_distribution': {'workflow': 'noise', 'title': 'Distribute a small load', 'text': 'If a small load lets water jets strike the tub directly, distribute the tableware evenly or add more tableware for the next wash.', 'pages': [48]},
    'noise_light_items': {'workflow': 'noise', 'title': 'Secure light items', 'text': 'Position light items of tableware securely so they do not move about during the wash cycle.', 'pages': [48]},
    'rust_resistant_tableware': {'workflow': 'rust', 'title': 'Use rust-resistant tableware', 'text': 'Use rust-resistant tableware when rust spots appear on cutlery.', 'pages': [45]},
    'rust_remove_rusting_items': {'workflow': 'rust', 'title': 'Keep rusting items out', 'text': 'Do not wash rusting items together with the cutlery.', 'pages': [45]},
    'clouding_dishwasher_proof': {'workflow': 'clouding', 'title': 'Use dishwasher-proof glasses', 'text': 'Use glasses that are dishwasher-proof; long-term wear can otherwise be expected.', 'pages': [45]},
    'clouding_steam_phase': {'workflow': 'clouding', 'title': 'Avoid a lengthy steam phase', 'text': 'Avoid leaving glassware standing in the appliance for a long time after the wash cycle ends.', 'pages': [45]},
    'clouding_lower_temperature': {'workflow': 'clouding', 'title': 'Use a lower-temperature programme', 'text': 'Use a programme with a lower washing temperature.', 'pages': [45]},
    'clouding_glass_protection': {'workflow': 'clouding', 'title': 'Use glass-protection detergent', 'text': 'Use detergent with a glass protection component.', 'pages': [45]},
    'odour_wipe_interior': {'workflow': 'odour', 'title': 'Remove coarse interior soiling', 'text': 'Remove coarse soiling from the appliance interior with a damp cloth.', 'pages': [36]},
    'odour_clean_filters': {'workflow': 'odour', 'title': 'Clean the filters', 'text': 'Check the filters for residue and clean them under running water as described in the manual.', 'pages': [36]},
    'odour_machine_care': {'workflow': 'odour', 'title': 'Run Machine Care', 'text': 'Run Machine Care without tableware. Use only products designed for dishwashers and follow the product packaging safety instructions.', 'pages': [35, 36]},
}
INFO_DEFINITIONS = {
    'plastic': {'title': 'Plastic dries differently', 'text': 'Plastic retains less heat and can remain wet. The manual describes this as normal.', 'pages': [41]},
    'interior': {'title': 'Drops inside the tub', 'text': 'Moisture on the inner walls is part of condensation drying; the manual says no action is required for this condition.', 'pages': [41]},
}

CATALOGS = {
    'SMS6HAI02A/01': {
        'model': MODEL,
        'aliases': ('BOSCHSMS6HAI02A/01', 'SMS6HAI02A/01'),
        'source': SOURCE,
        'step_pages': {key: value['pages'] for key, value in STEP_DEFINITIONS.items()},
        'info_pages': {key: value['pages'] for key, value in INFO_DEFINITIONS.items()},
    },
    'SMS6HCI01A/38': {
        'model': 'Bosch SMS6HCI01A/38',
        'aliases': ('BOSCHSMS6HCI01A/38', 'SMS6HCI01A/38'),
        'source': {
            'title': 'Bosch SMS6HCI01A · Australian English user manual',
            'url': 'https://media3.bsh-group.com/Documents/9001720311_B.pdf',
            'service_url': 'https://www.bosch-home.com.au/en/productservice/SMS6HCI01A-38',
            'document': '9001720311 (050605) 650 A1',
            'verified': '2026-09-15',
            'sha256': 'b2bb4608cd266752804e8c02b3e251bb31e6c32f95824e602614b13f83240fc9',
            'coverage': 'Exact /38 service page links to this manual; cover names SMS6HCI01A.',
        },
        'step_pages': {
            'programme': [44], 'rinse_aid': [44, 24, 25], 'loading': [44], 'waiting': [44],
            'food_spacing': [45], 'food_spray_arm': [45, 39], 'food_filters': [45, 38, 39],
            'food_programme': [45], 'detergent_tray': [46, 28], 'detergent_position': [46],
            'streaks_rinse_setting': [48, 25], 'streaks_add_rinse_aid': [48, 24],
            'streaks_tray': [48, 28], 'streaks_prerinse': [48],
            'noise_spray_arm': [52], 'noise_load_distribution': [52], 'noise_light_items': [52],
            'rust_resistant_tableware': [49], 'rust_remove_rusting_items': [49],
            'clouding_dishwasher_proof': [49], 'clouding_steam_phase': [49],
            'clouding_lower_temperature': [49], 'clouding_glass_protection': [49],
            'odour_wipe_interior': [38], 'odour_clean_filters': [38], 'odour_machine_care': [37, 38],
        },
        'info_pages': {'plastic': [44], 'interior': [45]},
    },
    'SMS6HCI02A/72': {
        'model': 'Bosch SMS6HCI02A/72',
        'aliases': ('BOSCHSMS6HCI02A/72', 'SMS6HCI02A/72'),
        'source': {
            'title': 'Bosch SMS6HCI02A · Australian English user manual',
            'url': 'https://media3.bsh-group.com/Documents/9002017246_A.pdf',
            'service_url': 'https://www.bosch-home.com.au/en/productservice/SMS6HCI02A-72',
            'document': '9002017246 (050605) 650 V1',
            'verified': '2026-09-15',
            'sha256': 'b499156281a114882fd254e11400bc6318db71020eab2c4cfac9848264b4b476',
            'coverage': 'Exact /72 service page links to this manual; cover names SMS6HCI02A.',
        },
        'step_pages': {
            'programme': [41], 'rinse_aid': [41, 23, 24], 'loading': [41, 28], 'waiting': [42],
            'food_spacing': [42], 'food_spray_arm': [42, 37], 'food_filters': [43, 36, 37],
            'food_programme': [43], 'detergent_tray': [43, 27, 28], 'detergent_position': [43],
            'streaks_rinse_setting': [45, 24], 'streaks_add_rinse_aid': [45, 23],
            'streaks_tray': [45, 27, 28], 'streaks_prerinse': [46],
            'noise_spray_arm': [49], 'noise_load_distribution': [49], 'noise_light_items': [50],
            'rust_resistant_tableware': [46], 'rust_remove_rusting_items': [46],
            'clouding_dishwasher_proof': [46], 'clouding_steam_phase': [46],
            'clouding_lower_temperature': [46], 'clouding_glass_protection': [46],
            'odour_wipe_interior': [36], 'odour_clean_filters': [36], 'odour_machine_care': [35, 36],
        },
        'info_pages': {'plastic': [42], 'interior': [42]},
    },
}


def catalog_for(model):
    normalised = re.sub(r'\s+', '', model or '').upper()
    return next((entry for entry in CATALOGS.values() if normalised in entry['aliases']), None)


def source_for(model):
    entry = catalog_for(model)
    return entry['source'] if entry else SOURCE


def steps_for(model):
    entry = catalog_for(model)
    pages = entry['step_pages'] if entry else CATALOGS['SMS6HAI02A/01']['step_pages']
    return {key: {**value, 'pages': list(pages[key])} for key, value in STEP_DEFINITIONS.items()}


def info_for(model):
    entry = catalog_for(model)
    pages = entry['info_pages'] if entry else CATALOGS['SMS6HAI02A/01']['info_pages']
    return {key: {**value, 'pages': list(pages[key])} for key, value in INFO_DEFINITIONS.items()}


STEPS = steps_for(MODEL)
INFO = info_for(MODEL)
