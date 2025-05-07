class WealthSimulator:
    def __init__(self, years, starting_capital, starting_loan, static_return, static_investment, static_new_loan,
                 inflation_rate, loan_interest_rate=0.0,
                 cash_injections=None, debt_injections=None, withdrawals=None, debt_repayments=None):
        self.years = years
        self.starting_capital = starting_capital
        self.starting_loan = starting_loan
        self.static_return = static_return / 100
        self.static_investment = static_investment
        self.static_new_loan = static_new_loan
        self.inflation_rate = inflation_rate / 100
        self.loan_interest_rate = loan_interest_rate / 100 if loan_interest_rate else 0.0
        self.cash_injections = {int(k): v for k, v in (cash_injections or {}).items()}
        self.debt_injections = {int(k): v for k, v in (debt_injections or {}).items()}
        self.withdrawals = {int(k): v for k, v in (withdrawals or {}).items()}
        self.debt_repayments = {int(k): v for k, v in (debt_repayments or {}).items()}

    def run(self):
        results = []
        gross = self.starting_capital + self.starting_loan
        loan = self.starting_loan
        net = gross - loan
        previous_net = net
        previous_gross = gross

        for year in range(1, self.years + 1):
            # Track this year's injections and interest
            cash_change = 0
            debt_change = 0
            interest_payment = 0

            # Interest calculated before any changes
            if self.loan_interest_rate > 0:
                interest_payment = loan * self.loan_interest_rate
                loan += interest_payment

            # Calculate investment gain on previous gross
            investment_gain = previous_gross * self.static_return
            gross += investment_gain

            # Apply cash injection or withdrawal
            if year in self.withdrawals:
                cash_change = -self.withdrawals[year]
                gross -= self.withdrawals[year]
            elif year in self.cash_injections:
                cash_change = self.cash_injections[year]
                gross += self.cash_injections[year]
            else:
                cash_change = self.static_investment
                gross += self.static_investment

            # Apply loan or repayment
            if year in self.debt_repayments:
                debt_change = -self.debt_repayments[year]
                loan -= self.debt_repayments[year]
                gross -= self.debt_repayments[year]
            elif year in self.debt_injections:
                debt_change = self.debt_injections[year]
                loan += self.debt_injections[year]
                gross += self.debt_injections[year]
            else:
                debt_change = self.static_new_loan
                loan += self.static_new_loan
                gross += self.static_new_loan

            loan = max(0, loan)
            net = gross - loan

            # Final return: change in net minus cash added
            investment_return = (net - previous_net) - cash_change

            # Save previous for next round
            previous_net = net
            previous_gross = gross

            # Inflation adjustment
            inflation_factor = (1 + self.inflation_rate) ** year
            results.append({
                'year': year,
                'gross': gross / inflation_factor,
                'loan': loan / inflation_factor,
                'net': net / inflation_factor,
                'annual_return': investment_return / inflation_factor,
                'cash_injection': cash_change,
                'debt_injection': debt_change,
                'interest_payment': interest_payment,
                'investment_gain': investment_gain
            })

        return results





