'''
Foundations of a Simplified BlackJack Game
'''

from random import shuffle
import os
class Deck():
    '''
    Create an instance of a shuffled deck of cards
    '''
    num_cards = 52
    suits = ['Heart', 'Spade', 'Diamond', 'Club']
    digit_cards = list(range(2, 11))
    special_cards = ['Jack', 'Queen', 'King', 'Ace']

    def __init__(self, cards=None):

        if cards is None:
            cards = []

        self.make_deck(**{'num_cards':Deck.num_cards, 'suits':Deck.suits, \
        'digit_cards':Deck.digit_cards, 'special_cards':Deck.special_cards})

        print("Here's your deck")

    def make_deck(self, **kwargs):
        '''
        Make a deck of cards to spec.  Defaults to digits 1 - 10, no special cards, single suit
        '''
        self.cards = []
        newdeck = []
        cardtypes = kwargs.get("digit_cards", list(range(1, 11)))+kwargs.get("special_cards", [])

        for cardtype in cardtypes:
            for suit in kwargs.get("suits", ['DefaultSuit']):
                newdeck.append(';'.join([str(cardtype), str(suit)])) #Ensure typing consistent

        #Validate Deck
        if len(newdeck) == Deck.num_cards:
            self.cards = newdeck.copy()
            return None
        print('Deck invalid')
        return None

    def shuffle_deck(self, num_shuffles):
        '''
        Shuffle cards of deck object X number of times
        '''
        for _ in range(num_shuffles):
            shuffle(self.cards)
        print('Deck Shuffled {} times.'.format(num_shuffles))

    def collect_cards(self, hands):
        '''
        Round up all the hands ane put back into the deck
        '''
        print('Currently have {} cards'.format(len(self.cards)))
        for hand in hands:
            #Put cards in the deck
            print('Adding {} cards from player {}'.format(hand.cards, hand.playername))
            for card in hand.cards:
                self.cards.append(card)

            #Empty Hand
            hand.cards = []

        #Validate Deck
        if len(self.cards) == Deck.num_cards:
            print('Collected all the Cards.  Deck Size: ', len(self.cards))
        else:
            print('Deck is off. Make a new deck - Deck Size: ', len(self.cards))

class Dealer():
    '''
    Dealer Actions and Methods
    '''
    playername = 'Dealer'
    def __init__(self, bankroll):
        self.bankroll = bankroll

    def deal(self, deck, hands):
        '''
        Pop top cards out of the deck object
        '''
        #Deal top(or is it bottom?) card of deck to each hand
        if type(hands) == list:
            for hand in hands:
                hand.add_card(deck.cards.pop())
            return hands

        hands.add_card(deck.cards.pop())
        return hands

class Player():
    '''
    Provide and Validate Player Action Methods
    '''
    def __init__(self, playername='NewPlayer', bankroll=0):
        self.playername = playername
        self.bankroll = bankroll
        print('Welcome Player {}.  Your Balance is ${}'.format(self.playername, self.bankroll))


class Table():
    '''
    Define the playing field.  How many seats empty/filled, the button, dealing order.
    '''
    def __init__(self, num_seats, decks, players, pot_value, board=None):
        self.num_seats = num_seats
        self.decks = decks
        self.players = players
        self.pot_value = 0
        print('At This Table: \n Players: {}\n The deck: {}\n Chairs {}'\
        .format(self.players, self.decks, self.num_seats))

        if board is None:
            self.board = {}
            for player in self.players:
                self.board[player.playername] = ''

    def show_card(self, card, playername):
        '''
        Add's shown card to the board
        '''
        try:
            self.board[playername] += card + '   '
        except:
            print('Could not show cards')

    def draw(self):
        '''
        Draw Board and other features
        '''
        os.system('cls')
        bufferzone = 20*'@@'
        print("Pot Value: {}".format(self.pot_value))
        print(bufferzone.center(50), '\n\n')
        for player in self.players:
            print(player.playername, '({})'.format(player.bankroll),\
             ' Showing: ', self.board[player.playername])
            print('')
        print('\n\n', bufferzone.center(50))

    def bet(self, player, betsize):
        '''
        Betting methods affecting bankroll and table value
        '''
        try:
            betsize = int(betsize)
            print('bet of {} received on bankroll of {}'.format(betsize, player.bankroll))
        except:
            print('Only Cash, Credit, or Bitcoin!')

        if player.bankroll >= betsize:
            player.bankroll -= betsize
            self.pot_value += betsize
        else:
            print('You Do Not Have The Money!')
            return False

    def bank(self, winner):
        winner.bankroll += self.pot_value
        self.pot_value = 0

    def clear_board(self):
        for player in self.players:
            self.board[player.playername] = ''


