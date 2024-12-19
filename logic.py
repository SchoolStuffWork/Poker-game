from random import randint
from time import sleep
import pygame
pygame.init()

pictureCards = {
  "A" : 14,
  "K" : 13,
  "Q" : 12,
  "J" : 11
} #gives the values the each picture card holds in a lookup table

def insertion_sort(hand):
  #takes a hand to do an insertions sort
  if not hand:
    return []
  #returns an empty list of hand is empty
  
  sortedHand = [hand[0]]
  #appends the first item of the hand into a new list
  
  for i in range(1,len(hand)):
    #for loop which of hand length except first item
    
    inserted = False
    for j in range(len(sortedHand)):
      if hand[i] < sortedHand[j]:
      #iterates through sortedHand to find the correct position to insert the item
        sortedHand.insert(j, hand[i])
        inserted = True
        #if hand[i] is smaller than the previous element it is appended at position j
        #then the loop breaks
        break
    if not inserted:
      sortedHand.append(hand[i])
  return sortedHand
      

def shuffle(deck):
  length = len(deck)
  #gives the lenght of the array
  for i in range(length-1,0,-1):
    #for loop that decreases starting from the last item going down
    n = randint(0,i)
    #finds a random variable between 0 and i

    deck[i], deck[n] = deck[n], deck[i]
    #switches the position of item[i] and item[n]
    #switches i with a random item from the list to the left of i
  return deck

values = [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]
suits = ["S","C","H","D"]
#the values and suits that a card can be


class Card:
  def __init__ (self, value, suit):
    self.value = value
    self.suit = suit
    #assigns a value and a suit to every card

  def __repr__(self):
        return f'Card("{self.value}", "{self.suit}")'
        #Creates the cards objects in the format that I actualy want them
        #otherwise it would just show a bunch of random numbers and letters

  @classmethod
  def create_cards(cls, values, suits): 
    cards = []
    #empty list to add the cards to
    for suit in suits:
      for value in values: 
      #loops through suits and cards 
      #every combination is created
        cards.append(cls(value, suit))
    return cards

  @classmethod
  def suit(cls,item):
    return item[1]
    #returns the suit of a card
    
  @classmethod
  def value(cls,item):
    
    pictureCards = {"A": 14, "K": 13, "Q": 12, "J": 11}
    #lookup table for picture cards
    if isinstance(item.value, int):
        return item.value
    elif item.value in pictureCards:
        #using the lookup table
        return pictureCards[item.value]
    else:
        #turn the string number into an int
        return int(item.value)
        
        



  @classmethod
  def flush(cls,cards):
    
    count = {}
    #counts the number of times a suit is repeated

    for i in cards:

      count[i.suit] = count.get(i.suit,0) + 1
      #counts the occurance of each suit

    for count in count.values():
        if count >= 5:
        #checks wether any suit appears 4 or more times
          return True
    return False


  @classmethod
  def straight(cls,cards):
    ordered = insertion_sort(list(set([cls.value(card) for card in cards])))
    #takes the cards values
    for i in range(len(ordered) - 4):
      if ordered[i + 4] - ordered[i] == 4:
      #checks all the cards are incrementing in value by one
        return True
    return False
  

  @classmethod
  #method to determine if a hand has a pair, triple, or quadruple
  def pairs(cls,cards,num=None):
    ordered = insertion_sort([cls.value(card) for card in cards])
    #sorted list of cards
    count = {}
    #dictionary to count occurances
    for i in ordered:
      count[i] = count.get(i,0) + 1

    if num is not None:
      return any(j == num for j in count.values())
      #searches for singular pairs and 3 of a kinds
    
    #variable to hold wether a 3 of a kind is present
    three = False
    pair_count = 0
    #variable which holds the number of different pairs

    for j in count.values():
      if j == 3:
        three = True
        #returns True if there is 3 of a kind
      elif j == 2:
        pair_count += 1
    #for loop goes through the cards checking if there is a pair and 3 of a kind
      
    if three and pair_count > 0:
      return "full house"
      #returns True if a full house is present

    elif pair_count == 2:
      return "2 pair"
      #checks for a 2 pair

    elif pair_count == 1:
      return "1 pair"
      #checks if there is only one pair
    
    return False
  
  @classmethod
  def high_card(self,cards):
    pcards = cards[:2]
    #only takes the players personal cards
    values = [Card.value(card) for card in pcards]
    ordered_values = insertion_sort(values)
    
    return ordered_values[len(ordered_values) - 1]
  
  @classmethod
  def ace_helper(cls,cards):
    ordered = insertion_sort([cls.value(card) for card in cards])
    #takes the cards values
    for i in range(len(ordered) - 2):
      if ordered[i] + 1 != ordered[i + 1]:
      #checks all the cards are incrementing in value by one
        return False
    return True 
  
  @classmethod  
  def ace_low(self,cards):
    values = [Card.value(card) for card in cards]
    ordered = insertion_sort(values)
    #creates a sorted list by value of the cards
     
    if Card.ace_helper(cards) == True and ordered[0] == 2 and ordered[4] == 14:
      #retruns true if the first 4 cards are a straight
      #and if the first item is a 2 while the last item is an ace
      return True
      
    else:
      return False

  

  @classmethod
  def hand_rank(cls,cards):
      points = 0
      #variable to store the "points the user has collected"
      #This will help determine the rank
      if cls.flush(cards) == True and cls.straight(cards) == True :
        points += 8 
      # identifies straight flush
      elif cls.flush(cards) == True and cls.ace_low(cards) == True:
        points += 8
      #identifies an ace low straight flush
      elif cls.pairs(cards,4) == True:
        points += 7
      #identifies 4 of a kind
      elif cls.pairs(cards) == "full house" :
        points += 6
      #identifies full house
      elif cls.flush(cards) == True:
        points += 5
      #identifies flush
      elif cls.ace_low(cards) == True:
        points += 4
      #identifies ace low straight
      elif cls.straight(cards) == True:
        points += 4
      #identifies straight
      elif cls.pairs(cards,3) == True:
        points += 3
      #identifies 3 of a kind
      elif cls.pairs(cards) == "2 pair":
        points += 2
      #identifies a 2 pair
      elif cls.pairs(cards) == "1 pair":
         points += 1
      #identifies a pair
      
      return points


