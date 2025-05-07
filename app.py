from models.simulator import WealthSimulator
from models.targets import TargetChecker
from visualization.charts import ChartGenerator
from reports.report_generator import ReportGenerator

# --- Preset Scenarios ---
presets = {
    '1': {
        'name': 'Balanced Plan',
        'years': 30,
        'starting_capital': 100000,
        'starting_loan': 50000,
        'static_return': 0.05,
        'static_investment': 10000,
        'static_new_loan': 0,
        'gross_target': 500000,
        'net_target': 400000,
        'gain_target': 50000
    },
    # You can add more presets here easily later
}

# --- Menu System ---
print("\nWelcome to the Wealth Forecast App\n")
print("Choose an option:")
print("1. Use preset scenario")
print("2. Enter custom data")

choice = input("\nEnter 1 or 2: ")

if choice == '1':
    print("\nAvailable presets:")
    for key, preset in presets.items():
        print(f"{key}. {preset['name']}")

    preset_choice = input("\nEnter the number of the preset to use: ")
    selected = presets.get(preset_choice)

    if not selected:
        print("Invalid preset. Exiting.")
        exit()

    print(f"\nYou selected: {selected['name']}")

    years = selected['years']
    starting_capital = selected['starting_capital']
    starting_loan = selected['starting_loan']
    static_return = selected['static_return']
    static_investment = selected['static_investment']
    static_new_loan = selected['static_new_loan']
    gross_target = selected['gross_target']
    net_target = selected['net_target']
    gain_target = selected['gain_target']

else:
    # --- Get user input ---
    years = int(input("Enter the number of years to simulate (e.g., 30): "))
    starting_capital = float(input("Enter your starting capital (€): "))
    starting_loan = float(input("Enter your starting loan (€): "))
    static_return = float(input("Enter your expected annual return rate (%) (e.g., 5 for 5%): ")) / 100
    static_investment = float(input("Enter your static investment per year (€): "))
    static_new_loan = float(input("Enter your static new loan per year (€): "))

    gross_target = float(input("Enter your gross wealth target (€): "))
    net_target = float(input("Enter your net wealth target (€): "))
    gain_target = float(input("Enter your annual gain target (€): "))


# --- Simulate ---
sim = WealthSimulator(
    years=years,
    starting_capital=starting_capital,
    starting_loan=starting_loan,
    static_return=static_return,
    static_investment=static_investment,
    static_new_loan=static_new_loan,
)


results = sim.run_simulation()

# Print simulation results
for row in results:
    print(row)

# --- Check Targets ---
target_checker = TargetChecker(results)

# Example targets
gross_target = 500000
net_target = 400000
gain_target = 50000

gross_year = target_checker.find_wealth_target(gross_target, net=False)
net_year = target_checker.find_wealth_target(net_target, net=True)
gain_year = target_checker.find_annual_gain_target(gain_target, inflation_adjusted=False)

print(f"\n🎯 Gross Wealth Target ({gross_target}) reached in Year: {gross_year}")
print(f"🎯 Net Wealth Target ({net_target}) reached in Year: {net_year}")
print(f"🎯 Annual Gain Target ({gain_target}) reached in Year: {gain_year}")



# --- Create targets_data dict ---
targets_data = {
    'gross_target': gross_target,
    'gross_year': gross_year,
    'net_target': net_target,
    'net_year': net_year,
    'gain_target': gain_target,
    'gain_year': gain_year
}
# --- Create Chart ---
chart = ChartGenerator(results, targets_data)
chart.plot_wealth()




# --- Generate Report (HTML only) ---
report = ReportGenerator(results, targets_data)
report.generate_html()

