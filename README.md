🏏 IPL Stats API

A Flask-based REST API to fetch detailed IPL statistics for teams, batsmen, and bowlers.
The API uses ball-by-ball and match-level data (fetched from Google Sheets) to generate records and head-to-head stats.

🚀 Features

* Teams *

  - Get all IPL teams
  - Team vs Team head-to-head record
  - Team overall record (wins, losses, titles, etc.)

* Batting *
    - Career stats for any batsman (runs, avg, strike rate, 50s, 100s, HS, etc.)
    - Batsman vs Team stats

* Bowling *

    - Career stats for any bowler (wickets, economy, average, SR, 3+W, best figures, etc.)
    - Bowler vs Team stats

📌 API Endpoints

* Root

    - GET /<br>
    Returns a simple hello message.

* Teams

    - GET /api/teams<br>
    Returns a list of all IPL teams.

    - GET /api/teamVteam?team1=<team1>&team2=<team2><br>
    Returns head-to-head record between two teams.

    - GET /api/team-record?team=<team><br>
    Returns overall record of a given team.

    - GET /api/teamAPI?team=<team><br>
    Returns team’s record overall and against every opponent.

* Batting

    - GET /api/batting-record?batsman=<player_name><br>
    Returns career stats and vs-team breakdown for the given batsman.

* Bowling

    - GET /api/bowler-record?bowler=<player_name><br>
    Returns career stats and vs-team breakdown for the given bowler.