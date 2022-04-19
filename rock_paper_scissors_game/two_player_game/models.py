from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    '''
    Player model 
    '''
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Create or retrieve a placeholder
def get_sentinel_player():
    return Player.objects.get_or_create(name="deleted")[0]
# Create an additional method to return only the id - default expects an id and not a Model object
def get_sentinel_player_id():
    return get_sentinel_player().id

class Game(models.Model):
    class Meta:
        unique_together = (('game_id', 'player'),)

    game_id = models.IntegerField(default = 0)
    player = models.ForeignKey(
        Player,
        db_column='player',
        on_delete=models.SET(get_sentinel_player),
        default=get_sentinel_player_id
    )
    score = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.game_id)

class GameMove(models.Model):
    '''
     model in which all players result will be stored
    '''
    id = models.BigAutoField(primary_key=True)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='game')
    player = models.ForeignKey("Player", on_delete=models.DO_NOTHING, related_name='player')
    move = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)
