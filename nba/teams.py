from collections import defaultdict
from dataclasses import dataclass

from nba import API_URI
from nba.util import get_paginated_data


@dataclass
class Team:
    id: int
    abbreviation: str
    city: str
    conference: str
    division: str
    full_name: str
    name: str

    @property
    def name_with_abbreviation(self) -> str:
        return f"{self.full_name} ({self.abbreviation})"


def get_grouped_teams():
    data = get_paginated_data(f"{API_URI}/teams")

    grouped = defaultdict(list)
    for team in data:
        team = Team(**team)
        grouped[team.division].append(team)

    return grouped
