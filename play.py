import pygame
from time import sleep
from logic import Player, Card , values, suits, shuffle, allocate
#in order to use the players in the rounds
from graphics import load_image
#importing the images to actualy display them

pygame.init()

#buttons which hold different values
#when pressed add that value to the player's bet
#only drawn when raise is selected
#show back of cards

#class to create a button in pygame
class Button():
  def __init__(self, x, y, width, height, text, color, hover_color, action_value=None):
  #takes the coordinates, size, text, colour and action 
    self.rect = pygame.Rect(x, y, width, height)
    #creates the button as a rectangle
    self.text = text
    self.color = color
    self.hover_color = hover_color
    self.action_value = action_value 
    

  def draw(self, surface, font):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_color = self.hover_color if self.rect.collidepoint(mouse) else self.color
    pygame.draw.rect(surface, button_color, self.rect)

    text_surface = font.render(self.text, True, "WHITE")
    text_rect = text_surface.get_rect(center=self.rect.center)
    surface.blit(text_surface, text_rect)

    if self.rect.collidepoint(mouse) and click[0] == 1:
        return self.action_value  # Return the action value when clicked
    return None



   

win = pygame.display.set_mode((800, 800))  
pygame.display.set_caption("Poker Game")
#the title and size of the display

font = pygame.font.SysFont("Arial", 16)
store = load_image()

def draw_hand(win, player, x1, y1, x2, y2 ,store, round_num):
  for index, card in enumerate(player.hand[:round_num]):
    #holds an index for card in player.hand
    card_img = f"{card.suit[0].upper()}{card.value}"
    img = store.get(card_img)

    if index < 2:  # For the first two cards
      win.blit(img, (x1 + index * 50, y1))
      #if index < 2 then it's the personal cards
    else:  
      win.blit(img, (x2 + (index - 2) * 50, y2))
      #community cards

def wait(win, font, buttons):
  while True:
    #continuesly lists events  
    for event in pygame.event.get():
      if event.type == pygame.QUIT:  
        pygame.quit()
        exit()
      #if the event is quit
      elif event.type == pygame.MOUSEBUTTONDOWN:
        #checks for mouseclick  
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
          if button.rect.collidepoint(mouse_pos):
            #checks if button is clicked 
            return button.action_value
          

    for button in buttons:
      button.draw(win, font)
      #redraws UI
    pygame.display.update()
    


          
            
    for button in buttons:
      button.draw(win, font)
      #redraws UI
    pygame.display.update()
          







