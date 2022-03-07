# NBA CLI

Command line tool for viewing data about NBA players, teams and matches.

## Running
This project runs under Python 3.9 and above. 

Install project requirements
```
$ pip install -r requirements.txt
```

## Examples
Teams grouped by division
```
$ python main.py grouped-teams

Southeast
    Atlanta Hawks (ATL)
    Charlotte Hornets (CHA)
    Miami Heat (MIA)
    Orlando Magic (ORL)
    Washington Wizards (WAS)
Atlantic
    Boston Celtics (BOS)
    Brooklyn Nets (BKN)
    ...
```

Tallest and heaviest player with a given name
```
$ python main.py players-stats --name Michael

Tallest player: Michael Porter Jr. - 2.08 m
Heaviest player: Michael Beasley - 106.59 kg
```

Wins and loses per team for a given season
```
$ python main.py teams-stats --season 2021

Houston Rockets (HOU)
    won games as home team: 10
    won games as visitor team: 9
    lost games as home team: 22
    lost games as visitor team: 28
Detroit Pistons (DET)
    won games as home team: 11
    won games as visitor team: 9
    lost games as home team: 22
    lost games as visitor team: 27
...
```

## Teams stats output formats
Supported output formats: `csv`, `json`, `sqlite`, `stdout` (default)
