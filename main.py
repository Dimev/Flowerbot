import engine
import flowerbot

print("RobotEngine v0.0.1")
print("written by Dimas Leenman")
print("This is a simple demo of a chatbot")
print("say bye or exit to stop the conversation")


# make a bot
bot = flowerbot.Bot()

# conversation manager
manager = engine.Manager(bot, mem_size = 32)

print("="*69) # nice

while True:
    # get the user input
    utterance = input("You: ").lower()
    # check if the conversation should stop
    if utterance == "exit" or utterance == "bye":
        print("Bot: Bye!")
        break
    else:
        responses = manager(utterance)
        for i in responses:
            print("Bot: " + i)
            
