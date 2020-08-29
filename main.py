import time, os, sys
from random import randint
from zones import *
from questions import *
from enemies import *

def titleScreen():
    title = True
    play = False
    help_ = False
    options = False
    with open('title.txt') as title:
        cntnts = title.read()
        os.system('cls')
    print(cntnts)

prompt = '> '
output = ''

name = 'Gregory'
job = 'Warrior'

choice = ''
menuChoices = ['play', 'help', 'options', 'quit']

title = True
play = False
help_ = False
options = False

#=======================================================================# Write Function

def write(string):
    for char in string:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
    print()

#=======================================================================# Setup Game Function

def setupGame(name, job):
    write('Hello. What is your name?')
    name = input(prompt)
    write('What job would you like?')
    write('You can play as Mage, Warrior, or Priest.')
    joblist = ['mage', 'warrior', 'priest']
    job = input(prompt).lower().strip()
    while not job in joblist:
        write('That is not a valid Job.')
        job = input(prompt).lower().strip()
    write(f'Welcome, {name} the {job}!')
    write(f'Are you ready to play?')
    while True:
        ready = input(prompt).lower().strip()
        if ready == 'y' or ready == 'yes':
            write('Cool! Let\'s go!')
            break
        elif ready == 'n' or ready == 'no':
            write('Ok. Just play again when you\'re ready!')
            time.sleep(1)
            main()
            break
        else:
            write('I do not understand that answer.')

#=======================================================================# Classes

class Player(object):
    def __init__(self):
        self.name = 'bob'
        self.job = 'warrior'
        self.health = 50
        self.location = 'a2'
        self.lastLocation = 'a2'
        self.isBlocking = False
        self.isFighting = False
        self.attackrange = [2, 5]
    def move(self):
        write('Where would you like to move to? ')
        where = input(prompt)
        print()
        if where in ['up', 'north']:
            if ZONEMAP[player.location][UP] == 'none':
                write('I cannot go anymore in that direction.')
            else:
                player.lastLocation = player.location
                player.location = ZONEMAP[player.location][UP]
                printLocation()
        elif where in ['down', 'south']:
            if ZONEMAP[player.location][DOWN] == 'none':
                write('I cannot go anymore in that direction.')
            else:
                player.lastLocation = player.location
                player.location = ZONEMAP[player.location][DOWN]
                printLocation()
        elif where in ['left', 'west']:
            if ZONEMAP[player.location][LEFT] == 'none':
                write('I cannot go anymore in that direction.')
            else:
                player.lastLocation = player.location
                player.location = ZONEMAP[player.location][LEFT]
                printLocation()
        elif where in ['right', 'east']:
            if ZONEMAP[player.location][RIGHT] == 'none':
                write('I cannot go anymore in that direction.')
            else:
                player.lastLocation = player.location
                player.location = ZONEMAP[player.location][RIGHT]
                printLocation()
        else:
            write('I do not know where that is.')

player = Player()

#=======================================================================# Do Correct Thing Function

def doCorrectThing():
    if choice == 'play':
        play()
    elif choice == 'options':
        options()
    elif choice == 'help':
        help_()
    elif choice == 'quit':
        quit_()
    else:
        getChoice()
        doCorrectThing()

#=======================================================================# Play Function

def play():
    play = True
    title = False
    options = False
    help_ = False
    setupGame(name, job)
    player.name = name
    player.job = job
    printLocation()
    while True:
        if player.isFighting:
            bossattack = randint(ENEMIES[player.location][ATTACKRANGE[0]], ENEMIES[player.location][ATTACKRANGE[1]])
            if player.isBlocking:
                write(f'{ENEMIES[player.location][NAME]} tried to damage you for {bossattack} health, but you were blocking.')
            else:
                player.health -= bossattack
                write(ENEMIES[player.location][NAME] + ' just damaged you for ' + str(bossattack) + ' damage! You\'re now on ' + str(player.health) + ' health.')
                write(f'{ENEMIES[player.location][NAME]} is on {str(ENEMIES[player.location][HEALTH])} health.')
        if player.health <= 0:
            write('You died!')
            time.sleep(1)
            main()
            break
        doPrompt()

#=======================================================================# Options Menu

def options():
    play = False
    title = False
    options = True
    help_ = False
    pass

#=======================================================================# Help Menu

def help_():
    play = False
    title = False
    options = False
    help_ = True
    pass

#=======================================================================# Quit Function

def quit_():
    play = False
    title = False
    options = False
    help_ = False
    print('k bye')
    time.sleep(0.5)
    exit()

#=======================================================================# Main Function

def main():
    titleScreen()
    getChoice()
    doCorrectThing()

#=======================================================================# MAP

"""
PLAYER STARTS AT A2

+-----------+
|a1|a2|a3|a4|
|--+--+--+--|
|b1|b2|b3|b4|
|--+--+--+--|
|c1|c2|c3|c4|
|--+--+--+--|
|d1|d2|d3|d4|
+-----------+
"""

#=======================================================================# Print Location Function

def printLocation():
    os.system('cls')
    print('----------------------------')
    write(f'- {ZONEMAP[player.location][ZONENAME]}')
    write(f'- {ZONEMAP[player.location][DESCRIPTION]}')
    if not player.location == 'a1':
        write('- You have already solved this zone.' if player.location in SOLVEDZONES else '- You have not solved this zone.')
    else:
        write('- You do not need to solve this zone - It is your home.')
    print('----------------------------')


