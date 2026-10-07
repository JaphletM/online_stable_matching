import numpy as np
import matplotlib.pyplot as plt


def plot_matching(
    daycares,
    babies,
    assignments,
    title="Matching",
    show_lines=False
):
    """
    Visualize a matching between babies and daycares.

    Daycares are shown as squares.
    Babies are shown as dots.
    A matched baby gets the same color as its assigned daycare.
    Unmatched babies are shown in black.

    show_lines:
        If True, draw a line between every matched baby
        and its assigned daycare.
    """

    fig, ax = plt.subplots(figsize=(8, 8))

    # Create one color for every daycare
    num_daycares = len(daycares)
    colors = plt.cm.tab10(
        np.linspace(0, 1, num_daycares)
    )

    # --------------------------------------------------
    # Plot daycares
    # --------------------------------------------------

    for daycare, color in zip(daycares, colors):

        ax.scatter(
            daycare.location[0],
            daycare.location[1],
            marker="s",
            s=250,
            color=color,
            edgecolor="black",
            linewidth=1.5,
            label=f"Daycare {daycare.id}"
        )

    # --------------------------------------------------
    # Plot babies
    # --------------------------------------------------

    for baby, assignment in zip(babies, assignments):

        if assignment is None:
            # Unmatched baby
            ax.scatter(
                baby.location[0],
                baby.location[1],
                marker="o",
                s=50,
                color="black"
            )

        else:
            # Matched baby gets daycare's color
            color = colors[assignment]

            ax.scatter(
                baby.location[0],
                baby.location[1],
                marker="o",
                s=50,
                color=color,
                edgecolor="black",
                linewidth=0.5
            )

            # ------------------------------------------
            # Optional connection line
            # ------------------------------------------

            if show_lines:
                daycare = daycares[assignment]

                ax.plot(
                    [baby.location[0], daycare.location[0]],
                    [baby.location[1], daycare.location[1]],
                    color=color,
                    linewidth=0.8,
                    alpha=0.5
                )

    # --------------------------------------------------
    # Formatting
    # --------------------------------------------------

    ax.set_title(title)
    ax.set_xlabel("x-coordinate")
    ax.set_ylabel("y-coordinate")

    ax.axhline(0, linewidth=0.5)
    ax.axvline(0, linewidth=0.5)

    ax.set_aspect("equal", adjustable="box")

    ax.legend()

    plt.show()