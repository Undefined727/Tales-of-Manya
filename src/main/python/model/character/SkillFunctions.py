from model.character.Skill import Skill
from model.character.Character import Character
from model.Singleton import Singleton

def attack(character:Character, enemy:Character, gameData:Singleton, skill:Skill):
    enemy.takeDamage(character.attack * skill.motionValue/100)

def fireBolt(character:Character, enemy:Character, gameData:Singleton, skill:Skill):
    enemy.takeDamage(character.attack * skill.motionValue/100)

def flameSwathe(character:Character, enemy:Character, gameData:Singleton, skill:Skill):
    for aoe in gameData.currentEnemies:
        aoe.takeDamage(character.attack * skill.motionValue/100)



def useSkill(character:Character, enemy:Character, gameData:Singleton, skill:Skill):
    # General things that always happen
    character.spendMana(skill.manaCost)

    # mega switch statement :widegladeline2:
    # nvm python doesn't have switch statements :youknowicattodoittoem:
    # add a line for every new skill :thumbeline:
    if skill.name == "Attack": attack(character, enemy, gameData, skill)
    elif skill.name == "Fire Bolt": fireBolt(character, enemy, gameData, skill)
    elif skill.name == "Flame Swathe": flameSwathe(character, enemy, gameData, skill)
