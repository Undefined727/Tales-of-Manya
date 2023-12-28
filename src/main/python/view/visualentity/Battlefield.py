import json, pygame, random
from model.character.Character import Character
from view.visualentity.CombatCharacterEntity import CombatCharacterEntity
from view.visualentity.Animation import Animation
from view.visualentity.ImageEntity import ImageEntity
from view.visualentity.DamageNumber import DamageNumber
from model.Singleton import Singleton

class Battlefield:
    name = "battlefield"
    isShowing = True
    tags = []
    screenX = 0
    screenY = 0

    enemies:list[CombatCharacterEntity]
    characters:list[CombatCharacterEntity]
    currentWeather:str
    currentWeatherAnimation:Animation
    damageNumbers:list[DamageNumber]
    attackAnimationTimer:int
    attackAnimation:Animation
    gameData:Singleton

    PLAYER_LINE_START = (0.02, 0.65)
    PLAYER_LINE_END = (0.98, 0.98)
    PLAYER_Y_IND_PERCENT = 0.6
    PLAYER_X_IND_PERCENT = 0.7

    ENEMY_LINE_START = (0.02, 0.02)
    ENEMY_LINE_END = (0.98, 0.35)
    ENEMY_Y_IND_PERCENT = 0.6
    ENEMY_X_IND_PERCENT = 0.7

    def __init__(self, gameData:Singleton):
        self.screenX, self.screenY = gameData.pygameWindow.get_size()
        self.characters = self.buildCombatEntities(gameData.player.party, self.PLAYER_LINE_START, self.PLAYER_LINE_END, self.PLAYER_X_IND_PERCENT, self.PLAYER_Y_IND_PERCENT, gameData.pygameWindow)
        self.enemies = self.buildCombatEntities(gameData.currentEnemies, self.ENEMY_LINE_START, self.ENEMY_LINE_END, self.ENEMY_X_IND_PERCENT, self.ENEMY_Y_IND_PERCENT, gameData.pygameWindow)
        for enemy in self.enemies:
            enemy.isEnemy = True
        self.currentWeatherAnimation = Animation("WeatherAnimation")
        self.currentWeatherAnimation.scale(*gameData.pygameWindow.get_size())
        self.currentWeatherAnimation.updateImages(f"weather{gameData.currentWeatherEffect}Animation")
        self.damageNumbers = []
        self.attackAnimation = Animation("AttackAnimation")
        self.attackAnimationTimer = 0




    def buildCombatEntities(self, characters:list[Character], start:tuple, end:tuple, xPercent:float, yPercent:float, window:pygame.Surface):
        totalWidth = xPercent*(end[0]-start[0])/(len(characters)+1)
        totalHeight = yPercent*(end[1]-start[1])

        count = 1
        combatEntities = []
        for character in characters:
            characterX = start[0] + count*(end[0]-start[0])/(len(characters)+1)
            characterY = start[1] + count*(end[1]-start[1])/(len(characters)+1)

            entityDetails = {
                "name": character.name,
                "HPBorderXPosition": characterX-totalWidth/2,
                "HPBorderYPosition": characterY-totalHeight/2,
                "ManaBorderXPosition": characterX-totalWidth/2,
                "ManaBorderYPosition": characterY-totalHeight*0.2,
                "BorderWidth": totalWidth*0.5,
                "BorderHeight": totalHeight*0.3,
                "checkmarkXPosition": characterX,
                "checkmarkYPosition": characterY,
                "checkmarkWidth": totalWidth,
                "checkmarkHeight": totalHeight,
                "imgXPosition": characterX,
                "imgYPosition": characterY-totalHeight/2,
                "imgWidth": totalWidth/2,
                "imgHeight": totalHeight
            }
            entityDetails = json.loads(json.dumps(entityDetails))

            displayedCharacter = CombatCharacterEntity.createFrom(entityDetails)
            displayedCharacter.characterHPBarText.updateText(displayedCharacter.characterHPBarText.text, displayedCharacter.characterHPBarText.font, 12)
            displayedCharacter.scale(*window.get_size())
            if (character.basedef == 0): isEnemy = False
            else: isEnemy = True
            displayedCharacter.changeCharacter(character, isEnemy)

            combatEntities.append(displayedCharacter)
            count = count+1
        return combatEntities
        

    def getItems(self):
        items = []
        for enemy in self.enemies:
            if (enemy.character.getCurrentHP() > 0): items.append(enemy)
        for character in self.characters:
            if (character.character.getCurrentHP() > 0): items.append(character)
        items.append(self.currentWeatherAnimation)
        items.extend(self.characters)
        for number in self.damageNumbers[:]:
            if number.timer <= 0:
                self.damageNumbers.remove(number)
        items.extend(self.damageNumbers)
        if (self.attackAnimationTimer > 0): items.append(self.attackAnimation)
        return items
    
    def getButtons(self):
        buttons = []
        for enemy in self.enemies:
            if (enemy.character.getCurrentHP() > 0): buttons.append(enemy.getButtons())
        for character in self.characters:
            if (character.character.getCurrentHP() > 0): buttons.append(character.getButtons())
        return buttons
    
    def dealDamage(self, rawDamage : float, damageType : str, damageDealer : Character, attacked : Character):
        allEntities = self.characters + self.enemies
        for character in allEntities:
            if character.character == damageDealer:
                damageDealerEntity = character
            if character.character == attacked:
                attackedEntity = character
        
        damageDealt = damageDealerEntity.dealDamage(rawDamage, damageType, attackedEntity)
        damageNumberXPosition = attackedEntity.characterImg.xPosition + random.randint(int(-attackedEntity.characterImg.width), int(attackedEntity.characterImg.width))
        damageNumberYPosition = attackedEntity.characterImg.yPosition + random.randint(int(-attackedEntity.characterImg.height/2), int(attackedEntity.characterImg.width))
        self.damageNumbers.append(DamageNumber(damageDealt, damageType, damageNumberXPosition, damageNumberYPosition, self.screenX, self.screenY))

            
    def updateCharacters(self):
        for character in self.characters:
            character.updateCharacter()
        for enemy in self.enemies:
            enemy.updateCharacter()