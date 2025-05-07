class TargetChecker:
    def __init__(self, results):
        self.results = results  # Store the simulation results

    def find_wealth_target(self, target, net=True):
        """
        Finds the first year where the net or gross wealth reaches the target.
        :param target: The wealth target amount.
        :param net: True to check net wealth, False for gross wealth.
        :return: The year when the target is reached, or None if never reached.
        """
        for row in self.results:
            value = row['net'] if net else row['gross']
            if value >= target:
                return row['year']
        return None

    def find_annual_gain_target(self, gain_target, inflation_adjusted=False):
        """
        Finds the first year where the annual return (real money) reaches the target.
        :param gain_target: The target annual gain.
        :param inflation_adjusted: (Kept for compatibility, not used here now.)
        :return: The year when the gain target is reached, or None if never reached.
        """
        for row in self.results:
            gain = row['annual_return']  # Use the updated key from simulator
            if gain >= gain_target:
                return row['year']
        return None

