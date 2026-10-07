import numpy as np
from dataclasses import dataclass, field
'''
Baby properties:
- ID: Just the number of the baby
- Location: A 1x2 vector containing 2D coordinates (x, y)
- Preferences: A list of preferences for the daycare, unique for each baby\

- generate_utilities generates utilities based on the distance to the daycares and 
  their preference list. Using formula explained in the LOG
'''

@dataclass
class Baby:
    id: int
    location: np.ndarray
    preferences: list[int]
    utilities: dict[int, float] = field(default_factory=dict)

    def generate_utilities(
        self,
        daycares,
        alpha=0.7,
        std=10
    ):
        """
        Generate the utility of every daycare for this baby.

        Utility consists of:
        - preference utility
        - distance utility

        alpha determines the weight given to the preference.
        (1 - alpha) is the weight given to distance.
        """

        num_daycares = len(daycares)

        for rank, daycare_id in enumerate(
            self.preferences,
            start=1
        ):
            daycare = daycares[daycare_id]

            # -----------------------------
            # Preference utility
            # -----------------------------

            if num_daycares == 1:
                preference_utility = 1.0
            else:
                preference_utility = (
                    1
                    - (rank - 1) / (num_daycares - 1)
                )

            # -----------------------------
            # Distance utility
            # -----------------------------

            distance = daycare.distance_to(self)
            #Distance from top left corner to bottom right corner
            max_distance = std*3 #First took the maximum total distance, later changed it to this as this would give more proper results, ask Juul explanation.
            distance_utility = max(0, 1 - (distance / max_distance) ** 2)

            # -----------------------------
            # Combined utility
            # -----------------------------

            utility = (
                alpha * preference_utility
                + (1 - alpha) * distance_utility
            )

            self.utilities[daycare_id] = utility