from model.character.Skill import Skill
from model.character.Character import Character
from model.Singleton import Singleton

def attack(character:Character, enemy:Character, gameData:Singleton, skill:Skill):
    character.dealDamage((character.attack * skill.motionValue/100), "Physical", enemy)

def fireBolt(character:Character, enemy:Character, gameData:Singleton, skill:Skill):
     attack = (character.attack * skill.motionValue/100)
     if gameData.currentWeatherEffect == "Fog": attack = attack*.8
     character.dealDamage(attack, "Blaze", enemy)

def flameSwathe(character:Character, enemy:Character, gameData:Singleton, skill:Skill):
    for allEnemies in gameData.currentEnemies:
        character.dealDamage((character.attack * skill.motionValue/100), "Blaze", allEnemies)
    if gameData.currentWeatherEffect == "Fog": gameData.currentWeatherEffect = "Mist"

def rock(character:Character, enemy:Character, gameData:Singleton, skill:Skill):
    character.dealDamage((character.attack * skill.motionValue/100), "Foundation", enemy)



def useSkill(character:Character, enemy:Character, gameData:Singleton, skill:Skill):
    # General things that always happen
    character.spendMana(skill.manaCost)

    # mega switch statement :widegladeline2:
    # nvm python doesn't have switch statements :youknowicattodoittoem:
    # add a line for every new skill :thumbeline:
    if skill.name == "Attack": attack(character, enemy, gameData, skill)
    elif skill.name == "Fire Bolt": fireBolt(character, enemy, gameData, skill)
    elif skill.name == "Flame Swathe": flameSwathe(character, enemy, gameData, skill)
    elif skill.name == "Rock": rock(character, enemy, gameData, skill)