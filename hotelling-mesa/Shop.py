import numpy as np
from mesa import Agent

rng = np.random.default_rng(seed=2000)


class Shop(Agent):
    """
    Profit-maximizing firm (shop) will modify price \
    and location to compete for greater market share.
    """

    def __init__(self, color, unique_id, model):
        super().__init__(unique_id, model)
        self.price = rng.uniform(low=20, high=80, size=1)
        self.color = color
        self.area_count = 0
        self.pos_adjusted = None
        self.price_adjusted = None

    def __repr__(self):
        return f"Shop {self.unique_id}"

    def step(self):
        self.adjust_location()
        self.adjust_price()

        print(self.pos, self.pos_adjusted)

    def advance(self):
        self.affect_location()
        self.affect_price()

    def adjust_location(self):
        # Save initial position
        initial_pos = self.pos

        # get all possible moves
        _possible_moves = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=True
        )

        # get a mapping of all possible moves to their potential areas/market shares
        _potential_areas = {}
        for move in _possible_moves:
            self.model.grid.move_agent(self, move)
            _potential_areas[move] = self.model.recalculate_areas()[self]

        # select and store the move with the highest potential area/market share
        self.pos_adjusted = max(_potential_areas, key=_potential_areas.get)

        # pull back to initial position
        self.model.grid.move_agent(self, initial_pos)

    def adjust_price(self):
        pass

    def affect_location(self):
        self.model.grid.move_agent(self, self.pos_adjusted)

    def affect_price(self):
        pass
