# simple demo for ordering flowers
import re

# flower types (there are probably more types)
FLOWER_NONE = 0
FLOWER_TULIP = 1
FLOWER_ROSE = 2

# flower colors
COLOR_NONE = 0
COLOR_RED = 1
COLOR_GREEN = 2
COLOR_BLUE = 3
COLOR_WHITE = 4
# states
STATE_NONE = 0
STATE_NEW = 1 # not used
STATE_TYPE = 2
STATE_COLOR = 3
STATE_AMOUNT = 4
STATE_CONFIRM = 5
STATE_COMPLETE = 6
# states for editing current flower
STATE_EDIT = 7
STATE_EDIT_TYPE = 8
STATE_EDIT_COLOR = 9
STATE_EDIT_AMOUNT = 10
# STATE_EDIT_CONFIRM = 11
STATE_EDIT_ORDER = 12
STATE_COMPLETE_ORDER = 13
# adress
STATE_ADRESS = 14
STATE_ADRESS_CONFIRM = 15


class Bot:

    def __init__(self):
        self.type = 0
        self.state = 0
        self.flowers = []
        self.current = {}

    def save(self, path):
        pass

    def load(self, path):
        pass

    def __call__(self, inputmem, outputmem):
        # get the most recent input
        utterance = inputmem[0]

        # general info about the flowers
        # types
        if "what kind" in utterance or "types" in utterance:
            return ["We sell roses and tulips"]
        # colors
        if "what color" in utterance or "colors" in utterance:
            return ["We have all flowers in red, green, blue and white"]
        # if the conversation started
        if self.state == STATE_NONE:
            self.state = STATE_TYPE
            return [
            "Hello, I'm the flowerbotinator 9000, I sell flowers",
            "Let's get started, I'll ask what type and color you want.",
            "After you sepcified an order (type, color amount), you can always edit it",
            "So, What type of flower do you want?"
            ]
        # set type
        if self.state == STATE_TYPE:
            # extract the type from the utterance
            if "tulip" in utterance:
                self.current["type"] = FLOWER_TULIP
                self.state = STATE_COLOR
                return ["What color do you want your tulip to be?"]
            elif "rose" in utterance:
                self.current["type"] = FLOWER_ROSE
                self.state = STATE_COLOR
                return ["What color do you want your rose to be?"]
            # otherwise
            else:
                return ["Please specify your flower type, we only sell roses and tulips"]
        # set the color
        if self.state == STATE_COLOR:
            # extract the color info
            if "red" in utterance:
                self.current["color"] = COLOR_RED
                self.state = STATE_AMOUNT
            elif "blue" in utterance:
                self.current["color"] = COLOR_BLUE
                self.state = STATE_AMOUNT
            elif "green" in utterance:
                self.current["color"] = COLOR_GREEN
                self.state = STATE_AMOUNT
            elif "white" in utterance:
                self.current["color"] = COLOR_WHITE
                self.state = STATE_AMOUNT
            else:
                self.current["color"] = COLOR_NONE

            # build reply
            reply = "How many * do you want?".replace("*", [
                    "R ", "red ", "green ", "blue ", "white "
                ][self.current["color"]] + [
                    "R", "tulips", "roses"
                ][self.current["type"]])
            # if the reply contains an R, something went wrong, thus reply a fail answer
            if "R" in reply:
                reply = "We don't sell that color, we only sell red, green, blue and white"
            return [reply]

        # get the amount
        if self.state == STATE_AMOUNT:
            # convert the input to an int
            amount = 1
            try:
                # first remove all numeric characters, then get the integer
                amount = int(re.sub("[^0-9]", "", utterance))
            except:
                # if the converstion failed, give an explanation
                return ['Please only specify the amount, such as "10" or "1".']
            # continue
            self.current["amount"] = amount
            # build reply
            # data is amount color type
            data = str(amount) + " " + [
                    "R ", "red ", "green ", "blue ", "white "
                ][self.current["color"]] + ([
                    "R", "tulips", "roses"
                ][self.current["type"]] if amount > 1 else [
                    "R", "tulip", "rose"
                ][self.current["type"]])
            reply = "So *, is that correct?".replace("*", data)
            self.state = STATE_CONFIRM
            if amount == 69: # nice
                return ["Nice", reply]
            return [reply]

        if self.state == STATE_CONFIRM:
            # if the order is correct
            if "yes" in utterance:
                self.state = STATE_COMPLETE
                # add flower
                self.flowers.append(self.current)
                self.current = {}
                return ["Do you want anything else?"]
            else:
                self.state = STATE_EDIT
                return ["What would you like to change? (type, color or amount)"]

        # complete the order
        if self.state == STATE_COMPLETE:
            # if the order is complete
            if "no" in utterance:
                # summarize order
                summary = ["You ordered: "]
                for count, i in enumerate(self.flowers):
                    flower = str(count + 1) + ": " + str(i["amount"]) + " " + [
                            "R ", "red ", "green ", "blue ", "white "
                        ][i["color"]] + ([
                            "R", "tulips", "roses"
                        ][i["type"]] if i["amount"] > 1 else [
                            "R", "tulip", "rose"
                        ][i["type"]])
                    summary.append(flower)
                # complete summary
                summary.append("Is that correct?")
                self.state = STATE_COMPLETE_ORDER
                return summary
            else:
                self.state = STATE_TYPE
                return ["Ah, what type of flower do you want?"]

        # if the order is edited
        if self.state == STATE_COMPLETE_ORDER:
            # if the order is correct
            if "yes" in utterance:
                self.state = STATE_ADRESS
                return ["Where should we send the flowers to?"]
            else:
                self.state = STATE_EDIT_ORDER
                return ["What order do you want to change"]

        # get the adress
        if self.state == STATE_ADRESS:
            # confirm state
            self.state = STATE_ADRESS_CONFIRM
            # simply return the adress
            return ["Sending the flowers to: " + utterance, "Is that correct?"]

        # confirm the adress
        if self.state == STATE_ADRESS_CONFIRM:
            # if yes
            if "yes" in utterance:
                return ["Thank you for shopping!"]
            else:
                self.state = STATE_ADRESS
                return ["What is the adress you want the flowers to be delivered to?"]

        # if an order should be changed
        if self.state == STATE_EDIT_ORDER:
            # get the order to edit
            order = int(re.sub("[^0-9]", "", utterance))
            # reset the current order
            self.current = self.flowers[order-1]
            # remove the order
            self.flowers.pop(order-1)
            # set the state to edit
            self.state = STATE_EDIT
            # get the part to edit
            return ["What do you want to change about this order?"]

        # edit
        if self.state == STATE_EDIT:
            # get the edit type
            if "type" in utterance:
                self.state = STATE_EDIT_TYPE
                return ["What type of flower do you want it to be?"]
            elif "color" in utterance:
                self.state = STATE_EDIT_COLOR
                return ["What color do you want the flower to be?"]
            else:
                self.state = STATE_EDIT_AMOUNT
                return ["How many do you want then?"]

        # type
        if self.state == STATE_EDIT_TYPE:
            # set the type
            if "tulip" in utterance:
                self.current["type"] = FLOWER_TULIP
                self.state = STATE_CONFIRM
            elif "rose" in utterance:
                self.current["type"] = FLOWER_ROSE
                self.state = STATE_CONFIRM
            else:
                return ["We don't have that type, we only have roses and tulips"]
            # build answer
            data = str(self.current["amount"]) + " " + [
                    "R ", "red ", "green ", "blue ", "white "
                ][self.current["color"]] + ([
                    "R", "tulips", "roses"
                ][self.current["type"]] if self.current["amount"] > 1 else [
                    "R", "tulip", "rose"
                ][self.current["type"]])
            reply = "So *, is that correct?".replace("*", data)
            return [reply]

        # color
        if self.state == STATE_EDIT_COLOR:
            # extract the color info
            if "red" in utterance:
                self.current["color"] = COLOR_RED
                self.state = STATE_CONFIRM
            elif "blue" in utterance:
                self.current["color"] = COLOR_BLUE
                self.state = STATE_CONFIRM
            elif "green" in utterance:
                self.current["color"] = COLOR_GREEN
                self.state = STATE_CONFIRM
            elif "white" in utterance:
                self.current["color"] = COLOR_WHITE
                self.state = STATE_CONFIRM
            else:
                return ["We don't have that color, we only have red, green, blue and white"]
            # build answer
            data = str(self.current["amount"]) + " " + [
                    "R ", "red ", "green ", "blue ", "white "
                ][self.current["color"]] + ([
                    "R", "tulips", "roses"
                ][self.current["type"]] if self.current["amount"] > 1 else [
                    "R", "tulip", "rose"
                ][self.current["type"]])
            reply = "So *, is that correct?".replace("*", data)
            return [reply]

        # amount
        if self.state == STATE_EDIT_AMOUNT:
            # convert the input to an int
            amount = 1
            try:
                amount = int(re.sub("[^0-9]", "", utterance))
            except:
                # if the converstion failed, give an explanation
                return ['Please only specify the amount, such as "10" or "1".']
            # continue
            self.current["amount"] = amount
            self.state = STATE_CONFIRM
            # build answer
            data = str(amount) + " " + [
                    "R ", "red ", "green ", "blue ", "white "
                ][self.current["color"]] + ([
                    "R", "tulips", "roses"
                ][self.current["type"]] if amount > 1 else [
                    "R", "tulip", "rose"
                ][self.current["type"]])
            reply = "So *, is that correct?".replace("*", data)
            if amount == 69: # nice
                return ["Nice", reply]
            return [reply]
