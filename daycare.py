import numpy as np
from dataclasses import dataclass, field
'''
Daycare properties:
- ID: Just the number of the daycare
- Location: A 1x2 vector containing 2D coordinates (x, y)
- Capacity: The capacity of the daycare
- taken_capacity: The capacity already occupied by babies


distance_to() calculates the distance between the daycare and a baby using
pythagoream theorem
'''
@dataclass
class Daycare:
    id: int
    location: np.ndarray
    capacity: int
    taken_capacity: int = 0
    utilities: dict[int, float] = field(default_factory=dict)

    @property
    def remaining_capacity(self):
        return self.capacity - self.taken_capacity

    ##Calculate the distance between the daycare and the baby
    def distance_to(self, baby):
        dx = self.location[0] - baby.location[0]
        dy = self.location[1] - baby.location[1]

        return np.sqrt(dx**2 + dy**2)

    #Reset the capacity of current daycare
    def reset(self):
        self.taken_capacity = 0

    #Generates utilities according to ADM Log, std is used for the max distances
    def generate_utilities(
        self,
        babies,
        std
    ):
        """
        Generate the utility of every baby for this daycare.
        """

        #Distance from top left corner to bottom right corner
        max_distance = std*3

        for baby in babies:

            distance = self.distance_to(baby)

            utility = max(0, 1 - (
                distance / max_distance
            ) ** 2)

            self.utilities[baby.id] = utility
