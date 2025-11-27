import requests
import json
from .models import Team, Fixture, Player

POSITIONS = {1 : 'キーパー', 2 : 'ディフェンダー', 3 : 'ミッドフィルダー', 4 : 'フォワード'}

def initiate_db():
    try:
        response1 = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
        response1.raise_for_status()
        data1 = response1.json()
        teams_data = data1['teams']
        players_data = data1['elements']

        for team in teams_data:
            Team.objects.update_or_create(
                id = team['id'],
                defaults={
                    'name': team['name'],
                    'abbr': team['short_name'],
                    'rank': team['position'],
                    'code': team['code'],
                }
            )

        for player in players_data:
            if player['can_select']:
                Player.objects.update_or_create(
                    id = player['id'],
                    defaults={
                        'team_id': Team.objects.get(id=player['team']),
                        'code': player['code'],
                        'first_name': player['first_name'],
                        'last_name': player['second_name'],
                        'minutes_played': player['minutes'],
                        'goal_scored': player['goals_scored'],
                        'goal_conceded': player['goals_conceded'],
                        'assists': player['assists'],
                        'position': POSITIONS[player['element_type']],
                        'saves': player['saves'],
                        'penalties_saved': player['penalties_saved'],
                        'own_goal_scored': player['own_goals'],
                        'cleansheets': player['clean_sheets'],
                        'yellow_cards': player['yellow_cards'],
                        'red_cards': player['red_cards'],
                    },
                )

        response2 = requests.get('https://fantasy.premierleague.com/api/fixtures/')
        response2.raise_for_status()
        fixture_data = response2.json()

        for fixture in fixture_data:
            Fixture.objects.update_or_create(
                id = fixture['id'],
                defaults={
                    'gameweek': fixture['event'],
                    'finished': fixture['finished'],
                    'kickoff_time': fixture['kickoff_time'],
                    'team1_id': Team.objects.get(id = fixture['team_a']),
                    'team2_id': Team.objects.get(id = fixture['team_h']),
                    'team1_score': fixture['team_a_score'],
                    'team2_score': fixture['team_h_score'],
                },
            )

            if fixture['finished']:

                team1 = Team.objects.get(id=fixture['team_h'])
                team2 = Team.objects.get(id=fixture['team_a'])
    
                team1.match_played += 1
                team2.match_played += 1
    
                team1.goal_scored += fixture['team_h_score']
                team2.goal_scored += fixture['team_a_score']
    
                team1.goal_conceded += fixture['team_a_score']
                team2.goal_conceded += fixture['team_h_score']
    
                team1.goal_difference = team1.goal_scored - team1.goal_conceded
                team2.goal_difference = team2.goal_scored - team2.goal_conceded
    
                if fixture['team_a_score'] == fixture['team_h_score']:
                    team1.draw_count += 1
                    team2.draw_count += 1
                elif fixture['team_a_score'] > fixture['team_h_score']:
                    team2.win_count += 1
                    team1.lose_count += 1
                else:
                    team1.win_count += 1
                    team2.lose_count += 1
    
                team1.point = (team1.win_count * 3) + team1.draw_count
                team2.point = (team2.win_count * 3) + team2.draw_count
    
                team1.save()
                team2.save()
    except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
    except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
