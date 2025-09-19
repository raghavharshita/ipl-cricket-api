from flask import Flask,jsonify,request
import ipl

app=Flask(__name__)

@app.route('/')
def home():
    return "hello world"

@app.route('/api/teams')
def teams():
    teams=ipl.total_teams()
    return jsonify(teams)

@app.route('/api/teamVteam')
def teamVteam():
    team1=request.args.get('team1')
    team2=request.args.get('team2')

    response=ipl.teamVteamAPI(team1,team2)
    return jsonify(response)


@app.route('/api/team-record')
def team_record():
    team_name=request.args.get('team')
    response=ipl.allrecord(team_name)
    return response

@app.route('/api/teamAPI')
def teamAPI():
    team_name=request.args.get('team')
    response=ipl.teamsAPI(team_name)
    return jsonify(response)


@app.route('/api/batting-record')
def batting_record():
    batsman=request.args.get('batsman')
    response=ipl.batsmanAPI(batsman)
    return jsonify(response)

@app.route('/api/bowler-record')
def bowler_record():
    bowler=request.args.get('bowler')
    response=ipl.bowlerAPI(bowler)
    return jsonify(response)

app.run(debug=True)