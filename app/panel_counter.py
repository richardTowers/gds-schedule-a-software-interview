from itertools import groupby

def count_panels(panels):
    if panels == None:
        return None

    all_panelists = sorted(
        (
            p for panel in panels
            for p in [panel.chair, *panel.panelists]
        ), key=lambda p: p.name
    )
    panel_counts = sorted(
        (
            (panelist.name, panelist.team, sum(1 for _ in group))
            for panelist, group in groupby(all_panelists)
        ), key=lambda triplet: -triplet[2]
    )
    return panel_counts