#draw = [Card("Q", "H"), Card("K", "S"), Card("4", "D"), Card("5", "D"), Card("4", "C")]    
#print(Card.hand_rank(draw)) 


deck = Card.create_cards(values,suits)
#creates a deck of cards

shuffled = shuffle(deck)
#shuffles the deck of cards

#generates a river
river = []
for i in range(3):
  #for loop going 3 times
  river.append(shuffled.pop(0))
  #adds the first item from shuffled to river
  #removes that item from the deck at the same time


class Player:
  #creates a class for players
  def __init__(self, name, pos, is_turn = False, counter = 100, move = False):
    self.counter = counter
    #an attribute to hold the number of chips they have
    self.name = name
    #the players name
    self.hand = []
    #holds the players hand
    self.is_turn = is_turn
    #holds wether it is a players turn or not
    self.current_bet = 0
    #how much the player is betting in the current round
    self.move = move
    self.pos = pos


  
  def create_hand(self,shuffled,river):
    hand = []
    for j in range(2):
      hand.append(shuffled.pop(0))
      #adds 2 cards to the players hand from the deck
      #removes the cards at the same time 
    self.hand = hand + river
    #combinds those cards with the river
    return self.hand


  
  
    
  @staticmethod
  def compare(people, name=None):
    highest_rank = 0
    #variable to hold the highest rank
    highest_card = 0
    #variable to hold the highest card
    winners = []
    #list to hold who the winner is
    
    for player in people:
    #loops through the players

      rank = Card.hand_rank(player.hand)
      #the rank of the players hand
      player_high = Card.high_card(player.hand)
      #the value of the players highest card

      
      if rank > highest_rank:
        highest_rank = rank
        #updates the highest rank so that it now holds a higher rank
        highest_card = player_high
        #the highest card is updated to this players highest card
        #if the rank is lower than the high card doesnt come into play
        winners = [player]

      #if the card rankings are the same
      elif rank == highest_rank:
        if player_high > highest_card:
        #if the players high card is higher than the previous one
          highest_card = player_high
          winners = [player]
        elif player_high == highest_card:
        #if the high cards are the same  
          winners.append(player)  
        
    if name == "name":
      return [victor.name for victor in winners]
    else:
      return winners
    #returns the players name rather than the adress

  
  

  def fold(self, winners, pot):
    #winners.remove(player)
    #removes player from winners list
    if len(winners) == 1:
      print(f"{winners[0].name} has won")
      winners[0].counter += pot
      sleep(2)
      play = False
      #break
      #if this results in one player left they win

  def call(self, pot):
    difference = pot - self.current_bet
    #how much more the player needs to bet in order to match
    pot += difference
    self.current_bet += difference
    #adds this amount both to the players bet as well as the total pot
    return difference
  
  def check(self, current_bet):
    if self.current_bet == current_bet:
    #checks that the users current bet is equal to the table bet
      pass
      #passes their turn if so
    else:
      self.fold(group)
      return "wrong"

  def raise_bet(self, amount, pot):
    #gives an option for how much the player would like to raise to
    if amount <= self.counter:
        self.current_bet += amount
        pot += amount
        #adds this amount to the players bet and to the pot
        return amount
    else:
        self.fold(group)
        print("wrong")

 

#instantiates the players as objects of Player
player1 = Player(name = "player1", pos = 0)
player2 = Player(name = "player2", pos = 1)
player3 = Player(name = "player3", pos = 2)

#creates a hand for the player
player1.hand = player1.create_hand(shuffled, river)
player2.hand = player2.create_hand(shuffled, river)
player3.hand = player3.create_hand(shuffled, river)




#compares the hands of the players in the list

draw = [Card("K", "H"), Card("3", "H"), Card("8", "H"), Card("5", "H"), Card("7", "S"), Card("6","D"), Card("4","H")]    
#print(Card.hand_rank(draw))
#print(Player.compare([player1, player2], "name"))


pot = 0
winners = Player.compare([player1, player2, player3])
#function which allocates the counters to the winner/s
def allocate(winners):    
    if len(winners) < 2:
    #if there is only one winner
        winners[0].counter += pot
        #gives the winner the entire pot

    elif len(winners) >= 2:
    #if it is a draw
        split = pot / len(winners)
        #splits the pot into however many 
        for victor in winners:
            victor.counter += split
    return {victor.name: victor.counter for victor in winners}



