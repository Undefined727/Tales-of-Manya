from model.character.Skill import Skill
from model.character.Character import Character
from model.Singleton import Singleton

def attack(character:Character, enemy:Character, party:list[Character], enemies:list[Character], motionValue:int):
    enemy.takeDamage(character.attack * motionValue/100)




def useSkill(character:Character, enemy:Character, gameData:Singleton, skill:Skill):
    # General things that always happen
    character.spendMana(skill.manaCost)

    # mega switch statement :widegladeline2:
    # nvm python doesn't have switch statements :youknowicattodoittoem:
    # add a line for every new skill :thumbeline:
    if skill.name == "attack": attack(character, enemy, gameData.player.party, gameData.currentEnemies, skill.motionValue)