class Hand():
    '''
    Track Player's Hand
    '''
    def __init__(self, cards=None, playername=None, points=None):
        if cards is None:
            self.cards = []
            self.points = 0
        self.playername = playername

    def add_card(self, card):
        '''
        Add dealt card to hand
        '''
        self.cards.append(card)
        self.count_cards()

    def count_cards(self):
        '''
        Calculate points in hand
        '''
        total_points = 0

        for card in self.cards:
            cardinfo = card.split(';')[0]
            if cardinfo in Deck.special_cards:
                total_points += 10
            else:
                total_points += int(cardinfo)

        self.points = total_points

    def jackpot_bust(self):
        if self.points == 21:
            print('Jackpot!  Congradulations ', self.playername)
            return 'win'
        elif self.points > 21:
            print('BUST!  Player {} Loses'.format(self.playername))
            return 'lose'
        return 'stay'


def main():
    '''
    Initialize Game
    '''
    #Generate a deck and shuffle it a few times
    newdeck = Deck()
    newdeck.shuffle_deck(5)

    #Sit some players down
    dealer = Dealer(100000)
    player1 = Player('Acer', 1000)
    # player2 = Player('Fox', 25000)

    players = [player1, dealer]

    #Gen table player key to reference player objects in players later on
    playerkey = {}
    i = 0
    for player in players:
        playerkey[player.playername] = i
        i += 1

    #Seat everyone at a table
    newtable = Table(num_seats=3, decks=newdeck, players=players, pot_value=0)
    hands = [Hand(playername=player.playername) for player in players]

    '''
    The following comprises the turn-based events in the game.
    '''

    newgame = True
    while newgame:

        #Shuffle Deck
        newdeck.shuffle_deck(3)

        #Deal Cards (2 to each hand)
        print('Dealing Cards')
        dealer.deal(deck=newdeck, hands=hands)
        dealer.deal(deck=newdeck, hands=hands)

        #Flip Cards
        for hand in hands:
            i = 0 #creating a counter so the second dealer card is flipped
            for card in hand.cards:
                if hand.playername != 'Dealer':
                    newtable.show_card(card=card, playername=hand.playername)
                elif hand.playername == 'Dealer' and i == 1:
                    newtable.show_card(card=card, playername=hand.playername)
                i += 1
        newtable.draw()

        #Game Mechanics - Betting
        print('Place Your Bets!\n')
        for player in players:
            newtable.bet(player, input('How Much Do You bet {}? Max ({})'.\
            format(player.playername, player.bankroll)))

            newtable.draw()

        #Game Mechanics - Drawing Cards
        game = True
        for hand in hands:
            if game:
                while True:
                    if input("It is {}'s turn.\nHit (H) or Stay(S):  ".format(hand.playername)).lower() == 'h':
                        print('Player ', hand.playername, 'hits')
                        newcards = dealer.deal(deck=newdeck, hands=hand)
                        newtable.show_card(card=newcards.cards[-1], playername=hand.playername)
                        newtable.draw()
                        
                        status = hand.jackpot_bust()
                        if status == 'win':
                            newtable.bank(players[playerkey[hand.playername]])
                            game = False
                            break
                        elif status == 'lose':
                            newtable.bank(players[playerkey['Dealer']])
                            game = False
                            break

                    else:
                        print('Player ', hand.playername, 'stays')
                        newtable.draw()
                        break

        #If all hands stay under 21
        if game:
            scores = []
            for hand in hands:
                scores.append([hand.playername, hand.points])
            winner = sorted(scores, key = lambda x: x[1]).pop()
            newtable.bank(players[playerkey[winner[0]]])
            print('winner is: ', winner)
            input('\nPress Any Key to Continue')

        #Collect all cards
        newdeck.collect_cards(hands = hands)
        input('\nPress Any Key to Continue')
        
        #Reset Board
        newtable.clear_board()
        newtable.draw()

        #Start a new game
        newtable.draw()
        if input('Play Again (Y/N) or Press Any Key to Exit:   ').lower() == 'y':
            newgame = True
        else:
            newgame = False

if __name__ == '__main__':
    main()
