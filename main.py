import json
import logging
from os import environ
import dataclasses
import csv
import sqlite3

from argh import ArghParser, arg

from nba.players import get_heaviest_player, get_tallest_player
from nba.games import TeamStats, get_season_stats
from nba.teams import get_grouped_teams


def grouped_teams():
    """display all teams grouped by division"""

    grouped_teams = get_grouped_teams()

    for division, teams in grouped_teams.items():
        print(division)
        for team in teams:
            print(f"\t{team.name_with_abbreviation})")


@arg("-n", "--name", help="player name")
def players_stats(*, name: str):
    """get the heaviest and tallest player with a specific name"""

    tallest = get_tallest_player(name)
    heaviest = get_heaviest_player(name)

    tallest_info = (
        f"{tallest.full_name} - {round(tallest.height_meters, ndigits=2)} m"
        if tallest
        else "Not found"
    )

    heaviest_info = (
        f"{heaviest.full_name} - {round(heaviest.weight_kilograms,ndigits=2)} kg"
        if heaviest
        else "Not found"
    )

    print(f"Tallest player: {tallest_info}")
    print(f"Heaviest player: {heaviest_info}")


class StatWriter:
    StatList = list[TeamStats]

    @staticmethod
    def write_csv(stats: StatList):
        raw_columns = dataclasses.asdict(stats[0]).keys()
        columns = [i.replace("_", " ").title() for i in raw_columns]

        with open("output.csv", "w") as outfile:
            writer = csv.writer(outfile, delimiter="\t")

            # Header
            writer.writerow(columns)

            for team in stats:
                writer.writerow(dataclasses.astuple(team))

    @staticmethod
    def write_json(stats: StatList):
        with open("output.json", "w") as outfile:
            json.dump(stats, outfile, indent=2, default=lambda x: dataclasses.asdict(x))

    @staticmethod
    def write_sqlite(stats: StatList):
        table = "teams_stats"
        columns = ", ".join(dataclasses.asdict(stats[0]).keys())
        stats_to_write = [dataclasses.astuple(row) for row in stats]

        with sqlite3.connect("output.sqlite") as db:
            db.execute(f"drop table if exists {table}")
            db.execute(f"create table if not exists {table}({columns})")

            db.executemany(
                f"insert into {table}({columns}) values (?, ?, ?, ?, ?)",
                stats_to_write,
            )

    @staticmethod
    def write_stdout(stats: StatList):
        for team in stats:
            print(
                f"{team.team_name}\n"
                f"\twon games as home team: {team.won_games_as_home_team}\n"
                f"\twon games as visitor team: {team.won_games_as_visitor_team}\n"
                f"\tlost games as home team: {team.lost_games_as_home_team}\n"
                f"\tlost games as visitor team: {team.lost_games_as_visitor_team}"
            )


@arg(
    "-o", "--output", choices=["csv", "json", "sqlite", "stdout"], help="output format"
)
def teams_stats(*, season: int, output: str = "stdout"):
    """get statistics for a season"""

    print(f"Fetching stats for season {season}")

    stats = get_season_stats(season)

    if output == "csv":
        StatWriter.write_csv(stats)
        print("Wrote stats to output.csv")
    elif output == "json":
        StatWriter.write_json(stats)
        print("Wrote stats to output.json")
    elif output == "sqlite":
        StatWriter.write_sqlite(stats)
        print("Wrote stats to output.sqlite")
    elif output == "stdout":
        StatWriter.write_stdout(stats)


def get_parser() -> ArghParser:
    parser = ArghParser()
    parser.add_commands([grouped_teams, players_stats, teams_stats])
    return parser


if __name__ == "__main__":
    log_level = environ.get("PYTHON_LOG", "INFO").upper()
    logging.basicConfig(level=log_level)

    parser = get_parser()
    parser.dispatch()
