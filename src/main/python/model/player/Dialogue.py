
class Dialogue:
    text = [["Calikka", "Funny Dialogue", "Excited"], ["Generic_NPC", "Ridiculously long text spam blerb thing", "Default"]]
    dialogue_ID = 0
    options = [["Yes", "Quest", "FreeLoot"], ["No", "End", "None"], ["What", "Dialogue", "0"]]

    def __init__(self, dialogue_ID):
        if (dialogue_ID == 0):
            self.text = [["Calikka", "Funny Dialogue", "Excited"], ["Generic_NPC", "Ridiculously long text spam blerb thing", "Default"]]
            self.options = [["Yes", "Quest", "FreeLoot"], ["No", "End", "None"], ["What", "Dialogue", "0"]]
        if (dialogue_ID == 1):
            self.text = [["Calikka", "test", "Excited"], ["Generic_NPC", "test2", "Default"]]
            self.options = []
        if (dialogue_ID == 2):
            self.text = [["Generic_NPC", "default", "Default"], ["Generic_NPC", "bozo", "Default"]]
            self.options = []