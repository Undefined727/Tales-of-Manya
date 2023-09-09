from view.visualentity.Paragraph import Paragraph
from view.visualentity.TextEntity import TextEntity
from view.visualentity.ImageButton import ImageButton
from view.visualentity.HoverShapeButton import HoverShapeButton
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.ShapeEntity import ShapeEntity
from view.visualentity.VisualEntity import VisualEntity
from model.player.Dialogue import Dialogue

class VisualNovel(VisualEntity):
    paragraph:Paragraph
    continueButton:ImageButton
    frame:ImageEntity
    backgroundBox:ShapeEntity
    dialogue:Dialogue
    name:TextEntity
    currentTextPosition:int
    text:str
    isShowingOptions:bool
    optionButtons:list
    optionParagraphs:list


    def __init__(self, name = "Default_Text", isShowing = True, xPosition = 0, yPosition = 0, width = 0, height = 0, tags = [], dialogue = 0):
        super().__init__(name, isShowing, xPosition, yPosition, width, height, tags)
        self.currentTextPosition = 0
        self.dialogue = Dialogue(dialogue)
        self.text = self.dialogue.text[self.currentTextPosition][1]
        self.isShowingOptions = False
        self.optionParagraphs = []
        self.optionButtons = []
        self.frame = ImageEntity("vn_frame", True, xPosition, yPosition, width, height/3, tags, "visual_novel_frame.png")
        self.backgroundBox = ShapeEntity("vn_background", True, xPosition, yPosition + height/4, width, 3*height/4, tags, (0, 0, 255, 160), False, "rectangle")
        self.paragraph = Paragraph("text", True, xPosition + width/5, yPosition + 6*height/16, 0.4*width, 0.55*height, tags, self.text, "mono", 24)
        self.paragraph.align = "Left"
        self.continueButton = ImageButton("continue_button", True, xPosition + 0.85*width, yPosition + 6*height/16, width/10, height/8, tags, "change_active_right.png", "continueText")
        


    def updateDialogue(self, dialogueID):
        if(self.isShowingOptions): return
        self.currentTextPosition = 0
        self.dialogue = Dialogue(dialogueID)
        self.text = self.dialogue.text[self.currentTextPosition][1]
        self.updateText(self.text)

    def updateText(self, text, font = None, fontSize = None, fontColor = None, highlightColor = None):
        self.text = text
        self.paragraph.updateText(text, font, fontSize, fontColor, highlightColor)

    def continueText(self):
        self.currentTextPosition += 1
        if (self.currentTextPosition < len(self.dialogue.text)):
            self.updateText(self.dialogue.text[self.currentTextPosition][1])
            return "Text"
        else:
            if (len(self.dialogue.options) > 0 and not self.isShowingOptions):
                self.backgroundBox.reposition(self.xPosition, self.yPosition + self.height/4 - 3*self.height/4)
                self.frame.reposition(self.xPosition, self.yPosition - 3*self.height/4)
                self.continueButton.reposition(self.xPosition + 0.85*self.width, self.yPosition - 3*self.height/4 + 6*self.height/16)
                self.paragraph.reposition(self.xPosition + self.width/5, self.yPosition - 3*self.height/4 + 6*self.height/16)
                self.backgroundBox.resize(self.width, 6*self.height/4)
                self.isShowingOptions = True
                self.optionParagraphs = []
                counter = -1
                for option in self.dialogue.options:
                    counter += 1
                    height = self.yPosition + 6*self.height/16 + counter*((3*self.height/5)/len(self.dialogue.options))
                    optionParagraph = Paragraph("option", True, self.xPosition + self.width/5, height, 0.4*self.width, ((3*self.height/5)/len(self.dialogue.options)), self.tags, ">> " + option[0], "mono", 24)
                    optionParagraph.align = "Left"
                    optionParagraph.scaled = True
                    optionParagraph.updateText(optionParagraph.text)
                    self.optionParagraphs.append(optionParagraph)
                    optionButton = HoverShapeButton("option_button", True, self.xPosition, height, 0.4*self.width, ((3*self.height/5)/len(self.dialogue.options)), self.tags, (0, 0, 0, 0), (0, 80, 255, 190), "rectangle", "textOption", [option[1], option[2]], True)
                    self.optionButtons.append(optionButton)
                return "Options"
            elif (self.isShowingOptions): 
                self.isShowingOptions = False
                self.optionParagraphs = []
                self.reposition(self.xPosition, self.yPosition)
                self.resize(self.width, self.height)
                return "Finished"
            else: return "Finished"

    
    def resize(self, width, height):
        self.width = width
        self.height = height
        self.frame.resize(width, height/3)
        self.backgroundBox.resize(width, 3*height/4)
        self.paragraph.resize(0.4*width, 0.55*height)
        self.continueButton.resize(width/10, height/8)
    
    def reposition(self, xPosition, yPosition):
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.frame.reposition(xPosition, yPosition)
        self.backgroundBox.reposition(xPosition, yPosition + self.height/4)
        self.paragraph.reposition(xPosition + self.width/5, yPosition + 6*self.height/16)
        self.continueButton.reposition(xPosition + 0.85*self.width, yPosition + 6*self.height/16)
    
    def scale(self, screenX, screenY):
        self.resize(self.width, self.height)
        self.reposition(self.xPosition, self.yPosition)
        self.frame.scale(screenX, screenY)
        self.backgroundBox.scale(screenX, screenY)
        self.paragraph.scale(screenX, screenY)
        self.continueButton.scale(screenX, screenY)
        self.resize(self.width*screenX, self.height*screenY)
        self.reposition(self.xPosition*screenX, self.yPosition*screenY)
        self.updateText(self.text)


    @staticmethod
    def createFrom(json_object):
        newObject = VisualNovel()
        newObject.__dict__.update(json_object)
        newObject.frame = ImageEntity("vn_frame", True, newObject.xPosition, newObject.yPosition, newObject.width, newObject.height/3, newObject.tags, "text_background.png")
        newObject.backgroundBox = ShapeEntity("vn_background", True, newObject.xPosition, newObject.yPosition + newObject.height/4, newObject.width, 3*newObject.height/4, newObject.tags, (0, 255, 0, 100), False, "rectangle")
        newObject.paragraph = Paragraph("text", True, newObject.xPosition + newObject.width/5, newObject.yPosition + 6*newObject.height/16, 0.4*newObject.width, 0.55*newObject.height, newObject.tags, newObject.text, "mono", 24)
        newObject.paragraph.align = "Left"
        newObject.continueButton = ImageButton("continue_button", True, newObject.xPosition + 0.85*newObject.width, newObject.yPosition + 6*newObject.height/16, newObject.width/10, newObject.height/8, newObject.tags, "change_active_right.png", "continueText")
        return newObject