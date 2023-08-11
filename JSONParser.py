import json as JSON
from model.visualentity.ImageEntity import ImageEntity
from model.visualentity.ShapeEntity import ShapeEntity
from model.visualentity.TextEntity import TextEntity
from model.visualentity.ShapeButton import ShapeButton
from model.visualentity.ImageButton import ImageButton
from model.visualentity.CombatCharacterEntity import CharacterEntities
from model.visualentity.InventoryCharacterEntity import InventoryCharacterEntity

def loadJson(address, screenX, screenY, lists):
    visualEntities = lists[0]
    buttons = lists[1]
    if (len(lists) > 2): 
        partyVisuals = lists[2] 
        party = lists[3]
    file = open("screens/" + address, 'r')
    data = JSON.load(file)
    for item in data:
        entity = None
        if item["entityType"] == "Image":
            entity = ImageEntity.createFrom(item)
        elif item["entityType"] == "Drawing":
            entity = ShapeEntity.createFrom(item)
        elif item["entityType"] == "Text":
            entity = TextEntity.createFrom(item)
        elif item["entityType"] == "Button":
            entity = ShapeButton.createFrom(item)
        elif item["entityType"] == "ImageButton":
            entity = ImageButton.createFrom(item)
        elif item["entityType"] == "ShapeButton":
            entity = ShapeButton.createFrom(item)
        elif item["entityType"] == "CharacterEntityCoords":
            if (item["name"] == "ActiveCharacter"): index = 1
            elif (item["name"] == "InactiveCharacter1"): index = 0
            elif (item["name"] == "InactiveCharacter2"): index = 2
            else: index = 0
            entity = CharacterEntities.createFrom(item, party[index])
        elif item["entityType"] == "InventoryCharacterCoords":
            index = 0
            entity = InventoryCharacterEntity.createFrom(item, party[index])
            print(entity)



        if not (entity is None):
            entity.scale(screenX, screenY)
            if (item["entityType"] == "ImageButton" or item["entityType"] == "ShapeButton"): 
                buttons.append(entity)
                print(entity.buttonVisual().name)
                visualEntities.append(entity.buttonVisual())
            elif(item["entityType"] == "CharacterEntityCoords" or item["entityType"] == "InventoryCharacterCoords"): partyVisuals[index] = entity
            else: visualEntities.append(entity)