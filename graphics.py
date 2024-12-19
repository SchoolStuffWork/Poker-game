import pygame
import os
pygame.init()




def load_image():
    long_values = [2,3,4,5,6,7,8,9,10, "jack", "queen", "king", "ace"]
    long_suits = ["hearts", "diamonds", "clubs", "spades"]
    #the official names for the values and suits
    base_path = os.path.join(os.getcwd(), "PNG-cards-1.3")
    #the folder name which contains all the cards
    store = {}
    for suit in long_suits:
        for value in long_values:
            image_path = os.path.join(base_path, f"{value}_of_{suit}.png")
            #finds the actual card png names
            #has to be in this format
            
                   
            if isinstance(value,str) and value in ["jack", "queen", "king", "ace"]:
                name = f"{suit[0].upper()}{value[0].upper()}"
                #if the value is a picture card
                #names the card by it's suit and first letter capitol
            else:
                name = f"{suit[0].upper()}{value}"
                #if it's just a normal card
                #names the card by it's suit and value

                #e.g D8 for 8 of diamonds
            
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (100,150))
            #loads and makes all the images the same size
            store[name] = image
            #appends them to a dictionary
    backside = pygame.image.load(os.path.join(base_path, "playing_card_back.png"))
    backside = pygame.transform.scale(backside, (100,150))
    store["backside"] = backside

    chips = pygame.image.load("poker_counters.png")
    chips = pygame.transform.scale(chips, (100,150))
    store["chips"] = chips
    #does the same for the back od the card

    return store

store = load_image()