SOLVEDZONES = []


def doPrompt():
    print('\n=====================================')
    write('What would you like to do?')
    action = input(prompt).lower()
    acceptable_actions = ['solved', 'load', 'save', 'move', 'go', 'travel', 'walk', 'quit', 'examine', 'inspect', 'look', 'attack', 'fight', 'run', 'flee', 'defend', 'block']
    while action not in acceptable_actions:
        write('Unknown action, Try again.\n')
        action = input(prompt).lower()
    if action == 'quit':
        quit_()
    elif action in ['move', 'go', 'travel', 'walk']:
        if player.isFighting:
            write('You can only flee/run while in a boss fight!')
        else:
            player.move()
    elif action in ['examine', 'inspect', 'interact', 'look']:
        write(f'You examine: {ZONEMAP[player.location][EXAMINATION]}')
        if player.location in SOLVEDZONES:
            write('You have already solved this puzzle.')
        elif ZONEMAP[player.location][HASQUESTION]:
            write(QUESTIONS[player.location]['Q'])
            answer = input(prompt).lower().strip()
            if answer == QUESTIONS[player.location]['A']:
                write(f'{str(len(SOLVEDZONES))}/15 Puzzles Solved!')
                ZONEMAP[player.location][SOLVED] = True
                SOLVEDZONES.append(player.location)
            else:
                write('You got it wrong.')
        elif ZONEMAP[player.location][HASENEMY]:
            write(f'You discover a {ENEMIES[player.location][TYPE]}, {ENEMIES[player.location][NAME]}.')
            player.isFighting = True

    elif action in ['attack', 'fight']:
        if player.isFighting:
            playerAttack = randint(player.attackrange[0], player.attackrange[1])
            ENEMIES[player.location][HEALTH] -= playerAttack
            write(f'You attacked {ENEMIES[player.location][NAME]} for {str(playerAttack)} health.')
            if ENEMIES[player.location][NAME] <= 0:
                write(f'You killed {ENEMIES[player.location][NAME]}!')
                SOLVEDZONES.append(player.location)
                write('You have solved ' + str(len(SOLVEDZONES)) + '/15 Zones.')
        else:
            write('There is nothing to attack!')
    elif action in ['run', 'flee']:
        if player.isFighting:
            player.location = player.lastLocation
            write('You ran from the beast, to your last location.')
            player.isFighting = False
            time.sleep(0.8)
            printLocation()
        else:
            write('There is nothing to run from!')
    elif action in ['defend', 'block']:
        if player.isFighting:
            write('You chose to block.')
            player.isBlocking = True
        else:
            write('There is nothing to defend from!')
    elif action == 'solved':
        write('Solved Zones:')
        for index, zone in enumerate(SOLVEDZONES):
            if index == len(SOLVEDZONES) - 1:
                print(zone)
            else:
                print(zone + ', ')
    elif action == 'save':
        if player.isFighting:
            write('You cannot save while in a fight!')
        else:
            try:
                with open('savenames.txt', 'r') as f:
                    savenames = f.readlines()
            except FileNotFoundError:
                savenames = []
            write('What would you like to call this save?')
            savename = input(prompt).strip().lower()
            if savename in savenames:
                write('There is already a save with that name!')
            else:
                write('Saving game...')
                with open ('savenames.txt', 'a') as sn:
                    sn.write(savename)
                time.sleep(1)
                try:
                    with open('gamesave-' + savename, 'w') as savefile:

                        # SAVE PLAYER INFO
                        savefile.write(player.name + '\n')
                        savefile.write(player.job + '\n')
                        savefile.write(player.health + '\n')
                        savefile.write(player.location + '\n')
                        savefile.write('Solved: ')
                        for index, zone in enumerate(SOLVEDZONES):
                            if index == len(SOLVEDZONES) - 1:
                                savefile.write(zone + '\n')
                            else:
                                savefile.write(zone + ', ')
                        # do rest of save, bosses etc

                        savefile.write('\n')
                        savefile.write('BOSSES')
                        savefile.write('\n')
                        savefile.write('Boss Locations: ')
                        for index, boss in enumerate(ENEMIES):
                            if index == len(ENEMIES) - 1:
                                savefile.write(boss + '\n')
                            else:
                                savefile.write(boss + ', ')
                        savefile.write('Bosses Healths in Order: ')
                        for index, boss in enumerate(ENEMIES):
                            if index == len(ENEMIES) - 1:
                                savefile.write(boss[HEALTH] + '\n')
                            else:
                                savefile.write(boss[HEALTH] + ', ')
                    write('Game Saved!')
                except:
                    write('There was an error saving the game. Please try again.')
                time.sleep(1.5)
    elif action == 'load':
        try:
            with open('savenames.txt', 'r') as f:
                savenames = f.readlines()
                write('What is the name of the save you would like to load?')
                print('You current saves are: ', end='')
                for index, sn in enumerate(savenames):
                    if index == len(savenames) - 1:
                        print(sn)
                    else:
                        print(sn + ', ', end='')
                snl = input(prompt).lower().strip()
                if snl in savenames:
                    write(f'Loading \'{snl}\'...')
                    time.sleep(0.8)

                    # LOAD THE GAME SAVE HERE

                else:
                    write('You do not have a save under that name.')
                    
        except FileNotFoundError:
            write('You do not have any saves to load.')

main()