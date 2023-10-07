import pygame, numpy, math, os, random, json, copy
from view.visualentity.Tag import Tag
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.ShapeEntity import ShapeEntity
from view.visualentity.TextEntity import TextEntity
from view.visualentity.ShapeButton import ShapeButton
from view.visualentity.ImageButton import ImageButton
from view.visualentity.DynamicStatEntity import DynamicStatEntity
from view.visualentity.CombatCharacterEntity import CombatCharacterEntity
from model.skill.Skill import Skill
from model.character.Character import Character
from model.item.Item import Item
from view.visualentity.CombatEnemyEntity import CombatEnemyEntity
from model.player.Player import Player
from view.displayHandler import displayEntity
from view.JSONParser import loadJson
from model.database.DBElementFactory import DBElementFactory


visualEntities = []
partyVisuals = []
buttons = []
quit = False
newSceneData = {}

databaseFactory = DBElementFactory()

currentSceneData:list
playerData:Player
screen:pygame.surface


def combatButton():
    global quit
    global nextScreen
    quit = True
    nextScreen = "Combat"

def openWorld(map):
    global quit
    global newSceneData
    global screen
    quit = True
    newSceneData = {"screenData": screen, "curScreen": "Open World", "map": map, "playerData": playerData, "enemyData": currentSceneData.get("enemies", None)}

def returnToMapButton():
    openWorld(currentSceneData["map"])


def refreshScreen(screen):
    # Fill the background
    global visualEntities
    for entity in visualEntities:
         if entity.isShowing:
            displayEntity(entity, screen)
    for entity in partyVisuals:
        ls = entity.getItems()
        for item in ls:
            if item.isShowing:
                displayEntity(item, screen)

    pygame.display.flip()



