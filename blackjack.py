# random module is used in shuffling the deck array
import random
# sys imported for exit functionality
import sys
# initialize global vars
playerhand = ''
dealerhand = ''
newgame = ''
chump = ''
bet = 0

# class to organize attributes about the person playing blackjack
class player(object):
    wins = 0
    losses = 0
    draws = 0
    def __init__(self, name, bank):
        self.name = name
        self.bank = bank
    # adds winnings to player bank
    def bankadd(self, amt):
        self.bank += int(amt)
    # subtracts losses from player bank
    def banksubtract(self, amt):
        self.bank -= int(amt)
    # keeps track of wins, losses and draws
    def playerstats(self, winlosedraw):
        if winlosedraw == 'w':
            self.wins += 1
        elif winlosedraw == 'l':
            self.losses += 1
        else:
            self.draws += 1

# class to store the attributes of the cards and build and manage the deck array
class card(object):
    # static values to use to build the deck
    suits = ['h', 'c', 'd', 's']
    cards = range(1,14)
    deck = []

    # function to build the deck by looping through suits, then the range of cards 1-12 returning deck
    def builddeck(self):
        for suit in self.suits:
            for card in self.cards:
                self.deck.append(suit + ',' + str(card))
        return self.deck
    
    # uses the random module to shuffle the array deck
    def shuffle(self):
        random.shuffle(self.deck)
        return self.deck

    # returns a single card from the array deck by pop.   
    def dealcard(self):
        if len(self.deck) > 0:
            dealtcard = self.deck.pop()
        else:
            card.shuffle(card.builddeck())
            dealtcard = self.deck.pop()
        return dealtcard
    
    # function to change card numbers to A, J, Q, K when applicable
    def displaycard(self, disp):
        val = 0
        if len(disp) > 3:
            val = int(disp[-2:])
        else:
            val = int(disp[-1:])
        if val == 1:
            return disp[0:2] + 'A'
        elif 1 < val < 11:
            return disp[0:2] + str(val)
        elif val == 11:
            return disp[0:2] + 'J'
        elif val == 12:
            return disp[0:2] + 'Q'
        elif val == 13:
            return disp[0:2] + 'K'
    # returns played cards to the first index.  Cards are popped from the back and reshuffled each game    
    def returncards(self):
        for i in dealerhand.hand:
            self.deck.insert(0, i)
        for i2 in playerhand.hand:
            self.deck.insert(0, i2)
            
# class to manage the cards from the deck array that are in play and return them to deck array.            
class hand(object):
    # starts an empty hand
    def __init__(self):
        self.hand = []

    # calculates the value of cards in a hand
    def handmath(self):
        handval = 0
        aces = 0
        for c in self.hand:
            # captures two digit card values 10-13
            if len(c) > 3:
                handval += 10
            # assigns specific attribute to aces to be totaled after initial hand total
            elif c[-1] == "1" and len(c) < 4:
                aces += 1
            # adds single digit cards to handval
            else:
                handval += int(c[-1])
        # checks if aces exist in hand
        if aces == 1:
            if handval + 11 <= 21:
                handval += 11
            else:
                handval += 1
        # checks if multiple aces exist in hand
        elif aces > 1:
            if handval + (aces - 1) + 11 <= 21:
                handval += (aces - 1) + 11
            else:
                handval += aces
        return int(handval)
    
    def dealerhandmath(self):
        # special hand math instance for inital draw to only show dealers second card value only called once per game.
        handval = 0
        aces = 0
        # captures two digit card values 10-13
        if len(self.hand[1]) > 3:
            handval += 10
        # assigns specific attribute to aces to be totaled after initial hand total
        elif self.hand[1][-1] == "1" and len(self.hand[1]) < 4:
            aces += 1
            # adds single digit cards to handval
        else:
            handval += int(self.hand[1][-1])
        # checks if aces exist in hand
        if aces == 1:
            if handval + 11 <= 21:
                handval += 11
            else:
                handval += 1
        return int(handval)
    
