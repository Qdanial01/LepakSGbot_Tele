from random import choice
import json

#Load JSON data from lepak_locations.json and replies.json
# "r" opens file in read mode
with open('lepak_locations.json', 'r', encoding='utf-8') as file:
    lepak_locations = json.load(file)

with open('replies.json', 'r', encoding='utf-8') as file:
    replies = json.load(file)



def handle_response(text:str) -> str:
    processed: str = text.lower().strip()

    if 'hello' in processed:
        return 'Hey there! Enter a town you want to lepak and I\'ll recommend a spot!'
    
    if 'idk' in processed:
        return 'Just choose a town you\'re at right now or want to go and I\'ll recommend a spot!'
    
    words = processed.split() # Split the input into words
    
    # Handle towns with more than one word
    town = None
    category = None

    #Tries matching town first
    for i in range(len(words)):
        possible_town = ' '.join(words[:i+1]) #This joins words from the start to i-th word
        if possible_town in lepak_locations:
            town = possible_town
            category = ' '.join(words[i+1:]) #Takes the remaining words as category
            break

    if not town:
        return choice(['I don\'t think I know places for that town','Please try another town', 'I don\'t recognize that town. Please try again!',
                       'Not sure where that is.... you could check in /towns for the list of places I support!','Not sure about spots for that place.. maybe try something else?'])
    
    categories = lepak_locations[town] # Retrieve available categories for the input town

        # If user input a category, check if category is valid
    if category and category in categories:
        place = choice(categories[category]) # Random place is chosen within that specified category

    else:
            # Pick random category and a place from that category
            random_category = choice(list(categories.keys())) # A spot is chosen at random depending on the selected town
            place = choice(categories[random_category])


    message = choice(replies).format(place) # Format with a pre-written reply
    
    return message


