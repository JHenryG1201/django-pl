from django.db import models

# Create your models here.
class Team(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    abbr = models.CharField(max_length=10)
    match_played = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    win_count = models.IntegerField(default=0)
    draw_count = models.IntegerField(default=0)
    lose_count = models.IntegerField(default=0)
    goal_scored = models.IntegerField(default=0)
    goal_conceded = models.IntegerField(default=0)
    goal_difference = models.IntegerField(default=0)
    rank = models.IntegerField()

class Player(models.Model):
    id = models.CharField(primary_key=True, max_length=10000)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    minutes_played = models.IntegerField()
    goal_scored = models.IntegerField()
    goal_conceded = models.IntegerField()
    assists = models.IntegerField()
    position = models.CharField(max_length=10)
    saves = models.IntegerField()
    penalties_saved = models.IntegerField()
    own_goal_scored = models.IntegerField()
    cleansheets = models.IntegerField()
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()
    
class Fixture(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    gameweek = models.CharField(max_length=2)
    finished = models.BooleanField()
    kickoff_time = models.DateTimeField()
    team1_id = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
    team2_id = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2')
    team1_score = models.IntegerField(null=True)
    team2_score = models.IntegerField(null=True)

class Guess(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.PROTECT)
    team_1_score = models.IntegerField()
    team_2_score = models.IntegerField()
    guess_name = models.CharField(max_length=100)