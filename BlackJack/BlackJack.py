import random # To Shuffle Deck

class Card: # Playing Cards Class
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck: # Deck Class
        # Class Attributes
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Jack":10, "Queen":10, "King":10, "Ace":11} 

        def __init__(self): # Constructor generating shuffled deck of 52 cards
            self.cards = []
            for suit in self.suits:
                for rank in self.ranks:
                    self.cards.append(Card(suit, rank, self.values[rank]))
            random.shuffle(self.cards)

        def deal(self): # Deals and removes a card from the deck
             dealtCard = self.cards[-1]
             self.cards.pop()
             return dealtCard


class Participant: # Superclass of classes 'Player' and 'Dealer'
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0

    def handleAce(self): # Handles "Ace" as 11 or 1
        for card in self.hand:
            if card.rank == "Ace" and self.score > 21:
                self.score = self.score - 10
                return self.score

    def getScore(self):
        self.score = 0
        for card in self.hand:
            self.score = self.score + card.value
        if self.score > 21: # Ace handling
            self.handleAce()
        return self.score

    def hit(self, deck):
        self.hand.append(deck.deal())
        self.getScore()

    def showHand(self):
        print(self.name + "'s Hand: " + ", ".join(str(card) for card in self.hand))
        print(self.name + "'s Score: " + str(self.score))
        

class Player(Participant): # Subclass of 'Participant'
    def __init__(self, name):
        super().__init__(name)
    
    def action(self): # Hit or Stand
        hit_stand = input("Hit or Stand (h/s): ")
        return hit_stand
    

class Dealer(Participant): # Subclass of 'Participant'
    def __init__(self):
        super().__init__("Dealer")

    def action(self, deck):
        while self.score < 17: # Dealer must hit until they have score of 17 or more (https://bicyclecards.com/how-to-play/blackjack)
            self.hit(deck)


class BlackJack: # Main Game
    def __init__(self):
        self.deck = Deck()
        self.dealer = Dealer()
        self.player = Player(input("Enter name: "))

    def cardSetup(self): # Setup initial 2 cards for Dealer and Player
        for i in range(2):
            self.dealer.hit(self.deck)
            self.player.hit(self.deck)

    def winOrLose(self):
            if self.dealer.score > 21:
                self.dealer.showHand()
                print('-----------------------')
                self.player.showHand()
                print('-----------------------')
                print("Dealer BUST! You Win!")
            elif self.player.score > self.dealer.score:
                self.dealer.showHand()
                print('-----------------------')
                self.player.showHand()
                print('-----------------------')
                print("You Win!")
            elif self.player.score < self.dealer.score:
                self.dealer.showHand()
                print('-----------------------')
                self.player.showHand()
                print('-----------------------')
                print("You Lose :(")
            else:
                self.dealer.showHand()
                print('-----------------------')
                self.player.showHand()
                print('-----------------------')
                print("It's a Tie -_-")

    def resetGame(self): # Resets the Game
        self.deck = Deck()
        self.dealer = Dealer()
        self.player = Player(self.player.name)        

    def playGame(self): # Main Game
        print("\n\n=======BLACKJACK=======")
        self.cardSetup()
        game_state = True

        print('-----------------------')
        self.dealer.showHand()
        print('-----------------------')
        self.player.showHand()
        print('-----------------------')

        # Game Loop
        while True:
            if self.player.score == 21:
                print("You have Blackjack! You Win!")
                # print("=======================")
                game_state = False
                break # Player has Blackjack, end game
            elif self.dealer.score == 21:
                print("Dealer has Blackjack! You Lose :(")
                # print("=======================")
                game_state = False
                break # Dealer has Blackjack, end game

            player_action = self.player.action()
            if player_action == 'h':
                print("\n==========HIT==========")
                self.player.hit(self.deck)
                self.dealer.showHand()
                print('-----------------------')
                self.player.showHand()
                print('-----------------------')
                if self.player.score > 21:
                    print("BUST!")
                    game_state = False
                    break # Player bust, end game
            elif player_action == 's':
                print("\n=========STAND=========")
                self.dealer.action(self.deck)
                break

        if game_state == True: # Use winOrLose method if above criteria are not met
            self.winOrLose()

        replay = input("Play again (y/n): ")
        if replay == 'y':
            self.resetGame()
            self.playGame()


game = BlackJack()
game.playGame()