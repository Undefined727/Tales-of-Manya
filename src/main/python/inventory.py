import pygame, numpy, math, os, random, json, copy
from view.visualentity.Tag import Tag
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.ShapeEntity import ShapeEntity
from view.visualentity.TextEntity import TextEntity
from view.visualentity.ShapeButton import ShapeButton
from view.visualentity.ImageButton import ImageButton
from view.visualentity.DynamicStatEntity import DynamicStatEntity
from view.visualentity.CombatCharacterEntity import CharacterEntities
from model.skill.Skill import Skill
from model.character.Character import Character
from model.item.Item import Item
from view.visualentity.CombatEnemyEntity import CombatEnemyEntity
from view.displayHandler import displayEntity
from view.JSONParser import loadJson


visualEntities = []
partyVisuals = []
buttons = []
quit = False
nextScreen = "Quit"


inventory = []

party = [Character("Catgirl", "catgirl.png", 10), Character("Catgirl", "catgirl.png", 10)]
party.append(Character("lmao", "catgirl.png",  20))

party[0].skills[0] = Skill(1)
party[0].skills[1] = Skill(2)
party[0].skills[2] = Skill(3)

inventory.append(Item(9))
inventory.append(Item(9))
inventory.append(Item(7))

party[0].helmet = Item(2)

