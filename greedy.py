class BabyGreedy:
    """
    Always assign the arriving baby to their highest-ranked
    available daycare.
    """

    def __init__(self, daycares):
        self.daycares = daycares
        self.assignments = {}

    def match_baby(self, baby):

        best_daycare = None
        best_utility = -float("inf")

        for daycare in self.daycares:

            if daycare.remaining_capacity <= 0:
                continue

            utility = baby.utilities[daycare.id]

            if utility > best_utility:
                best_utility = utility
                best_daycare = daycare

        if best_daycare is None:
            self.assignments[baby.id] = None
            return None

        best_daycare.taken_capacity += 1
        self.assignments[baby.id] = best_daycare.id

        return best_daycare.id


class DaycareGreedy:
    """
    Always assign the arriving baby to the closest
    available daycare.
    """

    def __init__(self, daycares):
        self.daycares = daycares
        self.assignments = {}

    def match_baby(self, baby):

        best_daycare = None
        best_utility = -float("inf")

        for daycare in self.daycares:

            if daycare.remaining_capacity <= 0:
                continue

            utility = daycare.utilities[baby.id]

            if utility > best_utility:
                best_utility = utility
                best_daycare = daycare

        if best_daycare is None:
            self.assignments[baby.id] = None
            return None

        best_daycare.taken_capacity += 1
        self.assignments[baby.id] = best_daycare.id

        return best_daycare.id