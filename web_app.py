
from flask import Flask, render_template, request, jsonify
from models.simulator import WealthSimulator
from models.targets import TargetChecker
from visualization.charts import ChartGenerator
import json
import os

app = Flask(__name__)

PRESETS_FILE = os.path.join("static", "presets.json")

@app.route('/', methods=['GET', 'POST'])
def home():
    preset_names = []
    if os.path.exists(PRESETS_FILE):
        with open(PRESETS_FILE, 'r', encoding='utf-8') as f:
            presets = json.load(f)
            preset_names = list(presets.keys())

    if request.method == 'POST':
        form = request.form

        def parse_float(key, default=0.0):
            return float(form.get(key, default) or default)

        simulator = WealthSimulator(
            years=int(form['years']),
            starting_capital=parse_float('starting_capital'),
            starting_loan=parse_float('starting_loan'),
            static_return=parse_float('static_return'),
            static_investment=parse_float('static_investment'),
            static_new_loan=parse_float('static_new_loan'),
            inflation_rate=parse_float('inflation_rate'),
            loan_interest_rate=parse_float('loan_interest_rate'),
            investment_growth_type=form.get('investment_growth_type', 'none'),
            investment_growth_value=parse_float('investment_growth_value'),
            loan_growth_type=form.get('loan_growth_type', 'none'),
            loan_growth_value=parse_float('loan_growth_value'),
            cash_injections=json.loads(form.get('cash_injections_json') or '{}'),
            debt_injections=json.loads(form.get('debt_injections_json') or '{}'),
            withdrawals=json.loads(form.get('withdrawals_json') or '{}'),
            debt_repayments=json.loads(form.get('debt_repayments_json') or '{}')
        )

        results = simulator.run()

        target_checker = TargetChecker(results)
        gross_target = parse_float('gross_target')
        net_target = parse_float('net_target')
        gain_target = parse_float('gain_target')

        gross_year = target_checker.find_wealth_target(gross_target, net=False)
        net_year = target_checker.find_wealth_target(net_target, net=True)
        gain_year = target_checker.find_annual_gain_target(gain_target)

        chart = ChartGenerator(results, {
            'gross_target': gross_target,
            'net_target': net_target
        })
        chart.plot_wealth()

        targets_data = {
            'gross_target': gross_target,
            'net_target': net_target,
            'gain_target': gain_target,
            'gross_year': gross_year if gross_year else "Not reached",
            'net_year': net_year if net_year else "Not reached",
            'gain_year': gain_year if gain_year else "Not reached"
        }

        return render_template('result.html',
                               wealth_data=results,
                               targets=targets_data,
                               chart_file='wealth_chart.png')

    return render_template('form.html', preset_names=preset_names)

@app.route('/save_presets', methods=['POST'])
def save_presets():
    data = request.get_json()
    with open(PRESETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
