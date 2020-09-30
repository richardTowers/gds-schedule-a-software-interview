from ortools.sat.python import cp_model
from collections import namedtuple

class Panel:
    pass

def generate_panel(candidates, panelists):
    model = cp_model.CpModel()
    variables = {}
    for candidate in candidates:
        for panelist in panelists:
            variables[candidate, panelist] = model.NewBoolVar(
                "%s_is_on_the_panel_for_%s" % (panelist.name, candidate.name)
            )

    for candidate in candidates:

        # There should be exactly three panelists for every interview
        model.Add(
            sum(
                variables[candidate, panelist] for panelist in panelists
            )
            == 3
        )

        # Panels must have exactly one person who can chair the panel
        # NOTE - we could loosen this so more than one chair can be on the same panel if we wanted
        model.Add(
            sum(
                variables[candidate, panelist] for panelist in panelists
                if panelist.can_chair_panels
            )
            == 1
        )

        # Panels must have at least two people with a software engineering background
        model.Add(
            sum(
                variables[candidate, panelist] for panelist in panelists
                if panelist.has_a_software_engineering_background
            )
            >= 2
        )

        # Panels must have at least one person who does not identify as male
        model.Add(
            sum(
                variables[candidate, panelist] for panelist in panelists
                if not panelist.is_male
            )
            >= 1
        )

        # Panels must have at least one person who identifies as BAME
        model.Add(
            sum(
                variables[candidate, panelist] for panelist in panelists
                if panelist.is_bame
            )
            >= 1
        )

        # Panels must have at least one person who is not from the same team as the candidate
        model.Add(
            sum(
                variables[candidate, panelist] for panelist in panelists
                if panelist.team != candidate.team
            )
            >= 1
        )

    for panelist in panelists:
        # All panelist must be on at least their minimum specified panels:
        model.Add(
            sum(
                variables[candidate, panelist] for candidate in candidates
            )
            >= panelist.min_panels
        )
        # All panelist must be on at most their maximum specified panels:
        model.Add(
            sum(
                variables[candidate, panelist] for candidate in candidates
            )
            <= panelist.max_panels
        )

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
        panels = []
        for candidate in candidates:
            panel = Panel()
            panel.candidate = candidate.name
            panel.panelists = []
            for panelist in panelists:
                if solver.BooleanValue(variables[candidate, panelist]):
                    if panelist.can_chair_panels:
                        panel.chair = panelist.name
                    else:
                        panel.panelists.append(panelist.name)
            panels.append(panel)
        return panels
    else:
        print("No solution possible - consider relaxing some constraints")
        return None

