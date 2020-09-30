import csv
from collections import namedtuple

Candidate = namedtuple('Candidate', [
    'name',
    'team',
])

def parse(text):

    HEADERS = [
        'Candidate',
        'Team',
    ]

    lines = text.split('\n')
    parsed = list(csv.reader(lines, dialect='excel-tab'))
    if parsed[0] != HEADERS:
        return None
    else:
        return [Candidate(name = row[0], team = row[1]) for row in parsed[1:]]

