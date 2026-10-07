import numpy as np


class ProperAlgorithm:
    """
    Online matching algorithm using predictive capacity prices.

    The algorithm balances:
    - utility for the arriving baby
    - utility for the daycare
    - the expected future value of remaining daycare capacity

    Previous assignments cannot be changed.
    """

    def __init__(
    self,
    daycares,
    total_babies,
    beta=0.5,
    gamma=0.1,
    threshold_max=0.7,
    threshold_min=0.4
):
        self.daycares = daycares
        self.total_babies = total_babies
        self.beta = beta
        self.gamma = gamma
        self.threshold_max = threshold_max
        self.threshold_min = threshold_min

        self.arrivals_seen = 0
        self.utility_sum = np.zeros(len(daycares))
        self.assignments = {}

    # ---------------------------------------------------------
    # Estimate future demand
    # ---------------------------------------------------------

    def estimate_future_demand(self):
        """
        Estimate the future demand for each daycare.

        The average daycare utility among observed babies is
        used as an estimate of how attractive the daycare will
        be to future babies.

        Returns:
            Expected future demand for every daycare.
        """

        if self.arrivals_seen == 0:
            return np.zeros(len(self.daycares))

        # Average attractiveness of each daycare
        average_utility = (
            self.utility_sum / self.arrivals_seen
        )

        # Number of babies that have not arrived yet
        babies_remaining = (
            self.total_babies - self.arrivals_seen
        )

        # Expected future demand
        future_demand = (
            babies_remaining * average_utility
        )

        return future_demand

    # ---------------------------------------------------------
    # Calculate capacity prices
    # ---------------------------------------------------------

    def calculate_capacity_prices(self):
        """
        Calculate the value of remaining capacity.

        A daycare gets a higher price when:
        - expected future demand is high
        - remaining capacity is low
        """

        future_demand = self.estimate_future_demand()

        prices = np.zeros(len(self.daycares))

        for daycare in self.daycares:

            remaining = daycare.remaining_capacity

            if remaining > 0:
                prices[daycare.id] = (
                    self.gamma
                    * future_demand[daycare.id]
                    / remaining
                )
            else:
                prices[daycare.id] = np.inf

        return prices

    # ---------------------------------------------------------
    # Match one baby
    # ---------------------------------------------------------

    def match_baby(self, baby):
        prices = self.calculate_capacity_prices()

        best_daycare = None
        best_score = -np.inf
        best_baby_utility = -np.inf

        for daycare in self.daycares:
            if daycare.remaining_capacity <= 0:
                continue

            baby_utility = baby.utilities[daycare.id]
            daycare_utility = daycare.utilities[baby.id]

            score = (
                baby_utility
                + self.beta * daycare_utility
                - prices[daycare.id]
            )

            if score > best_score:
                best_score = score
                best_daycare = daycare
                best_baby_utility = baby_utility

        if best_daycare is None:
            self.assignments[baby.id] = None
            self.update_demand_information(baby)
            return None

        threshold = self.get_threshold()

        # Reject if this baby has no sufficiently good available option
        if best_baby_utility < threshold:
            self.assignments[baby.id] = None
            self.update_demand_information(baby)
            return None

        best_daycare.taken_capacity += 1
        self.assignments[baby.id] = best_daycare.id

        self.update_demand_information(baby)

        return best_daycare.id

    # ---------------------------------------------------------
    # Update information about observed demand
    # ---------------------------------------------------------

    def update_demand_information(self, baby):
        """
        Update the observed demand information using the
        current baby's daycare utilities.
        """

        for daycare in self.daycares:

            self.utility_sum[daycare.id] += (
                daycare.utilities[baby.id]
            )

        self.arrivals_seen += 1

    def get_threshold(self):
        if self.total_babies <= 1:
            return 0.0

        progress = self.arrivals_seen / (self.total_babies - 1)

        threshold = (
            self.threshold_max
            - (self.threshold_max - self.threshold_min) * progress
        )

        return threshold