
class Dialogue:
    text = [["Calikka", "Funny Dialogue", "Excited"], ["Generic_NPC", "Ridiculously long text spam blerb thing", "Default"]]
    dialogue_ID = 0
    options = [["Yes", "Quest", "FreeLoot"], ["No", "End", "None"], ["What", "Dialogue", "0"]]

    def __init__(self, dialogue_ID):
        if (dialogue_ID == 0):
            self.text = [["Calikka", "Funny Dialogue", "Excited"], ["Generic_NPC", "Ridiculously long text spam blerb thing", "Default"]]