import os
from flask import Flask
from flask import flash, redirect, render_template, request, url_for
from . import candidates_tsv_parser
from . import panelist_tsv_parser
from . import panel_generator
from . import panel_counter

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ["FLASK_SECRET_KEY"]

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/start')
    def start():
        return redirect(url_for('add_candidates_and_panelists'))

    @app.route('/add-candidates-and-panelists')
    def add_candidates_and_panelists():
        return render_template('add_candidates_and_panelists.html')

    @app.route('/results', methods=['POST'])
    def results():
        error = False
        raw_candidates = request.form['candidates']
        raw_panelists = request.form['panelists']
        if raw_candidates == '':
            error = True
            flash('Enter a list of candidates', 'candidates')
        if raw_panelists == '':
            error = True
            flash('Enter a list of panelists', 'panelists')

        if error:
            return redirect(url_for('add_candidates_and_panelists'))

        candidates = candidates_tsv_parser.parse(raw_candidates)
        if candidates is None:
            error = True
            flash('The candidates must be in the specified format', 'candidates')

        panelists = panelist_tsv_parser.parse(raw_panelists)
        if panelists is None:
            error = True
            flash('The panelists must be in the specified format', 'panelists')

        if error:
            return redirect(url_for('add_candidates_and_panelists'))

        panels = panel_generator.generate_panel(candidates, panelists)
        if panels is None:
            flash('Could not find a set of panels which met the constraints. Consider allowing some panelists to sit on more interview panels.', 'solver')
            return redirect(url_for('add_candidates_and_panelists'))

        panel_counts = panel_counter.count_panels(panels)

        return render_template(
            'results.html',
            panels=sorted(panels, key=lambda p: p.chair),
            panel_counts=panel_counts,
            raw_candidates=raw_candidates,
            raw_panelists=raw_panelists
        )

    return app

app = create_app()

