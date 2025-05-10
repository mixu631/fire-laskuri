from typing import Dict, List

class WealthSimulator:
    def __init__(
        self,
        years: int,
        starting_capital: float,
        starting_loan: float,
        static_return: float,
        static_investment: float,
        static_new_loan: float,
        inflation_rate: float,
        loan_interest_rate: float = 0.0,
        cash_injections: Dict[int, float] = None,
        debt_injections: Dict[int, float] = None,
        withdrawals: Dict[int, float] = None,
        debt_repayments: Dict[int, float] = None,
        investment_growth_type: str = "none",
        investment_growth_value: float = 0.0,
        loan_growth_type: str = "none",
        loan_growth_value: float = 0.0,
    ):
        self.years = years
        self.starting_capital = starting_capital
        self.starting_loan = starting_loan
        self.static_return = static_return / 100
        self.static_investment = static_investment
        self.static_new_loan = static_new_loan
        self.inflation_rate = inflation_rate / 100
        self.loan_interest_rate = loan_interest_rate / 100

        self.cash_injections = cash_injections or {}
        self.debt_injections = debt_injections or {}
        self.withdrawals = withdrawals or {}
        self.debt_repayments = debt_repayments or {}

        self.investment_growth_type = investment_growth_type
        self.investment_growth_value = investment_growth_value
        self.loan_growth_type = loan_growth_type
        self.loan_growth_value = loan_growth_value

    def _adjusted_amount(self, base: float, year: int, growth_type: str, growth_value: float) -> float:
        if growth_type == "percent":
            return base * ((1 + (growth_value / 100)) ** year)
        elif growth_type == "fixed":
            return base + (growth_value * year)
        return base

    def run(self) -> List[Dict]:
        capital = self.starting_capital
        loan = self.starting_loan

        history = []

        for year in range(1, self.years + 1):
            real_factor = (1 + self.inflation_rate) ** year

            adjusted_investment = self._adjusted_amount(
                self.static_investment, year - 1, self.investment_growth_type, self.investment_growth_value
            )
            adjusted_loan = self._adjusted_amount(
                self.static_new_loan, year - 1, self.loan_growth_type, self.loan_growth_value
            )

            cash_injection = self.cash_injections.get(year, 0)
            debt_injection = self.debt_injections.get(year, 0)
            withdrawal = self.withdrawals.get(year, 0)
            debt_repayment = self.debt_repayments.get(year, 0)

            total_cash_added = adjusted_investment + cash_injection - withdrawal
            total_debt_added = adjusted_loan + debt_injection - debt_repayment

            capital += total_cash_added
            loan += total_debt_added

            interest_payment = loan * self.loan_interest_rate
            investment_gain = capital * self.static_return

            capital += investment_gain
            capital -= interest_payment

            net = capital - loan
            real_gross = capital / real_factor
            real_loan = loan / real_factor
            real_net = net / real_factor

            # Final simplified return: just gain minus interest
            annual_return = investment_gain - interest_payment

            history.append({
                "year": year,
                "gross": capital,
                "loan": loan,
                "net": net,
                "real_gross": real_gross,
                "real_loan": real_loan,
                "real_net": real_net,
                "annual_return": annual_return,
                "cash_injection": cash_injection,
                "debt_injection": debt_injection,
                "interest_payment": interest_payment,
                "investment_gain": investment_gain
            })

        return history





