#!/usr/bin/env python
from twentyone import Game
import sys

def main():
    print("""
*****************************
    Welcome!
*****************************
""")

    money = 500

    while True:
        print("You have %d" % money)
        print("How much would you like to bet?")
        bet_input = input()
        if bet_input:
            try:
                bet = int(bet_input)
            except ValueError:
                print("Invalid bet")
                continue

        if not bet:
            print("Please place a bet")
        elif bet > money:
            print("You do not have enough money to place this bet")
        else:
            game = Game()

            while game.status == 'playing':
                print("Dealer's cards: %s" % game.dealer.hidden())
                print("Your cards: %s (%d)" % (game.player, game.player.current_score()))

                print("Press 'h' to hit, press any other key to stand")
                pressed = input()
                if pressed.startswith('h'):
                    game.hit()
                else:
                    game.stand()
                    
            if game.dealer.current_score() > 21:
                print("Dealer is bust")
            elif game.player.current_score() > 21:
                print("You are bust")

            print("Dealer's cards: %s (%d)" % (game.dealer, game.dealer.current_score()))
            print("Your cards %s (%d)\n" % (game.player, game.player.current_score()))

            if game.status == "dealer":
                money -= bet
                print("Dealer is the winner")
            elif game.status == 'player':
                money += bet
                print("You are the winner")
            elif game.status == 'twenty-one':
                money += int(1.5 * bet)
                print("Twenty-one!!")
            else:
                print("Tie")

        print("\n")

        if money == 0:
            print("You are out of money")
            exit()

if __name__ == '__main__':
    main()