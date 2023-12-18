from model.character.Skill import Skill
from model.character.Character import Character
from view.visualentity.CombatCharacterEntity import CombatCharacterEntity
from model.Singleton import Singleton

def attack(characterData:CombatCharacterEntity, enemyData:CombatCharacterEntity, gameData:Singleton, skill:Skill):
    characterData.dealDamage((characterData.character.attack * skill.motionValue/100), "Physical", enemyData)

def fireBolt(characterData:CombatCharacterEntity, enemyData:CombatCharacterEntity, gameData:Singleton, skill:Skill):
     attack = (characterData.character.attack * skill.motionValue/100)
     if gameData.currentWeatherEffect == "Fog": attack = attack*.8
     characterData.dealDamage(attack, "Blaze", enemyData)

def flameSwathe(characterData:CombatCharacterEntity, enemyData:CombatCharacterEntity, gameData:Singleton, skill:Skill):
    for allEnemies in gameData.currentEnemies:
        characterData.dealDamage((characterData.character.attack * skill.motionValue/100), "Blaze", allEnemies)
    if gameData.currentWeatherEffect == "Fog": gameData.currentWeatherEffect = "Mist"

def rock(characterData:CombatCharacterEntity, enemyData:CombatCharacterEntity, gameData:Singleton, skill:Skill):
    characterData.dealDamage((characterData.character.attack * skill.motionValue/100), "Foundation", enemyData)



def useSkill(characterData:CombatCharacterEntity, enemyData:CombatCharacterEntity, gameData:Singleton, skill:Skill):
    # General things that always happen
    characterData.character.spendMana(skill.manaCost)

    # mega switch statement :widegladeline2:
    # nvm python doesn't have switch statements :youknowicattodoittoem:
    # add a line for every new skill :thumbeline:
    if skill.name == "Attack": attack(characterData, enemyData, gameData, skill)
    elif skill.name == "Fire Bolt": fireBolt(characterData, enemyData, gameData, skill)
    elif skill.name == "Flame Swathe": flameSwathe(characterData, enemyData, gameData, skill)
    elif skill.name == "Rock": rock(characterData, enemyData, gameData, skill)