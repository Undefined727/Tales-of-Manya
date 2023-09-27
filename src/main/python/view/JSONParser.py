import json as JSON
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.ShapeEntity import ShapeEntity
from view.visualentity.TextEntity import TextEntity
from view.visualentity.Paragraph import Paragraph
from view.visualentity.VisualNovel import VisualNovel
from view.visualentity.ShapeButton import ShapeButton
from view.visualentity.HoverShapeButton import HoverShapeButton
from view.visualentity.ScrollBar import ScrollBar
from view.visualentity.ImageButton import ImageButton
from view.visualentity.CombatCharacterEntity import CombatCharacterEntity
from view.visualentity.InventoryCharacterEntity import InventoryCharacterEntity

def loadJson(address, screenX, screenY, lists):
    visualEntities = lists[0]
    buttons = lists[1]
    if (len(lists) > 2): 
        partyVisuals = lists[2] 
        party = lists[3]
    file = open("src/main/python/screens/" + address, 'r')
    data = JSON.load(file)
    for item in data:
        entity = None
        if item["entityType"] == "Image":
            entity = ImageEntity.createFrom(item)
        elif item["entityType"] == "Shape":
            entity = ShapeEntity.createFrom(item)
        elif item["entityType"] == "Text":
            entity = TextEntity.createFrom(item)
        elif item["entityType"] == "Paragraph":
            entity = Paragraph.createFrom(item)
        elif item["entityType"] == "VisualNovel":
            entity = VisualNovel.createFrom(item)
        elif item["entityType"] == "Button":
            entity = ShapeButton.createFrom(item)
        elif item["entityType"] == "ImageButton":
            entity = ImageButton.createFrom(item)
        elif item["entityType"] == "ShapeButton":
            entity = ShapeButton.createFrom(item)
        elif item["entityType"] == "HoverShapeButton":
            entity = HoverShapeButton.createFrom(item)
        elif item["entityType"] == "ScrollBar":
            entity = ScrollBar.createFrom(item)
        elif item["entityType"] == "CharacterEntityCoords":
            if (item["name"] == "Character1"): index = 0
            elif (item["name"] == "Character2"): index = 1
            elif (item["name"] == "Character3"): index = 2
            else: index = 0
            entity = CombatCharacterEntity.createFrom(item, party[index])
        elif item["entityType"] == "InventoryCharacterCoords":
            index = 0
            entity = InventoryCharacterEntity.createFrom(item, party[index])



        if not (entity is None):
            entity.scale(screenX, screenY)
            if (item["entityType"] == "ImageButton" or item["entityType"] == "ShapeButton" or item["entityType"] == "HoverShapeButton"): 
                buttons.append(entity)
                visualEntities.append(entity.buttonVisual())
            elif(item["entityType"] == "ScrollBar"):
                buttons.append(entity.button)
                visualEntities.append(entity)
            elif(item["entityType"] == "VisualNovel"):
                buttons.append(entity.continueButton)
                visualEntities.append(entity)
            elif(item["entityType"] == "CharacterEntityCoords" or item["entityType"] == "InventoryCharacterCoords"): 
                partyVisuals[index] = entity
            else: visualEntities.append(entity)