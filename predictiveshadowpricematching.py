import numpy as np

class PredictiveShadowPriceMatching:
    """
    Predictive Shadow-Price Matching (PSPM)

    Babies arrive one by one.
    Previous assignments cannot be changed.

    Each daycare has:
    - fixed capacity
    - preferences based on distance

    Each baby has:
    - a ranking over daycares
    - distances to every daycare
    """

    def __init__(
        self,
        capacities,
        total_babies,
        alpha=1.0,
        beta=1.0,
        gamma=0.5,
        theta=0.0,
        sigma=5.0,
        close_distance=2.0
    ):
        self.capacities = np.array(capacities, dtype=int)
        self.remaining = self.capacities.copy()

        self.num_daycares = len(capacities)
        self.total_babies = total_babies

        # Score weights
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        # Minimum score required to accept a match
        self.theta = theta

        # Controls how quickly distance utility decreases
        self.sigma = sigma

        # Distance used to define an "attractive" baby
        self.close_distance = close_distance

        # Statistics learned from previous arrivals
        self.arrivals_seen = 0
        self.close_counts = np.zeros(self.num_daycares)

        # Store assignments
        self.assignments = []

    def baby_utility(self, rank):
        """
        Convert baby's preference rank into utility.

        rank = 1 means first choice.
        """

        if self.num_daycares == 1:
            return 1.0

        return 1 - (rank - 1) / (self.num_daycares - 1)

    def daycare_utility(self, distance):
        """
        Daycare prefers babies who live closer.

        Utility = exp(-distance / sigma)
        """

        return np.exp(-distance / self.sigma)

    def estimate_future_demand(self):
        """
        Estimate how many attractive babies may still arrive
        for each daycare using observed data.
        """

        if self.arrivals_seen == 0:
            return np.zeros(self.num_daycares)

        # Estimated probability that a baby is "close"
        p_hat = self.close_counts / self.arrivals_seen

        babies_remaining = self.total_babies - self.arrivals_seen

        return babies_remaining * p_hat

    def shadow_prices(self):
        """
        Shadow price:

            lambda_j =
                gamma * predicted_future_demand / remaining_capacity
        """

        future_demand = self.estimate_future_demand()

        prices = np.zeros(self.num_daycares)

        for j in range(self.num_daycares):

            if self.remaining[j] > 0:

                prices[j] = (
                    self.gamma
                    * future_demand[j]
                    / self.remaining[j]
                )

            else:
                prices[j] = np.inf

        return prices

    def match_baby(self, preferences, distances):
        """
        Match one arriving baby.

        preferences:
            list of daycare indices ordered from best to worst.

            Example:
                [2, 0, 1]

            means:
                daycare 2 is first choice
                daycare 0 is second choice
                daycare 1 is third choice

        distances:
            distance to each daycare.

            Example:
                [3.0, 5.0, 1.0]
        """

        distances = np.array(distances)

        # -----------------------------------------------------
        # 1. Compute shadow prices BEFORE using current baby
        # -----------------------------------------------------

        lambdas = self.shadow_prices()

        scores = np.full(
            self.num_daycares,
            -np.inf
        )

        # -----------------------------------------------------
        # 2. Calculate score for every available daycare
        # -----------------------------------------------------

        for rank_position, daycare in enumerate(
            preferences,
            start=1
        ):

            if self.remaining[daycare] == 0:
                continue

            U = self.baby_utility(rank_position)

            V = self.daycare_utility(
                distances[daycare]
            )

            scores[daycare] = (
                self.alpha * U
                + self.beta * V
                - lambdas[daycare]
            )

        # -----------------------------------------------------
        # 3. Find best daycare
        # -----------------------------------------------------

        best_daycare = np.argmax(scores)
        best_score = scores[best_daycare]

        # -----------------------------------------------------
        # 4. Accept or reject
        # -----------------------------------------------------

        if best_score >= self.theta:

            assignment = best_daycare

            self.remaining[best_daycare] -= 1

        else:

            assignment = None

        # -----------------------------------------------------
        # 5. Learn from current baby's location
        # -----------------------------------------------------

        self.close_counts += (
            distances <= self.close_distance
        )

        self.arrivals_seen += 1

        self.assignments.append(assignment)

        return {
            "assignment": assignment,
            "score": best_score,
            "all_scores": scores,
            "shadow_prices": lambdas,
            "remaining_capacity":
                self.remaining.copy()
        }


