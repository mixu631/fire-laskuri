import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os

class ChartGenerator:
    def __init__(self, results, targets=None):
        self.results = results
        self.targets = targets or {}

    def plot_wealth(self, output_path='static/wealth_chart.png'):
        years = [row['year'] for row in self.results]
        gross = [row['gross'] for row in self.results]
        loan = [row['loan'] for row in self.results]
        net = [row['net'] for row in self.results]

        plt.style.use('seaborn-v0_8-muted')
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(years, gross, label='Gross (€)', linewidth=2.2, color='#3b6fb6')
        ax.plot(years, net, label='Net (€)', linewidth=2.2, color='#1a9988')
        ax.plot(years, loan, label='Loan (€)', linewidth=2.2, color='#c94c4c')

        # Optional target lines
        if 'gross_target' in self.targets:
            ax.axhline(y=self.targets['gross_target'], color='#669966', linestyle='--', linewidth=1.2, label='Gross Target')
        if 'net_target' in self.targets:
            ax.axhline(y=self.targets['net_target'], color='#999966', linestyle='--', linewidth=1.2, label='Net Target')

        ax.set_title("Wealth Development (Inflation-Adjusted)", fontsize=14, fontweight='bold', loc='left')
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("€ (Today's Value)", fontsize=12)
        ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('€{x:,.0f}'))
        ax.grid(True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.6)
        ax.grid(False, which='major', axis='x')
        ax.legend(loc='upper left', frameon=False, fontsize=10)
        ax.tick_params(axis='both', labelsize=10)

        plt.tight_layout()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=100)
        plt.close()


