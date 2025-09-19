import pandas as pd
import numpy as np

ipl_matches = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRy2DUdUbaKx_Co9F0FSnIlyS-8kp4aKv_I0-qzNeghiZHAI_hw94gKG22XTxNJHMFnFVKsO4xWOdIs/pub?gid=1655759976&single=true&output=csv"
matches=pd.read_csv(ipl_matches)
matches.head()

ipl_ball = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRu6cb6Pj8C9elJc5ubswjVTObommsITlNsFy5X0EiBY7S-lsHEUqx3g_M16r50Ytjc0XQCdGDyzE_Y/pub?output=csv"
balls = pd.read_csv(ipl_ball)

ball_With_match=balls.merge(matches,on='ID',how='inner').copy()
ball_With_match['BowlingTeam']=ball_With_match.Team1+ball_With_match.Team2
ball_With_match['BowlingTeam']=ball_With_match[['BowlingTeam','BattingTeam']].apply(lambda x:x.values[0].replace(x.values[1],''),axis=1)
batter_data=ball_With_match[np.append(balls.columns.values,['BowlingTeam','Player_of_Match'])]

def total_teams():
  teams=list(set(list(list(matches['Team1'])+list(matches['Team2']))))
  team_dict={
      'teams':teams
  }
  return team_dict

def teamsAPI(team,matches=matches):
    # df = matches[(matches['Team1'] == team) | (matches['Team2'] == team)].copy()
    self_record = allrecord(team)
    TEAMS = total_teams()['teams']
    against={}
    for team2 in TEAMS:
        if team2 != team:
            against[team2]= teamVteamAPI(team, team2)

    data = {team: {'overall': self_record,
                   'against': against}}
    return data

def teamVteamAPI(team1,team2):
  try:
    temp_df=matches[((matches['Team1']==team1) & (matches['Team2']==team2)) | ((matches['Team1']==team2) & (matches['Team2']==team1))]
    total_matches=temp_df.shape[0]

    matches_won_team1=temp_df['WinningTeam'].value_counts()[team1]
    matches_won_team2=temp_df['WinningTeam'].value_counts()[team2]

    draws=total_matches-(matches_won_team1+matches_won_team2)

    response={
        'total_matches':total_matches,
        team1:int(matches_won_team1),
        team2:int(matches_won_team2),
        'draws':int(draws)
    }

    return response
  except Exception as e:
    return {
        'Error':f"no matche between {team1} and {team2}",
        'total_matches':0,
        team1:0,
        team2:0,
        'draws':0
    }

def allrecord(team):
    temp_df=matches[(matches['Team1']==team) | (matches['Team2']==team)]
    total_matches=temp_df.shape[0]

    matches_won_team=temp_df['WinningTeam'].value_counts()[team]

    draws=temp_df['WinningTeam'].isnull().sum()

    loss=total_matches-(matches_won_team+draws)

    titles=temp_df[(temp_df['MatchNumber']=='Final') & (temp_df['WinningTeam']==team)].shape[0]

    response={
        'total_matches':total_matches,
        'matches_won':int(matches_won_team),
        'matches_lost':int(loss),
        'no_result':int(draws),
        'titles':int(titles)
    }

    return response



def batsmanrecord(batsman,df):
  if df.empty:
    return np.nan
   
  out=df[df.player_out==batsman].shape[0]
  df=df[df['batter']==batsman]
  inngs=df.ID.unique().shape[0]
  runs=df.batsman_run.sum()
  fours=df[(df.batsman_run==4) & (df.non_boundary==0)].shape[0]
  sixes=df[(df.batsman_run==6) & (df.non_boundary==0)].shape[0]

  if out:
     avg=runs/out
  else:
     avg=np.inf

  nballs=df[df.extra_type!='wides'].shape[0]
  if nballs:
     strike_rate=runs/nballs*100
  else:
     strike_rate=0

  gb=df.groupby('ID').sum()
  fifties=gb[(gb.batsman_run>=50) & (gb.batsman_run<100)].shape[0]
  hundreds=gb[gb.batsman_run>=100].shape[0]

  try:
      highest_score = gb.batsman_run.sort_values(ascending=False).head(1).values[0]
      hsindex = gb.batsman_run.sort_values(ascending=False).head(1).index[0]
      if (df[df.ID == hsindex].player_out == batsman).any():
          highest_score = str(highest_score)
      else:
          highest_score = str(highest_score) + '*'
  except:
      highest_score = gb.batsman_run.max()


  not_out=inngs-out
  mom=df[df['Player_of_Match']==batsman].drop_duplicates('ID',keep='first').shape[0]
  response = {
      'innings': str(inngs),
      'runs': str(runs),
      'fours': str(fours),
      'sixes': str(sixes),
      'avg': str(avg),
      'strikeRate': str(strike_rate),
      'fifties': str(fifties),
      'hundreds': str(hundreds),
      'highestScore': str(highest_score),
      'notOut': str(not_out),
      'mom': str(mom)
  }
  return response
  
