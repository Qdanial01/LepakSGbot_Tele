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
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'
    
    if 'how are you' in processed:
        return 'I am good!'
    
    return 'I do not understand what you wrote....'
