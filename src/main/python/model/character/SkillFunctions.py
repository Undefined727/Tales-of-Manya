from model.character.Skill import Skill
from model.character.Character import Character
from view.visualentity.Battlefield import Battlefield
from model.Singleton import Singleton

def attack(character:Character, enemy:Character, gameData:Singleton, battlefield:Battlefield, skill:Skill):
    attack = (character.attack * skill.motionValue/100)
    battlefield.dealDamage(attack, "Physical", character, enemy)

def fireBolt(character:Character, enemy:Character, gameData:Singleton, battlefield:Battlefield, skill:Skill):
     attack = (character.attack * skill.motionValue/100)
     if gameData.currentWeatherEffect == "Fog": attack = attack*.8
     battlefield.dealDamage(attack, "Blaze", character, enemy)

def flameSwathe(character:Character, enemy:Character, gameData:Singleton, battlefield:Battlefield, skill:Skill):
    attack = (character.attack * skill.motionValue/100)
    for allEnemies in gameData.currentEnemies:
        battlefield.dealDamage(attack, "Blaze", character, allEnemies)
    if gameData.currentWeatherEffect == "Fog": gameData.currentWeatherEffect = "Mist"

def rock(character:Character, enemy:Character, gameData:Singleton, battlefield:Battlefield, skill:Skill):
    attack = (character.attack * skill.motionValue/100)
    character.dealDamage(attack, "Foundation", enemy)



def useSkill(character:Character, enemy:Character, gameData:Singleton, battlefield:Battlefield, skill:Skill):
    # General things that always happen
    character.spendMana(skill.manaCost)

    # mega switch statement :widegladeline2:
    # nvm python doesn't have switch statements :youknowicattodoittoem:
    # add a line for every new skill :thumbeline:
    if skill.name == "Attack": attack(character, enemy, gameData, battlefield, skill)
    elif skill.name == "Fire Bolt": fireBolt(character, enemy, gameData, battlefield, skill)
    elif skill.name == "Flame Swathe": flameSwathe(character, enemy, gameData, battlefield, skill)
    elif skill.name == "Rock": rock(character, enemy, gameData, battlefield, skill)