def combatButton():
    global quit
    global nextScreen
    quit = True
    nextScreen = "Combat"


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
    global party
    global inventory
    global partyVisuals
    #newSceneData = [screen, "Inventory", playerData, currentSceneData[2]]
    screen = screenData[0]
    screenX, screenY = screen.get_size()
    leaveScreen = False
    nextScreen = None
    attachedItem = None
    attachedItemEquipped = None
    
    visualEntities = []
    partyVisuals = [CharacterEntities(party[0])]
    buttons = []
    loadJson("inventoryScreen.json", screenX, screenY, [visualEntities, buttons, partyVisuals, party])

    activeCharacter = 1


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
        nonlocal leaveScreen
        nonlocal nextScreen
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

    '''
    def updateStats():
        global visualEntities
        global party
        nonlocal activeCharacter
        party[activeCharacter-1].updateItems()
        for item in visualEntities:
            if (item.name == "PlayerHPText"): item.updateText("HP: " + str(int(party[activeCharacter-1].maxHP)), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerManaText"): item.updateText("Mana: " + str(int(party[activeCharacter-1].maxMana)), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerMagicText"): item.updateText("Magic Strength: " + str(int(party[activeCharacter-1].magic)), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerATKText"): item.updateText("ATK: " + str(int(party[activeCharacter-1].ATK)), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerDEFText"): item.updateText("DEF: " + str(int(party[activeCharacter-1].DEF)), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerGearHPText"): item.updateText("HP: +" + str(int(party[activeCharacter-1].maxHP - (party[activeCharacter-1].level*100))), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerGearManaText"): item.updateText("Mana: +" + str(int(party[activeCharacter-1].maxMana - (1000 + party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerGearMagicText"): item.updateText("Magic Strength: +" + str(int(party[activeCharacter-1].magic - (party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerGearATKText"): item.updateText("ATK: +" + str(int(party[activeCharacter-1].ATK - (party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green")
            if (item.name == "PlayerGearDEFText"): item.updateText("DEF: +" + str(int(party[activeCharacter-1].DEF - (party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green")

    
    def updateInventory():
        global visualEntities
        for entity in visualEntities[:]:
            if ("Inventory" in entity.tags):
                    visualEntities.remove(entity)
        
        count = 0
        itemrow = 0
        bufferX = screenX/24
        bufferY = screenY/20

        for item in inventory:
            curritemX = count * (itemSizeX + bufferX) + bufferX
            curritemY = itemrow * (itemSizeY + bufferY) + bufferY

            visualEntities.append(VisualEntity.VisualEntity(item.name, 0, True, curritemX, curritemY, itemSizeX, itemSizeY, ["Item", "Inventory"], item.img))
            visualEntities.append(VisualEntity.VisualEntity("Item" + str(count + itemrow*4) + "Button", 2, True, curritemX, curritemY, itemSizeX, itemSizeY, ["Button","Item", "Inventory"], itemClickFunction, [item], "rectangle"))
            count += 1
            if count >= 4:
                count = 0
                itemrow +=1

    activeCharacter = 1

    exitButtonX = screenX/16
    exitButtonY = 5*screenY/6
    buttonSizeX = 4*screenX/16
    buttonSizeY = screenY/8
    catgirlX = 29*screenX/48
    catgirlY = 3*screenY/12
    catgirlSizeX = screenX/3
    catgirlSizeY = 2*screenY/3
    nameX = 29*screenX/48
    nameY = 6*screenY/48
    levelX = 36*screenX/48
    itemSizeX = screenX/12
    itemSizeY = screenX/12
    helmetX = 21*screenX/24
    helmetY = 4*screenY/24
    chestplateX = 21*screenX/24
    chestplateY = 8*screenY/24
    leggingsX = 21*screenX/24
    leggingsY = 12*screenY/24
    bootsX = 21*screenX/24
    bootsY = 16*screenY/24
    accessory1X = 16*screenX/24
    accessory1Y = 19*screenY/24
    accessory2X = 37*screenX/48
    accessory2Y = 19*screenY/24
    weaponX = 29*screenX/48
    weaponY = 10*screenY/24
    statFontSize = screenX/100
    nameFontSize = screenX/40

    changeCharacterRX = 22*screenX/24
    changeCharacterRY = 4*screenY/48
    changeCharacterLX = 20*screenX/24
    changeCharacterLY = 4*screenY/48
    changeCharacterSizeX = screenX/24
    changeCharacterSizeY = 3*screenY/48

    visualEntities.clear()
    CharacterEntities(party[1])
    visualEntities.append(VisualEntity.VisualEntity("HelmetBackground", 1, True, helmetX, helmetY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet", "Item Background"], "cadetblue", False, "rectangle"))
    if (party[activeCharacter-1].helmet == None): visualEntities.append(VisualEntity.VisualEntity("Helmet", 0, True, helmetX, helmetY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet"], "helmet_transparent.png"))
    else: visualEntities.append(VisualEntity.VisualEntity("Helmet", 0, True, helmetX, helmetY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet"], party[activeCharacter-1].helmet.img))
    visualEntities.append(VisualEntity.VisualEntity("ChestplateBackground", 1, True, chestplateX, chestplateY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Chestplate", "Item Background"], "cadetblue", False, "rectangle"))
    if (party[activeCharacter-1].chestplate == None): visualEntities.append(VisualEntity.VisualEntity("Chestplate", 0, True, chestplateX, chestplateY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Helmet"], "chestplate_transparent.png"))
    else: visualEntities.append(VisualEntity.VisualEntity("Chestplate", 0, True, chestplateX, chestplateY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Chestplate"], party[activeCharacter-1].chestplate.img))
    visualEntities.append(VisualEntity.VisualEntity("LeggingsBackground", 1, True, leggingsX, leggingsY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Leggings", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Leggings", 0, True, leggingsX, leggingsY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Leggings"], party[activeCharacter-1].leggings.img))
    visualEntities.append(VisualEntity.VisualEntity("BootsBackground", 1, True, bootsX, bootsY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Boots", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Boots", 0, True, bootsX, bootsY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Boots"], party[activeCharacter-1].boots.img))
    visualEntities.append(VisualEntity.VisualEntity("Accessory1Background", 1, True, accessory1X, accessory1Y, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Accessory1", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Accessory1", 0, True, accessory1X, accessory1Y, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Accessory1"], party[activeCharacter-1].accessory1.img))
    visualEntities.append(VisualEntity.VisualEntity("Accessory2Background", 1, True, accessory2X, accessory2Y, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Accessory2", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Accessory2", 0, True, accessory2X, accessory2Y, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Accessory2"], party[activeCharacter-1].accessory2.img))
    visualEntities.append(VisualEntity.VisualEntity("WeaponBackground", 1, True, weaponX, weaponY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Weapon", "Item Background"], "cadetblue", False, "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Weapon", 0, True, weaponX, weaponY, itemSizeX, itemSizeY, ["Item", "Equipped Item", "Weapon"], party[activeCharacter-1].weapon.img))

    visualEntities.append(VisualEntity.VisualEntity("HelmetButton", 2, True, helmetX, helmetY, itemSizeX, itemSizeY,["Button", "Helmet","Item","Equipped Item"], itemClickFunction, [party[activeCharacter-1].helmet, "Helmet"], "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("ChestplateButton", 2, True, chestplateX, chestplateY, itemSizeX, itemSizeY,["Button", "Chestplate","Item","Equipped Item"], itemClickFunction, [party[activeCharacter-1].chestplate, "Chestplate"], "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("LeggingsButton", 2, True, leggingsX, leggingsY, itemSizeX, itemSizeY,["Button", "Item","Leggings","Equipped Item"], itemClickFunction, [party[activeCharacter-1].leggings, "Leggings"], "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("BootsButton", 2, True, bootsX, bootsY, itemSizeX, itemSizeY,["Button", "Item", "Boots","Equipped Item"], itemClickFunction, [party[activeCharacter-1].boots, "Boots"], "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Accessory1Button", 2, True, accessory1X, accessory1Y, itemSizeX, itemSizeY,["Button", "Item", "Accessory1","Equipped Item"], itemClickFunction, [party[activeCharacter-1].accessory1, "Accessory1"], "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("Accessory2Button", 2, True, accessory2X, accessory2Y, itemSizeX, itemSizeY,["Button", "Item", "Accessory2","Equipped Item"], itemClickFunction, [party[activeCharacter-1].accessory2, "Accessory2"], "rectangle"))
    visualEntities.append(VisualEntity.VisualEntity("WeaponButton", 2, True, weaponX, weaponY, itemSizeX, itemSizeY,["Item", "Equipped Item", "Button", "Weapon"], itemClickFunction, [party[activeCharacter-1].weapon, "Weapon"], "rectangle"))

    visualEntities.append(VisualEntity.VisualEntity("ChangeCharacterRight", 4, True, changeCharacterRX, changeCharacterRY, changeCharacterSizeX, changeCharacterSizeY, ["Change Character"], changeCharacterFunction, "Right", "change_active_right.png"))
    visualEntities.append(VisualEntity.VisualEntity("ChangeCharacterRightImg", 0, True, changeCharacterRX, changeCharacterRY, changeCharacterSizeX, changeCharacterSizeY, ["Change Character"], "change_active_right.png"))
    visualEntities.append(VisualEntity.VisualEntity("ChangeCharacterLeft", 4, True, changeCharacterLX, changeCharacterLY, changeCharacterSizeX, changeCharacterSizeY, ["Change Character"], changeCharacterFunction, "Left", "change_active_left.png"))
    visualEntities.append(VisualEntity.VisualEntity("ChangeCharacterLeftImg", 0, True, changeCharacterLX, changeCharacterLY, changeCharacterSizeX, changeCharacterSizeY, ["Change Character"], "change_active_left.png"))


    updateInventory()

    statX = 29*screenX/48
    stat1Y = 9*screenY/48
    stat2Y = 11*screenY/48
    stat3Y = 13*screenY/48
    stat4Y = 15*screenY/48
    stat5Y = 17*screenY/48
    gearStatBuffer = 20*screenY/48

    visualEntities.append(VisualEntity.VisualEntity("PlayerHPText", 3, True, statX, stat1Y, itemSizeX, itemSizeY, ["Stat"], "HP: " + str(int(party[activeCharacter-1].maxHP)), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerManaText", 3, True, statX, stat2Y, itemSizeX, itemSizeY, ["Stat"], "Mana: " + str(int(party[activeCharacter-1].maxMana)), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerMagicText", 3, True, statX, stat3Y, itemSizeX, itemSizeY, ["Stat"], "Magic Strength: " + str(int(party[activeCharacter-1].magic)), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerATKText", 3, True, statX, stat4Y, itemSizeX, itemSizeY, ["Stat"], "ATK: " + str(int(party[activeCharacter-1].ATK)), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerDEFText", 3, True, statX, stat5Y, itemSizeX, itemSizeY, ["Stat"], "DEF: " + str(int(party[activeCharacter-1].DEF)), "mono", int(statFontSize), "black", "green"))

    visualEntities.append(VisualEntity.VisualEntity("PlayerGearText", 3, True, statX, stat1Y + gearStatBuffer, itemSizeX, itemSizeY, ["Stat"], "Gear Stats", "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerGearHPText", 3, True, statX, stat2Y + gearStatBuffer, itemSizeX, itemSizeY, ["Stat"], "HP: +" + str(int(party[activeCharacter-1].maxHP - (party[activeCharacter-1].level*100))), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerGearManaText", 3, True, statX, stat3Y + gearStatBuffer, itemSizeX, itemSizeY, ["Stat"], "Mana: +" + str(int(party[activeCharacter-1].maxMana - (1000 + party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerGearMagicText", 3, True, statX, stat4Y + gearStatBuffer, itemSizeX, itemSizeY, ["Stat"], "Magic Strength: +" + str(int(party[activeCharacter-1].magic - (party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerGearATKText", 3, True, statX, stat5Y + gearStatBuffer, itemSizeX, itemSizeY, ["Stat"], "ATK: +" + str(int(party[activeCharacter-1].ATK - (party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green"))
    visualEntities.append(VisualEntity.VisualEntity("PlayerGearDEFText", 3, True, statX, stat5Y + gearStatBuffer + 2*screenY/48, itemSizeX, itemSizeY, ["Stat"], "DEF: +" + str(int(party[activeCharacter-1].DEF - (party[activeCharacter-1].level*10))), "mono", int(statFontSize), "black", "green"))


    visualEntities.append(VisualEntity.VisualEntity("ExitImg", 0, True, exitButtonX, exitButtonY, buttonSizeX, buttonSizeY, ["Menu"], "ExitButton.png"))
    visualEntities.append(VisualEntity.VisualEntity("ExitButton", 2, True, exitButtonX, exitButtonY, buttonSizeX, buttonSizeY, ["Menu"], exitButtonFunction, None, "rectangle"))

    visualEntities.append(attachedItemVisual)
    '''

    partyVisuals[0].updateCharacter()
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                for entity in buttons:
                        if entity.mouseInRegion(mouse, entity.shape, entity.xPosition, entity.yPosition, entity.width, entity.length):
                            entity.func(entity.args)
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
        if (leaveScreen): break
    return nextScreen
