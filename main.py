import numpy as np
from predictiveshadowpricematching import PredictiveShadowPriceMatching
from simulation import (
    generate_daycares,
    generate_babies,
    run_algorithm,
    reset_daycares
)
from greedy import BabyGreedy, DaycareGreedy
from visualization import plot_matching
from properalgorithm import ProperAlgorithm

# Simulation parameters

n_babies = 100
n_daycares = 5

alpha = 0.7 #How much of the Utility of the babies depends on the preferences

#Std for the normal distribution of the locations (both babies and daycares)
location_std = 10

#Parameters for the capacity initialization
capacity_ratio = 0.8 #Ratio of total capacity spots / total babies (So if 500 babies there are 400 spots with 0.8 capacity ratio)
mean_capacity = capacity_ratio * n_babies / n_daycares #Parameter used for the poisson distribution for the capacity
print(f"Mean capacity per daycare: {mean_capacity}")

#RNG Initialization
seed = 20
rng = np.random.default_rng(seed)


# -----------------------------
# Generate instance
# -----------------------------

daycares = generate_daycares(
    n_daycares=n_daycares,
    rng=rng,
    location_std=location_std,
    mean_capacity=mean_capacity,
)

babies = generate_babies(
    n_babies=n_babies,
    daycares=daycares,
    rng=rng,
    location_std=location_std
)

for baby in babies:
    baby.generate_utilities(daycares, alpha=alpha)

for daycare in daycares:
    daycare.generate_utilities(babies, std=location_std)


#Run simulation

# Baby greedy
baby_greedy = BabyGreedy(daycares)

print()
print("Baby Greedy")

baby_greedy_results, baby_greedy_assignments = run_algorithm(
    baby_greedy,
    babies,
    daycares
)



plot_matching(
    daycares,
    babies,
    baby_greedy_assignments,
    title="Baby Greedy",
    show_lines=False
)

reset_daycares(daycares)


daycare_greedy = DaycareGreedy(daycares)

print()
print("Daycare Greedy")
daycare_greedy_results, daycare_greedy_assignments = run_algorithm(
    daycare_greedy,
    babies,
    daycares
)



plot_matching(
    daycares,
    babies,
    daycare_greedy_assignments,
    title="Daycare Greedy",
    show_lines=False
)

reset_daycares(daycares)

#Start our algoritm
proper_algorithm = ProperAlgorithm(
    daycares=daycares,
    total_babies=n_babies,
    beta=0.5,
    gamma=0.1,
    threshold_max=1,
    threshold_min=0.4
)

print()
print("Proper Algorithm")
proper_results, proper_assignments = run_algorithm(
    proper_algorithm,
    babies,
    daycares
)


plot_matching(
    daycares,
    babies,
    proper_assignments,
    title="Proper Algorithm",
    show_lines=False
)
