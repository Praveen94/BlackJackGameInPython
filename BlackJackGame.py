import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
          'Queen':10, 'King':10, 'Ace':11}

playing = True # Boolean Value to control while loops

class Card:
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank

    def __str__(self):
        return "{} of {}".format(self.rank,self.suit)

class Deck:
    def __init__(self):
        self.deck=[]
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))


    def __str__(self):
        for cards in self.deck:
            print(cards)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self,card):
        self.cards.append(card)
        self.value+=values[card.rank]

    def adjust_for_ace(self):
        self.aces+=1
        if self.value>11:
            self.value-=10

class Chips:
    def __init__(self):
        self.total=100
        self.bet=0

    def win_bet(self):
        self.total+=self.bet

    def lose_bet(self):
        self.total-=self.bet

def take_bet(player_chips):
    while True:
        print("You have {} coins".format(player_chips.total))
        try:
            betting_amount=int(input("Enter the betting amount:"))
        except ValueError:
            print("Please enter an integer.")


        if betting_amount>player_chips.total:
            print("Amount is greater than number of chips")

        else:
            print("You have a placed a betting amount of {}".format(betting_amount))
            player_chips.bet=betting_amount
            break

def hit(deck,hand):
    card=deck.deal()
    if card.rank=="Ace":
        hand.adjust_for_ace()
    hand.add_card(card)

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    while True:
        player_decision=input("Do you want to hit or stand?").upper().strip()
        if player_decision=="HIT":
            hit(deck,hand)
        elif player_decision=="STAND":
            playing=False

        else:
            print("Sorry Please repeat again.")
            continue
        break

def show_some(player,dealer):
    print("Player's Cards:")
    for card in player.cards:
        print(card)
    print("Player's Value:{}".format(player.value))
    print()
    print("="*50)
    print("Dealer's Card:")
    print(dealer.cards[0])
    print()
    print("="*50)

def show_all(player,dealer):
    print("Player's Cards:")
    for card in player.cards:
        print(card)
    print()
    print("Player's Total:{}".format(player.value))
    print("="*50)
    print("Dealer's Card:")
    for card in dealer.cards:
        print(card)
    print()
    print("Dealer's Total:{}".format(dealer.value))
    print()
    print("="*50)

def player_busts(player):
    if player.value>21:
        return True
    return False

def player_wins(player,dealer):
    if dealer.value>21 and player.value<21:
        return True
    if player.value>dealer.value and player.value<21:
        return True
    return False

def dealer_busts(dealer):
    if dealer.value>21 and player.value<21:
        return True
    return False

def dealer_wins(player,dealer):
    if dealer.value>player.value:
        return True
    elif dealer.value==21 and player.value<22:
        return True
    else:
        return False

def push(player,dealer):
    if player.value==dealer.value:
        return True
    return False


while True:
    print("Welcome To BlackJack")


    # Create & shuffle the deck, deal two cards to each player
    deck=Deck()
    deck.shuffle()
    player=Hand()
    dealer=Hand()
    player.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())


    # Set up the Player's chips
    player_chips=Chips()





    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player,dealer)


    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player)

        # Show cards (but keep one dealer card hidden)
        show_some(player,dealer)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_busts(player):
            player_chips.lose_bet()
            print("Dealer Wins")
            break

        if player.value==21:
            print("Player Wins")
            player_chips.win_bet()
            break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17

    if dealer.value<17:
        dealer.add_card(deck.deal())

        # Show all cards
    show_all(player,dealer)

        # Run different winning scenarios

    if dealer_busts(dealer):
        print("Player Wins")
        player_chips.win_bet()

    elif player_wins(player,dealer):
        print("Player Wins")
        player_chips.win_bet()

    elif player.value==dealer.value and player.value<21:
        print("Push")


    elif dealer_wins(player,dealer):
        print("Dealer Wins")
        player_chips.lose_bet()

    else:
        pass

        # Inform Player of their chips total
    print("Player has {} coins remaining".format(player_chips.total))

        # Ask to play again
    play_again=input("Do you want to play again? Y or N? ")
    if play_again=="N":
        break
    else:
        playing=True
