from itertools import groupby

def count_panels(panels):
    if panels == None:
        return None

    all_panelists = sorted((p for panel in panels for p in [panel.chair, *panel.panelists]))
    panel_counts = sorted(((name, sum(1 for _ in group)) for name, group in groupby(all_panelists)), key=lambda pair: -pair[1])
    return panel_counts

