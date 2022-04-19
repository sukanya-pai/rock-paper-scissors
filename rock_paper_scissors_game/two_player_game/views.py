# Django Import
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from two_player_game.models import *
from django.db.models import F

# Python Import
import random
import logging
log = logging.getLogger(__name__)

def home(request):
    '''
    homepage and redirect to start game logic
    '''
    if request.method=='POST':
        details = {
            'player1name':request.POST.get('player1name'),
            'mode':request.POST.get('mode'),
            'player2name':request.POST.get('player2name','Computer')
        }
        return render(request,'game.html',details)

    return render(request, 'home_page.html')

def about(request):
    '''
    about page
    '''
    return render(request, 'about.html')

def contact(request):
    '''
    contact page
    '''
    return render(request, 'contact.html')


def game(request):
    if request.method == 'POST':
        details = {
            'player1name':request.POST.get('player1name'),
            'mode':request.POST.get('mode'),
            'player2name':request.POST.get('player2name','Computer'),
        }
        
        # player1 = Player.objects.get_or_create(name=details['player1name'])
        # player2 = Player.objects.get_or_create(name=details['player2name'])

        player1option = request.POST.get('player1option')
        # Play with player mode
        if details['mode'] == 'player':
            player2option = request.POST.get('player2option')
            messages.info(request, f"You selected {player1option}, {details['player2name']} selected {player2option}" )
        else:
            player2option = get_computer_option()
            messages.info(request, f"You selected {player1option}, computer selected {player2option}")
        
        
        # process the game
        result = process_game(request, player1option, player2option)

        # # Save details
        # game = Game(player1 = player1,
        #             player2 = player2,
        #             player1_move = player1option,
        #             player2_move = player2option,
        #             winner = result['winner'])
        # game.save()

        # # Save score
        # player1_score = GameResult(game = game_id, player = player1, score = F('player1score') + 1)
        # player1_score.save()
        # player2_score = GameResult(game = game_id, player = player2, score = F('player2score') + 1)
        # player2_score.save()

        return render(request,'game.html',details)



def get_computer_option():
    """
    Function to get computer's option
    """
    gamelist = ['rock', 'paper', 'scissors']
    computer_option = random.choice(gamelist)
    return computer_option

def process_game(request, player_one_option, player_two_option):
    winner = None
    player1score = 0
    player2score = 0

    if player_one_option == player_two_option:
        messages.info(request, f"Both players selected same option. It's a tie!")
        log.debug("Both players selected same option. It's a tie!")
    elif player_one_option == "rock":
        if player_two_option == "scissors":
            winner = player1name
            messages.success(request, "Rock smashes scissors! You win!")
        else:
            messages.info(request, "Paper covers rock! You lose.")
    elif player_one_option == "paper":
        if player_two_option == "rock":
            messages.success(request, "Paper covers rock! You win!")
        else:
            messages.info(request, "Scissors cuts paper! You lose.")

    elif player_one_option == "scissors":
        if player_two_option == "paper":
            messages.success(request, "Scissors cuts paper! You win!")
        else:
            messages.info(request, "Rock smashes scissors! You lose.")
        


