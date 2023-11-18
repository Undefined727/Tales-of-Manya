import json

class Dialogue:
    text = [["Calikka", "Funny Dialogue", "Excited"], ["Generic_NPC", "Ridiculously long text spam blerb thing", "Default"]]
    dialogue_ID = 0
    options = [["yes", "Quest", 1], ["Alright", "End", "None"], ["What", "Dialogue", "0"]]

    def __init__(self, dialogue_ID):
        self.dialogue_ID = dialogue_ID
        file = open("dialogue/dialogue.json", 'r')
        data = json.load(file)

        for dialogueEntry in data:
            if (dialogueEntry['id'] == dialogue_ID):
                self.text = dialogueEntry['text']
                self.options = dialogueEntry['options']