title_screen = font.render(("Rules for texas hold'em"), True, (255,255,255))
buy_in_screen = font.render((":Minimum buy_in is 5 counters"), True, (255,255,255))
aces_count_screen = font.render((":Ace can be high or low"), True, (255,255,255))
sequence_screen = font.render((":Best sequence of 5 cards counted"), True, (255,255,255))
counters_screen = font.render((":0 counters is a loss"), True, (255,255,255))
order_screen = font.render((":Player1 starts every round"), True, (255,255,255))


  
def round():

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False


    win.fill((33,124,66))
    #sets the background to the colour of a poker table

    round_num = 2
    #set to 2 to show the 2 cards in the player hands
    pot = 0
    high_bet = 0
    #the highest bet of the round
    to_bet = 0
    #how much the player needs to bet to stay in the game
  

    
    deck = Card.create_cards(values, suits)
    shuffled = shuffle(deck)

    river = []
    for i in range(5):
    #for loop going 5 times
      river.append(shuffled.pop(0))
      #adds the first item from shuffled to river
      #removes that item from the deck at the same time
    
    player1 = Player(name = "player1", pos = 0)
    player2 = Player(name = "player2", pos = 1)
    player3 = Player(name = "player3", pos = 2)
    #instantiates the players as objects of Player

    
    player1.hand = player1.create_hand(shuffled, river)
    player2.hand = player2.create_hand(shuffled, river)
    player3.hand = player3.create_hand(shuffled, river)
    #creates a hand for the player

    group = [player1, player2, player3]
    winners = group[:]

    play = True
    while play:
      
      if round_num > 7:
        allocate(winners)
        win.blit(victor_screen, (500,500))
        #checks if the final rounds has ended and selects the winner
        pygame.display.update()
        sleep(5)
  
        play = False 
        return
        #ends the game

      high_bet = 0
      all_matched = False
      #holds wether every player has matched the raise amount

      player_responses = {player: False for player in group}
      #dictionary to hold wether a player has responded yet

      while not all_matched:
        all_matched = True

         

        
        
        for player in group[:]:
          if player not in winners:
            continue
          #doesn't include players who have folded
        
          if player_responses[player]:
            continue

          to_bet = high_bet
          amount = 0
          if round_num == 2:
            to_bet = 5
          
          fold_button = Button(150, 650, 100, 50, "Fold", (255, 0, 0), (200, 0, 0), "fold")
          check_button = Button(300, 650, 100, 50, "Check/Call", (0, 255, 0), (0, 200, 0), "check")
          raise_button = Button(450, 650, 100, 50, "Raise", (0, 0, 255), (0,0,200), "raise")
          buttons = [fold_button, check_button, raise_button]
          #player option buttons

          one_button = Button(275, 700, 75, 30, "1", (255, 0, 0), (200, 0, 0), 1)
          five_button = Button(325, 700, 75, 30, "5", (255, 0, 0), (200, 0, 0), 5)
          twenty_button = Button(375, 700, 75, 30, "20", (255, 0, 0), (200, 0, 0), 20)
          fifty_button = Button(425, 700, 75, 30, "50", (255, 0, 0), (200, 0, 0), 50)
          done_button = Button(475, 700, 75, 30, "Done", (255, 0, 0), (200, 0, 0), 0)
          values_buttons = [one_button, five_button, twenty_button, fifty_button, done_button]
          #buttons for values


          
          
          player_turn_screen = font.render((f"it is {player.name}'s turn"), True, (255,255,255))
          player_counter_screen = font.render((f"you have {player.counter} chips"), True, (255,255,255))
          pot_screen = font.render((f"pot = {pot}"), True, (255,255,255))
          current_bet_screen = font.render((f"current bet = {player.current_bet}"), True, (255,255,255))
          min_bet_screen = font.render((f"min bet = {to_bet}"), True, (255,255,255))
          victor_screen = font.render(f"{winners[0].name} has won", True, (255,255,255))
          valid_option_screen = font.render(f"please choose a valid option", True, (255,255,255))
          check_screen = font.render(f"{player.name} has checked", True, (255,255,255))
          fold_screen = font.render(f"{player.name} has folded", True, (255,255,255))
          
          
          win.fill((33,124,66))
          
          


          pygame.draw.rect(win, (255,255,255), (440, 90, 300, 140), 2)
          win.blit(title_screen, (450,100))
          win.blit(buy_in_screen, (450, 120))
          win.blit(aces_count_screen, (450, 140))
          win.blit(sequence_screen, (450, 160))
          win.blit(counters_screen, (450, 180))
          win.blit(order_screen, (450, 200))
          pygame.display.update()



          counters = store.get("chips")
          win.blit(counters, (100,400))


          win.blit(player_turn_screen, (100,120))
          win.blit(player_counter_screen, (75,400))
          win.blit(pot_screen, (100,140))
          win.blit(current_bet_screen, (100,160))
          win.blit(min_bet_screen, (100,180))
          
          backside = store.get("backside")
          x = 200
          pygame.display.update()
          for i in range(5):
            win.blit(backside, (x, 250))
            x += 50

          draw_hand(win, player, 250, 450, 200, 250, store, round_num)

          pygame.display.update()

          
          choice = wait(win, font, buttons)
          
          
          pygame.display.update()

          if choice == "fold":
            winners.remove(player)
          #removes player from winners list
            win.blit(fold_screen, (500,500))
            pygame.display.update()
            sleep(1)
            if len(winners) == 1:
              win.blit(victor_screen, (500,500))
              pygame.display.update()
              sleep(1)
              winners[0].counter += pot
              sleep(2)
              play = False
              break
              #if this results in one player left they win

          elif choice == "check":
            player.counter -= to_bet
            #removes what the player has to bet from their counters
            player.current_bet += to_bet
            #increases their current bet
            pot += to_bet
            player_responses[player] = True
            #players has had a turn
            win.blit(check_screen, (500,600))
            pygame.display.update()
            sleep(1)
            

          elif choice == "raise":
            while True:
              while True:
                
                cumulative = wait(win, font, values_buttons)
                amount += cumulative
                pygame.display.update()
                if cumulative == 0:
                  break
              #what the player wants to raise by
             

              if amount > player.counter or amount < to_bet:
                print("you don't have enough counters")
                continue
                #keeps looping until the user puts in the right input
              else:
                break
              
            raise_amount = amount - player.current_bet
            #how much the player raised by
            player.counter -= raise_amount
            player.current_bet += raise_amount
            #removes this from the players counters but adds to current bet
            pot += amount
            high_bet = player.current_bet
            #makes the high bet the raise
            player_responses = {p: False for p in group if p in winners}
            #resets all responses  
            player_responses[player] = True
            #player has responded to their own move though
            all_matched = False
            #loops once more so everyone can react to bet
            player.move = True
            raise_screen = font.render(f"{player.name} has raised by {amount}", True, (255,255,255))
            win.blit(raise_screen, (500,500))
            pygame.display.update()
            sleep(1)
            


          else:
            win.blit(valid_option_screen, (500,500))
            pygame.display.update()
            sleep(1)
            continue

          win.blit(player_turn_screen, (100,100))
          win.blit(player_counter_screen, (150,400))
          win.blit(pot_screen, (100,140))
          win.blit(current_bet_screen, (100,160))
          win.blit(min_bet_screen, (100,180))
          
          pygame.display.update()
          


        if all(player.current_bet == high_bet for player in winners):
          all_matched = True
        #checks that each player has matched the raise to move the game on



      if len(winners) > 1:
        if round_num == 2:
          round_num += 3
          
          #shows the flop cards being revealed
          #3 cards shown only happens in the second round
        else:
          round_num += 1
          #only shows 1 additional card otherwise

        

round()