def batsmanVsteam(batsman,team,df):
   try:
    df=df[df.BowlingTeam==team]
    return batsmanrecord(batsman,df)
   except:
      return {'Error':f'No record of {batsman} against {team}'}

def batsmanAPI(batsman,df=batter_data):
    df=df[df.innings.isin([1,2])]
    self_record=batsmanrecord(batsman,df)
    TEAMS=total_teams()['teams']
    against={}
    for team in TEAMS:
        against[team]=batsmanVsteam(batsman,team,df)
  
    data={
       batsman:{
           'all':self_record,
           'against':against
        }
    }
    return data


bowler_data = batter_data.copy()

def bowlerRun(x):
    if x[0] in ['penalty', 'legbyes', 'byes']:
        return 0
    else:
        return x[1]
bowler_data['bowler_run'] = bowler_data[['extra_type', 'total_run']].apply(bowlerRun, axis=1)

def bowlerWicket(x):
    if x[0] in ['caught', 'caught and bowled', 'bowled', 'stumped', 'lbw', 'hit wicket']:
        return x[1]
    else:
        return 0
bowler_data['isBowlerWicket'] = bowler_data[['kind', 'isWicketDelivery']].apply(bowlerWicket, axis=1)


def bowlerRecord(bowler, df=bowler_data):
    df = df[df['bowler'] == bowler]
    inngs = df.ID.unique().shape[0]
    nballs = df[~(df.extra_type.isin(['wides', 'noballs']))].shape[0]
    runs = df['bowler_run'].sum()
    if nballs:
        eco = runs / nballs * 6
    else:
        eco = 0
    fours = df[(df.batsman_run == 4) & (df.non_boundary == 0)].shape[0]
    sixes = df[(df.batsman_run == 6) & (df.non_boundary == 0)].shape[0]

    wicket = df.isBowlerWicket.sum()
    if wicket:
        avg = runs / wicket
    else:
        avg = np.inf

    if wicket:
        strike_rate = nballs / wicket * 100
    else:
        strike_rate = np.nan

    gb = df.groupby('ID').sum()
    w3 = gb[(gb.isBowlerWicket >= 3)].shape[0]

    best_wicket = gb.sort_values(['isBowlerWicket', 'bowler_run'], ascending=[False, True])[
        ['isBowlerWicket', 'bowler_run']].head(1).values
    if best_wicket.size > 0:

        best_figure = f'{best_wicket[0][0]}/{best_wicket[0][1]}'
    else:
        best_figure = np.nan
    mom = df[df.Player_of_Match == bowler].drop_duplicates('ID', keep='first').shape[0]
    data = {
        'innings': str(inngs),
        'wicket': str(wicket),
        'economy': str(eco),
        'average': str(avg),
        'strikeRate': str(strike_rate),
        'fours': str(fours),
        'sixes': str(sixes),
        'best_figure': str(best_figure),
        '3+W': str(w3),
        'mom': str(mom)
    }

    return data


def bowlerVsTeam(bowler, team, df):
    df = df[df.BattingTeam == team].copy()
    return bowlerRecord(bowler, df)


def bowlerAPI(bowler, balls=bowler_data):
    df = balls[balls.innings.isin([1, 2])]  # Excluding Super overs
    self_record = bowlerRecord(bowler, df=df)
    TEAMS = matches.Team1.unique()
    against = {team: bowlerVsTeam(bowler, team, df) for team in TEAMS}
    data = {
        bowler: {'all': self_record,
                 'against': against}
    }
    return data

