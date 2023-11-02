import numpy as np
import seaborn as sns

from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

from typing import Any

rng = np.random.default_rng(seed=2000)


class Hotelling(Model):
    """ 
    Model objects manages key global variables such as \
    time, positions, and global parameters and variables.
    """

    def __init__(self, N, width, height, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.schedule = SimultaneousActivation(self)
        self.grid = MultiGrid(width, height, torus=False)

        # Get N colors for N agents
        n_colors = sns.color_palette(
            "colorblind",
            n_colors=N,
            as_cmap=True,
        )

        # Create agents
        for i in range(N):
            a = Shop(color=n_colors[i], unique_id=i, model=self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = rng.integers(self.grid.width)
            y = rng.integers(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def recalculate_areas(self):
        # initial areas dict is empty
        areas = {}

        # set up counts for each shop
        for shop in self.schedule.agents:
            areas[shop] = 0

        # iterate over each cell
        for content, (x, y) in self.grid.coord_iter():
            _dist = {}
            for shop in self.schedule.agents:
                _dist[shop] = euclid_dist(x, y, shop.pos[0], shop.pos[1])
            _choice = min(_dist, key=_dist.get)
            areas[_choice] += 1

        return areas

    def step(self):
        # clock will be updated before market shares are readjusted
        # should not cause any conflicts since its effect is almost simultaneous
        self.schedule.step()
        self.recalculate_areas()


# Utils
def euclid_dist(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
