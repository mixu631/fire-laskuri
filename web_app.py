from flask import Flask, render_template, request, jsonify
from models.simulator import WealthSimulator
from models.targets import TargetChecker
from visualization.charts import ChartGenerator
import json
import os

app = Flask(__name__)
PRESETS_FILE = 'presets.json'

def load_presets():
    if os.path.exists(PRESETS_FILE):
        with open(PRESETS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_presets(data):
    with open(PRESETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

@app.route('/', methods=['GET', 'POST'])
def home():
    presets = load_presets()
    preset_names = sorted(presets.keys())

    if request.method == 'POST':
        form_data = request.form.to_dict()
        action = form_data.get("action")
        name = form_data.get("presetName")

        if action in ("save_preset", "update_preset") and name:
            print(">> Saving preset:", name)
            ignore_keys = {"action", "presetName"}
            filtered = {k: v for k, v in form_data.items() if k not in ignore_keys}
            presets[name] = filtered
            save_presets(presets)
            return '', 204

        years = int(request.form['years'])
        starting_capital = float(request.form['starting_capital'])
        starting_loan = float(request.form['starting_loan'])
        static_return = float(request.form['static_return'])
        static_investment = float(request.form['static_investment'])
        static_new_loan = float(request.form['static_new_loan'])
        gross_target = float(request.form['gross_target'])
        net_target = float(request.form['net_target'])
        gain_target = float(request.form['gain_target'])
        inflation_rate = float(request.form['inflation_rate'])

        loan_interest_rate = request.form.get('loan_interest_rate', '').strip()
        loan_interest_rate = float(loan_interest_rate) if loan_interest_rate else 0.0

        def parse_json_field(field_name):
            field_value = request.form.get(field_name, '').strip()
            return json.loads(field_value) if field_value else {}

        cash_injections = parse_json_field('cash_injections_json')
        debt_injections = parse_json_field('debt_injections_json')
        withdrawals = parse_json_field('withdrawals_json')
        debt_repayments = parse_json_field('debt_repayments_json')

        simulator = WealthSimulator(
            years=years,
            starting_capital=starting_capital,
            starting_loan=starting_loan,
            static_return=static_return,
            static_investment=static_investment,
            static_new_loan=static_new_loan,
            inflation_rate=inflation_rate,
            loan_interest_rate=loan_interest_rate,
            cash_injections=cash_injections,
            debt_injections=debt_injections,
            withdrawals=withdrawals,
            debt_repayments=debt_repayments
        )

        results = simulator.run()

        target_checker = TargetChecker(results)
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

        return render_template(
            'result.html',
            wealth_data=results,
            targets=targets_data,
            chart_file='wealth_chart.png'
        )

    return render_template('form.html', preset_names=preset_names)

@app.route("/load_preset/<name>")
def load_preset(name):
    presets = load_presets()
    return jsonify(presets.get(name, {}))

@app.route("/delete_preset/<name>", methods=["DELETE"])
def delete_preset(name):
    presets = load_presets()
    if name in presets:
        del presets[name]
        save_presets(presets)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
