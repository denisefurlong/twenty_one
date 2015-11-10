import random

FACE_CARDS = {
    1: 'A',
    11: 'J',
    12: 'Q',
    13: 'K'
}

class Hand(list):
    """
    Represents a hand of cards. 
    """

    def current_score(self):
        """
        Calculates the score for the hand
        """
        score = 0
        total_aces = 0
        for card_number in self:
            # each suit has 13 cards
            # the list goes from 0 to 51 so that is why we add 1 here
            value = (card_number % 13) + 1
            # if there's an ace in the hand, add 11 instead of 1
            if value == 1:
                score += 11
                total_aces += 1
            else:
                # if its 10 or above its a face card so only add 10
                score += min(10, value)

        # if the hand is bust and we previously added 11 for aces,
        # change these aces to 1 until the score is reduced to 21
        while score > 21 and total_aces:
            score -= 10
            total_aces -= 1

        return score

    def _string_list(self):
        """
        Returns a list of strings representing the hand.
        """
        card_strings = []
        for card_number in self:
            suit_num = card_number/13
            # spade
            if suit_num < 1:
                suit = u"\u2660"
            # heart
            elif suit_num < 2:
                suit = u"\u2665"
            # club
            elif suit_num < 3:
                suit = u"\u2663"
            # diamond
            else:
                suit = u"\u2666"

            value = (card_number % 13) + 1
            value = FACE_CARDS[value] if value in FACE_CARDS else value
            card_strings.append(suit + str(value))
        return card_strings

    def hidden(self):
        """
        Returns the hand as a string with the first card hidden.
        Used to partially show the dealer's hand. 
        """
        strings = self._string_list()
        strings[0] = "??"
        return u", ".join(strings)

    def __str__(self):
        return u", ".join(self._string_list())


class Game(object):
    """
    Represents a game of twenty-one.
    """
    status = 'playing'

    def __init__(self):
        """
        Starts the game by creating the card deck, shuffling and dealing. 
        """
        self.card_deck = list(range(52))
        self.shuffle_deck()
        self.deal_hand()

    def shuffle_deck(self):
        """
        Shuffles the deck.
        """
        random.shuffle(self.card_deck)

    def deal_hand(self):
        """
        Deals the cards.
        """
        self.player = Hand()
        self.dealer = Hand()

        for i in range(4):
            if i % 2:
                self.player.append(self.card_deck.pop())
            else:
                self.dealer.append(self.card_deck.pop())
        self._check_hand()

    def hit(self):
        """
        Hits the player with a card.
        """
        self.player.append(self.card_deck.pop())
        if self.player.current_score() > 21:
            self._dealer_winner()
            return

        self._dealer_hit()

    def stand(self):
        """
        Ends the round for the player, but the dealer continues to play
        until it scores 17 or greater.
        """
        while (self._dealer_hit()):
            pass
        if self.status == 'playing':
            score_player = self.player.current_score()
            score_dealer = self.dealer.current_score()
            if score_player == score_dealer:
                self._tie()
            elif score_player > score_dealer:
                self._player_winner()
            else:
                self._dealer_winner()

    def _dealer_hit(self):
        """
        Deals a card to the dealer. Returns False if the dealer's score is
        >= 17 or has gone bust. Returns True otherwise.
        """
        if self.dealer.current_score() < 17:
            self.dealer.append(self.card_deck.pop())
            if self.dealer.current_score() > 21:
                self._player_winner()
                return False
            else:
                return True
        else:
            return False

    def _player_winner(self):
        """
        Sets status to indicate player has won.
        """
        self.status = 'player'

    def _dealer_winner(self):
        """
        Sets status to indicate dealer has won.
        """
        self.status = 'dealer'

    def _tie(self):
        """
        Sets status to indicate a tie.
        """
        self.status = 'tie'

    def _check_hand(self):
        """
        Checks the scores after the hand has been dealt for a twenty-one score or
        a tie. 
        """
        player_score = self.player.current_score()
        dealer_score = self.dealer.current_score()
        if player_score == 21 and dealer_score != 21:
            self.status = 'twenty-one'
        elif player_score == 21 and dealer_score == 21:
            self.status = 'tie'
        elif dealer_score == 21:
            self.status = 'dealer'
            