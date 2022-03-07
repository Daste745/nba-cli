from dataclasses import dataclass
from typing import Optional
from functools import cache

from nba import API_URI
from nba.util import get_paginated_data, height_to_meters, weight_to_kilograms
from nba.teams import Team


@dataclass
class Player:
    id: int
    first_name: str
    last_name: str
    height_feet: Optional[int]
    height_inches: Optional[int]
    weight_pounds: Optional[int]
    position: str
    team: Team

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def height_meters(self) -> Optional[float]:
        if not self.height_feet or not self.height_inches:
            return None

        return height_to_meters(self.height_feet, self.height_inches)

    @property
    def weight_kilograms(self) -> Optional[float]:
        if not self.weight_pounds:
            return None

        return weight_to_kilograms(self.weight_pounds)


@cache
def search_players(search: str) -> list[Player]:
    data = get_paginated_data(f"{API_URI}/players", params={"search": search})

    def convert(player: dict) -> Player:
        out = Player(**player)
        out.team = Team(**player["team"])

        return out

    return [convert(i) for i in data]


def get_tallest_player(name: str) -> Optional[Player]:
    players = search_players(name)

    tallest = max(players, key=lambda p: p.height_meters or 0)

    if not tallest.height_meters:
        return None

    return tallest


def get_heaviest_player(name: str) -> Optional[Player]:
    players = search_players(name)

    heaviest = max(players, key=lambda p: p.weight_kilograms or 0)

    if not heaviest.weight_kilograms:
        return None

    return heaviest
