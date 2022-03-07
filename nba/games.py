from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from nba import API_URI
from nba.util import get_paginated_data
from nba.teams import Team


@dataclass
class Game:
    id: int
    date: datetime
    period: int
    postseason: bool
    season: int
    status: str
    time: str
    home_team: Team
    home_team_score: int
    visitor_team: Team
    visitor_team_score: int

    @property
    def winner(self) -> Optional[Team]:
        if self.home_team_score > self.visitor_team_score:
            return self.home_team
        elif self.home_team_score < self.visitor_team_score:
            return self.visitor_team
        else:
            return None

    @property
    def loser(self) -> Optional[Team]:
        if self.home_team_score < self.visitor_team_score:
            return self.home_team
        elif self.home_team_score > self.visitor_team_score:
            return self.visitor_team
        else:
            return None


def get_season_games(season: int) -> list[Game]:
    data = get_paginated_data(
        f"{API_URI}/games", params={"seasons[]": [season], "per_page": 100}
    )

    def convert(game: dict) -> Game:
        out = Game(**game)
        out.home_team = Team(**game["home_team"])
        out.visitor_team = Team(**game["visitor_team"])

        return out

    return [convert(i) for i in data]


@dataclass
class TeamStats:
    team_name: str = ""
    won_games_as_home_team: int = 0
    won_games_as_visitor_team: int = 0
    lost_games_as_home_team: int = 0
    lost_games_as_visitor_team: int = 0


def get_season_stats(season: int) -> list[TeamStats]:
    stats = defaultdict(TeamStats)

    games = get_season_games(season)

    for game in games:
        winner, loser = game.winner, game.loser
        home_team, visitor_team = game.home_team, game.visitor_team

        # No winner/loser -> match was a tie
        if not winner or not loser:
            continue

        if winner == home_team:
            stats[winner.id].won_games_as_home_team += 1
        elif winner == visitor_team:
            stats[winner.id].won_games_as_visitor_team += 1

        if loser == home_team:
            stats[loser.id].lost_games_as_home_team += 1
        elif loser == visitor_team:
            stats[loser.id].lost_games_as_visitor_team += 1

        for team in winner, loser:
            if not stats[team.id].team_name:
                stats[team.id].team_name = f"{team.full_name} ({team.abbreviation})"

    return list(stats.values())