def loadInventory(screenData):
    global visualEntities
    global partyVisuals
    global currentSceneData
    global playerData
    global screen
    global quit
    global newSceneData
    quit = False
    currentSceneData = screenData
    playerData = currentSceneData["playerData"]
    screen = currentSceneData["screenData"]
    screenX, screenY = screen.get_size()
    attachedItem = None
    attachedItemEquipped = None
    
    visualEntities = []
    partyVisuals = [CombatCharacterEntity(playerData.party[0])]
    buttons = []
    loadJson("inventoryScreen.json", screenX, screenY, [visualEntities, buttons, partyVisuals, playerData.party])

    activeCharacter = 1

    currInventory = playerData.inventory.getItems()
    counter = 0
    for slot in currInventory:
        slotBackground = ImageEntity(f"InventorySlot{counter}", True, 0.02 + counter*0.07, 0.15, 0.06, 0.06*screenX/screenY, [], f"inventorySlotBackground.png")
        slotImage = ImageEntity(f"InventorySlotBackground{counter}", True, 0.02 + counter*0.07, 0.15, 0.06, 0.06*screenX/screenY, [], f"items/{slot.item.getPath()}")
        slotNumber = TextEntity(f"InventorySlotCount{counter}", True, 0.065 + counter*0.07, 0.24, 0.03, 0.06, [], str(slot.count), "mono", 26)
        slotBackground.scale(screenX, screenY)
        slotImage.scale(screenX, screenY)
        slotNumber.scale(screenX, screenY)
        visualEntities.append(slotBackground)
        visualEntities.append(slotImage)
        visualEntities.append(slotNumber)
        counter += 1


    def itemClickFunction(*args):
        nonlocal attachedItem
        nonlocal attachedItemEquipped
        attachedItem = args[0][0]
        if (attachedItem == None): return
        if (len(args[0]) > 1): attachedItemEquipped = args[0][1]
        else: attachedItemEquipped = None
        attachedItemVisual.updateImg(attachedItem.img)
        attachedItemVisual.isShowing = True


    def exitButtonFunction(*args):
        leaveScreen = True
        nextScreen = "Combat"
    
    def changeCharacterFunction(*args):
        nonlocal activeCharacter
        global party
        if (args[0] == "Left"): activeCharacter = ((activeCharacter)%len(party))+1
        else: activeCharacter = ((activeCharacter-2)%len(party))+1
        updateCharacter()

    def updateCharacter():
        global visualEntities
        global party
        nonlocal activeCharacter
        for entity in visualEntities:
            if (entity.name == "CharacterName"): entity.updateText(party[activeCharacter-1].name)
            elif (entity.name == "CharacterLevel"): entity.updateText("Level " + str(party[activeCharacter-1].level))
            elif ("Equipped Item" in entity.tags):
                if (entity.name == "Helmet"):
                    if (party[activeCharacter-1].helmet == None): entity.updateImg("helmet_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].helmet.img)
                elif (entity.name == "Chestplate"):
                    if (party[activeCharacter-1].chestplate == None): entity.updateImg("chestplate_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].chestplate.img)
                elif (entity.name == "Leggings"):
                    if (party[activeCharacter-1].leggings == None): entity.updateImg("leggings_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].leggings.img)
                elif (entity.name == "Boots"):
                    if (party[activeCharacter-1].boots == None): entity.updateImg("boots_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].boots.img)
                elif (entity.name == "Accessory1"):
                    if (party[activeCharacter-1].accessory1 == None): entity.updateImg("accessory_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].accessory1.img)
                elif (entity.name == "Accessory2"):
                    if (party[activeCharacter-1].accessory2 == None): entity.updateImg("accessory_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].accessory2.img)
                elif (entity.name == "Weapon"):
                    if (party[activeCharacter-1].weapon == None): entity.updateImg("weapon_transparent.png")
                    else: entity.updateImg(party[activeCharacter-1].weapon.img)
                elif (entity.entityType == 2):
                    if (entity.name == "HelmetButton"): entity.args = [party[activeCharacter-1].helmet, "Helmet"]
                    elif (entity.name == "ChestplateButton"): entity.args = [party[activeCharacter-1].chestplate, "Chestplate"]
                    elif (entity.name == "LeggingsButton"): entity.args = [party[activeCharacter-1].leggings, "Leggings"]
                    elif (entity.name == "BootsButton"): entity.args = [party[activeCharacter-1].boots, "Boots"]
                    elif (entity.name == "Accessory1Button"): entity.args = [party[activeCharacter-1].accessory1, "Accessory1"]
                    elif (entity.name == "Accessory2Button"): entity.args = [party[activeCharacter-1].accessory2, "Accessory2"]
                    elif (entity.name == "WeaponButton"): entity.args = [party[activeCharacter-1].weapon, "Weapon"]


    partyVisuals[0].updateCharacter()
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                for entity in buttons:
                    if entity.mouseInRegion(mouse):
                        if (entity.func == "returnToMapButton"): buttonFunc = returnToMapButton
                        if (len(entity.args) == 0): buttonFunc()
                        elif (len(entity.args) == 1): buttonFunc(entity.args[0])
                        else: buttonFunc(entity.args)
                        break
        '''
            if (event.type == pygame.MOUSEBUTTONUP):
                for entity in visualEntities:
                    if (entity.entityType == 2 and "Equipped Item" in entity.tags):
                        if mouseInRegion(mouse, entity.shape, entity.xPosition, entity.yPosition, entity.width, entity.length):
                            if ("Helmet" in entity.tags and attachedItem.type == "helmet"):
                                if (party[activeCharacter-1].helmet == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].helmet == None): inventory.append(party[activeCharacter-1].helmet)   
                                party[activeCharacter-1].helmet = attachedItem
                            elif ("Chestplate" in entity.tags and attachedItem.type == "chestplate"):
                                if (party[activeCharacter-1].chestplate == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].chestplate == None): inventory.append(party[activeCharacter-1].chestplate)   
                                party[activeCharacter-1].chestplate = attachedItem
                            elif ("Leggings" in entity.tags and attachedItem.type == "leggings"):
                                if (party[activeCharacter-1].leggings == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].leggings == None): inventory.append(party[activeCharacter-1].leggings)   
                                party[activeCharacter-1].leggings = attachedItem
                            elif ("Boots" in entity.tags and attachedItem.type == "boots"):
                                if (party[activeCharacter-1].boots == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].boots == None): inventory.append(party[activeCharacter-1].boots)   
                                party[activeCharacter-1].boots = attachedItem
                            elif ("Accessory1" in entity.tags and attachedItem.type == "accessory"):
                                if (party[activeCharacter-1].accessory1 == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].accessory1 == None): inventory.append(party[activeCharacter-1].accessory1)   
                                party[activeCharacter-1].accessory1 = attachedItem
                            elif ("Accessory2" in entity.tags and attachedItem.type == "accessory"):
                                if (party[activeCharacter-1].accessory2 == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].accessory2 == None): inventory.append(party[activeCharacter-1].accessory2)   
                                party[activeCharacter-1].accessory2 = attachedItem
                            elif ("Weapon" in entity.tags and attachedItem.type == "weapon"):
                                if (party[activeCharacter-1].weapon == attachedItem): 
                                    attachedItem = None
                                    attachedItemVisual.isShowing = False
                                    break
                                inventory.remove(attachedItem)
                                if (not party[activeCharacter-1].weapon == None): inventory.append(party[activeCharacter-1].weapon)   
                                party[activeCharacter-1].weapon = attachedItem
                            updateInventory()
                            updateCharacter()
                            attachedItem = None
                            attachedItemVisual.isShowing = False
                            break
                if (not attachedItem == None):
                    if (not attachedItemEquipped == None):
                        if (attachedItemEquipped == "Helmet"):
                            party[activeCharacter-1].helmet = None
                            inventory.append(attachedItem)
                        elif (attachedItemEquipped == "Chestplate"):
                            party[activeCharacter-1].chestplate = None
                            inventory.append(attachedItem) 
                        elif (attachedItemEquipped == "Leggings"):
                            print(attachedItemEquipped)
                            party[activeCharacter-1].leggings = None
                            inventory.append(attachedItem)
                        elif (attachedItemEquipped == "Boots"):
                            party[activeCharacter-1].boots = None
                            inventory.append(attachedItem)
                        elif (attachedItemEquipped == "Accessory1"):
                            party[activeCharacter-1].accessory1 = None
                            inventory.append(attachedItem)
                        elif (attachedItemEquipped == "Accessory2"):
                            party[activeCharacter-1].accessory2 = None
                            inventory.append(attachedItem)
                        elif (attachedItemEquipped == "Weapon"):
                            party[activeCharacter-1].weapon = None
                            inventory.append(attachedItem)  
                    attachedItem = None
                    attachedItemVisual.isShowing = False
                    updateInventory()
                    updateCharacter()
    
        if (not attachedItem == None):
            attachedItemVisual.xPosition = mouse[0] - attachedItemVisual.width/2
            attachedItemVisual.yPosition = mouse[1] - attachedItemVisual.length/2
        '''
        refreshScreen(screen)
        if (quit): break
    return newSceneData
