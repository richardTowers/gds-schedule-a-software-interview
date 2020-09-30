import csv
from collections import namedtuple

Panelist = namedtuple('Panelist', [
    'name',
    'can_chair_panels',
    'is_male',
    'is_bame',
    'team',
    'has_a_software_engineering_background',
    'community',
    'max_panels',
    'min_panels',
])

def parse(text):

    HEADERS = [
        'Panelist',
        'Can chair panels?',
        'Is male?',
        'Is BAME?',
        'Team',
        'Has a software engineering background?',
        'Community',
        'Max Panels',
        'Min Panels',
    ]

    lines = text.split('\n')
    parsed = list(csv.reader(lines, dialect='excel-tab'))
    if parsed[0] != HEADERS:
        return None
    else:
        return [
            Panelist(
                 name = row[0],
                 can_chair_panels = (row[1] == 'TRUE'),
                 is_male = (row[2] == 'TRUE'),
                 is_bame = (row[3] == 'TRUE'),
                 team = row[4],
                 has_a_software_engineering_background = (row[5] == 'TRUE'),
                 community = row[6],
                 max_panels = int(row[7]),
                 min_panels = int(row[8]),
            )
            for row in parsed[1:]
        ]

