

# Babies and their daycare preferences
babies = {
    "Baby1": ["A", "B", "C"],
    "Baby2": ["B", "A", "C"],
    "Baby3": ["A", "C", "B"],
    "Baby4": ["C", "A", "B"],
    "Baby5": ["B", "C", "A"]
}

# Maximum capacity of each daycare
max_capacity = {
    "A": 2,
    "B": 2,
    "C": 1
}

# Remaining capacity
capacity = max_capacity.copy()

# Distance from each baby to each daycare
distance = {
    "Baby1": {"A": 2, "B": 4, "C": 8},
    "Baby2": {"A": 5, "B": 2, "C": 6},
    "Baby3": {"A": 3, "B": 7, "C": 4},
    "Baby4": {"A": 9, "B": 5, "C": 2},
    "Baby5": {"A": 6, "B": 3, "C": 5}
}

# Threshold set by each daycare
threshold = {
    "A": 3,
    "B": 5,
    "C": 2
}

# Initially, no babies are matched
allocation = {baby: None for baby in babies}

# Go through each baby
for baby in babies:

    # Look through the baby's preferences
    for daycare in babies[baby]:

        # Check whether the daycare still has capacity
        if capacity[daycare] > 0:

            # Distance between baby and daycare
            d = distance[baby][daycare]

            # Does the baby pass the daycare's threshold?
            if d <= threshold[daycare]:

                # Match baby to daycare
                allocation[baby] = daycare

                # Reduce remaining capacity
                capacity[daycare] -= 1

                # Stop looking at other daycares
                break

# Find unmatched babies
unmatched_babies = [
    baby for baby in allocation
    if allocation[baby] is None
]

# Find blocking pairs
blocking_pairs = []

for baby in babies:

    for daycare in max_capacity:

        # Baby cannot form a blocking pair with its current daycare
        if allocation[baby] == daycare:
            continue

        current_daycare = allocation[baby]

        # Does the baby prefer this daycare to their current allocation?
        if current_daycare is None:
            baby_prefers = True
        else:
            baby_prefers = (
                babies[baby].index(daycare)
                < babies[baby].index(current_daycare)
            )

        if not baby_prefers:
            continue

        # Babies currently assigned to this daycare
        assigned_babies = [
            b for b in allocation
            if allocation[b] == daycare
        ]

        # If daycare has an empty place, it would accept the baby
        if len(assigned_babies) < max_capacity[daycare]:
            blocking_pairs.append((baby, daycare))
            continue

        # If daycare is full, compare distances
        farthest_baby = max(
            assigned_babies,
            key=lambda b: distance[b][daycare]
        )

        # Daycare prefers the new baby because it is closer
        if distance[baby][daycare] < distance[farthest_baby][daycare]:
            blocking_pairs.append((baby, daycare))


print("Allocation:", allocation)
print("Unmatched babies:", unmatched_babies)
print("Number of unmatched babies:", len(unmatched_babies))
print("Blocking pairs:", blocking_pairs)
print("Number of blocking pairs:", len(blocking_pairs))

