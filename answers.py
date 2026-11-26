# Average goals per game between 1900 and 2000

import pandas as pd

matches = pd.read_csv("results.csv", parse_dates=["date"])
period = matches[matches["date"].dt.year.between(1900, 2000)]
average_goals = (period["home_score"] + period["away_score"]).mean()

print(average_goals)

# Create a query that counts the number of shootouts wins by country and arrange in alphabetical order.

shootouts = pd.read_csv("shootouts.csv")
shootout_wins = (
    shootouts.groupby("winner")
    .size()
    .rename("wins")
    .rename_axis("country")
    .reset_index()
    .sort_values("country")
)

print(shootout_wins)

# Create a reliable key that allows the joining together of goal scorers, results, and shootouts.


def add_match_key(frame):
    frame = frame.copy()
    frame["date"] = pd.to_datetime(
        frame["date"], errors="raise").dt.strftime("%Y-%m-%d")
    frame["home_team"] = frame["home_team"].str.strip()
    frame["away_team"] = frame["away_team"].str.strip()
    frame["match_key"] = list(
        zip(frame["date"], frame["home_team"], frame["away_team"])
    )
    return frame


goalscorers = add_match_key(
    pd.read_csv("goalscorers.csv", dtype={
                "home_team": "string", "away_team": "string"})
)
results = add_match_key(
    pd.read_csv("results.csv", dtype={
                "home_team": "string", "away_team": "string"})
)
shootouts = add_match_key(
    pd.read_csv("shootouts.csv", dtype={
                "home_team": "string", "away_team": "string"})
)
