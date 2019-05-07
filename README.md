# Flowerbot
A simple chatbot in python.

This is a simple chatbot that is meant for ordering flowers.
The bot is capable of making multiple orders of different flower types, colors and amounts, which can be changed later.
At the end of the conversation, the bot repeats the list of orders the user made

The current flower types are tulips and roses, the colors are red, green blue and white, and any amount is possible 

# How to use
The bot needs python 3.5 or higher to work.
in your command line, open the main.py file using python, the script will then accept your input.
type bye or exit to stop the conversation (bot does not exit automatically)

# How it works
Behind the scenes, flowerbot is a simple state machine, that keeps track of where in the process of ordering it is.
The state is changed based on what the user inputs 
The bot keeps the current order, as well as a list of previous orders.
