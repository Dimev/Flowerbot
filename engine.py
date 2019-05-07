import random
import re

# conversation manager
# calls the conversation class when called
# conversation takes input mem and output mem as inputs
# should return an array of responses
class Manager:
    def __init__(self, conversation, mem_size = 8, inputmem = [], outputmem = []):
        self.conversation = conversation
        self.mem_size = 8
        self.inputmem = inputmem
        self.outputmem = outputmem

    def __call__(self, input_data):
        # track inputs
        self.inputmem.insert(0, input_data)
        # remove last element if the array is longer than the memory
        if len(self.inputmem) > self.mem_size:
            self.inputmem.pop()
        # call the conversation class
        responses = self.conversation(self.inputmem, self.outputmem)
        # add to the output mem
        for response in responses:
            self.outputmem.insert(0, response)
            # remove last element if the array is longer than the memory
            if len(self.outputmem) > self.mem_size:
                self.outputmem.pop()
        # return the response array
        return responses
