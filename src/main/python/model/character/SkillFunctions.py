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
    battlefield.dealDamage(attack, "Foundation", character, enemy)

def stare(character:Character, enemy:Character, gameData:Singleton, battlefield:Battlefield, skill:Skill):
    pass


def useSkill(character:Character, enemy:Character, gameData:Singleton, battlefield:Battlefield, skill:Skill):
    # General things that always happen
    character.spendMana(skill.manaCost)

    skillList = { 
        "Attack": attack,
        "Fire Bolt": fireBolt,
        "Flame Swathe": flameSwathe,
        "Rock": rock,
        "Stare": stare
    }
    skillList[skill.name](character, enemy, gameData, battlefield, skill)