from random import choice
import json

#Load JSON data from lepak_locations.json
# "r" opens file in read mode
with open('lepak_locations.json', 'r', encoding='utf-8') as file:
    lepak_locations = json.load(file)

#Pre-generated message list
Reply_List = [
    "{} seems like a great option for today!",
    "How about checking out {}? It's a great place to chill!",
    "{} could be fun spot to rest and relax!",
    "I heard {} is a great place to go!",
    "Maybe try {}? It's a popular choice for some people!",
    "If you're looking for something to just lepak, {} is one of the recommended picks!",
    "{} sounds like a cozy place to just chill!",
    "I would suggest going to {}!",
    "{} is a good spot!",
    "{} is a great place to relax!"
]

def handle_response(text:str) -> str:
    processed: str = text.lower().strip()

    if 'hello' in processed:
        return 'Hey there! Enter a town you want to lepak and I\'ll recommend a spot!'
    
    if 'idk' in processed:
        return 'Just choose a town you\'re at right now or want to go and I\'ll recommend a spot!'
    
    words = processed.split() # Split the input into words
    
    # Extract town and category (if any input provided)
    town = words[0]
    category = words[1] if len(words) > 1 else None

    if town in lepak_locations:
        categories =lepak_locations[town] # Retrieve available categories for input town

        # If user input a category, check if category is valid
        if category and category in categories:
            place = choice(categories[category]) # Random place is chosen within that specified category

        else:
            # Pick random category and a place from that category
            random_category = choice(list(categories.keys())) # A spot is chosen at random depending on the selected town
            place = choice(categories[random_category])


        message = choice(Reply_List).format(place) # Format with a pre-written reply
        return message

    return choice(["Im not sure where that is, my developer half fuck my code so my process is a bit limited.",
                   'I do not understand what you wrote....'])