class gamemechanics(object):
    # function to handle player bet input
    def placebet(self):
        global bet
        bet = 0
        # validate that player has money in bank
        if chump.bank <= 0:
            print "Sorry, we only like people with money here."
            sys.exit("Toodles!")
        else:
            # loop to get a valid bet > 0 that is not more money than the player has in player.bank
            while bet == 0:
                tempbet = raw_input("How much would you like to lose this round " + chump.name + "?")
                if int(tempbet) > 0:
                    # valid bet scenario
                    if (int(chump.bank) - int(tempbet)) >= 0:
                        bet = int(tempbet)
                    # player attempting to bet more than they have.
                    elif (int(chump.bank) - int(tempbet)) < 0: 
                        print "Try betting only the money you actually have, Mr. Wallstreet!"

    def startgame(self):
        # inital deal of 4 cards player > dealer > player > dealer
        playerhand.hand.append(card.dealcard(newgame))
        dealerhand.hand.append(card.dealcard(newgame))
        playerhand.hand.append(card.dealcard(newgame))
        dealerhand.hand.append(card.dealcard(newgame))
        
    def hitorstand(self):
        # handling for player hit or stand choice.  If player breaks 21 their loss is handled in this function.
        while playerhand.handmath() <= 21:
            action = raw_input("Enter 'h' for hit or anything else for stand: ")
            if action == 'h':
                # hit appends another card and returns the new total.  Players can hit on 21!
                playerhand.hand.append(card.dealcard(newgame))
                print newgame.displaycard(playerhand.hand[-1]) + " makes for " + str(playerhand.handmath())
            else:
                # standing is the only choice that invokes dealer logic
                print "Ok, let's see what the dealer has..."
                self.dealerlogic()
                break
        else:
            # loss handling for bust scenario
            chump.banksubtract(bet)
            chump.playerstats('l')
            print "Bust, that's no good.  Looks like we're going to keep your $" + str(bet)
            
    def dealerlogic(self):
        # The dealer will always stand at >= 16 hard or soft.
        print "Dealer has " + str(dealerhand.handmath()) + " with " + newgame.displaycard(dealerhand.hand[0]) + " and " + newgame.displaycard(dealerhand.hand[1])
        while dealerhand.handmath() <= 16:
            dealerhand.hand.append(card.dealcard(newgame))
            print "Dealer has drawn " + newgame.displaycard(dealerhand.hand[-1]) + " for " + str(dealerhand.handmath())
        # handling for if dealer busts.
        if dealerhand.handmath() > 21:
            chump.bankadd(bet*2)
            chump.playerstats('w')
            print "Dealer busts, you win!"
        # handling for natural loss by dealer
        elif dealerhand.handmath() < playerhand.handmath():
            chump.bankadd(bet*2)
            chump.playerstats('w')
            print "Dealer losts, you win!"
        # handling for natural loss by player
        elif dealerhand.handmath() > playerhand.handmath():
            chump.banksubtract(bet)
            chump.playerstats('l')
            print "Dealer wins, you lose!"
        # draw handling
        else:
            chump.playerstats('d')
            print "Either a draw or something has gone horribly wrong"
            
    def playagain(self):
        # gives player stats and current bank amount.  Uses while loop to let player play again.
        playagain = ''
        print "You have $" + str(chump.bank) + " in the bank."
        print "Your record is %s wins, %s losses and %s draws" % (str(chump.wins), str(chump.losses), str(chump.draws))
        while playagain == '':
            play = raw_input("Do you want to play again? y or n: ")
            if play == 'y':
                playagain = play
                initialize()
            elif play == 'n':
                print "Goodbye!"
                sys.exit()

def intro():
    # Intro text with name and bank input to generate your player class "chump"
    print "Welcome to my authentic Vegas-style black jack experience!"
    name = raw_input("What's your name, friend? ")
    bank = raw_input("And just how much money do you intend to lose today? ")
    print "Well %s you're a pretty high roller, waving your $%s around!" % (name, str(bank))
    print "Let's play!"
    global chump
    chump = player(name, int(bank))

def initialize():
    # Initialize the deck
    global newgame
    newgame = card()
    # Build the deck
    card.builddeck(newgame)
    # Shuffle the deck
    card.shuffle(newgame)
    # Initialize the players hand
    global playerhand
    playerhand = hand()
    # Initialize the dealers hand
    global dealerhand
    dealerhand = hand()
    gamemechanics.placebet(gamemechanics())
    gamemechanics.startgame(gamemechanics())
    print "Dealer shows: " + newgame.displaycard(dealerhand.hand[1]) + " for " + str(dealerhand.dealerhandmath())
    print "You have: " + newgame.displaycard(playerhand.hand[0]) + " and " + newgame.displaycard(playerhand.hand[1]) + " for " + str(playerhand.handmath())
    gamemechanics.hitorstand(gamemechanics())
    card.returncards(newgame)
    gamemechanics.playagain(gamemechanics())
    
def blackjack():
    # run this if you want to play blackjack.  Python 2x formatting.
    intro()
    initialize()