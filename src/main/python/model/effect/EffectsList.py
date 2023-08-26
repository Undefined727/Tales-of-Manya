from util.Messages import Error
from model.effect.Effect import Effect
from model.effect.EffectType import EffectType
import util.IllegalArgumentException as IllegalArgumentException

class EffectsList:
    effects : list[ Effect ]

    def __init__(self, effects : list[ Effect ] = list()):
        self.effects = effects

    def iterate(self):
        for effect in self.effects:
            yield effect

    def calculate(self):
        # Sums the values of all effects of each type and returns a dictionary
        # with the information as follows: { EffectType : int }

        types_and_values = {}
        for effect in self.effects:
            if (effect.getDurationRemaining() != 0):
                types_and_values[effect.getType()] += effect.getValue()
        return types_and_values

    def clean(self):
        # Remove all expired effects

        for effect in self.effects:
            if effect.isExpired(): self.effects.remove(effect)

    def add(self, new_effect:Effect):
        if new_effect.isExpired(): raise IllegalArgumentException(Error.EXPIRED_EFFECT)
        for element in self.effects:
            if element.equals(new_effect):
                extra_duration = abs(new_effect.getDuration() - element.getDuration())
                element.setDuration(new_effect.getDuration() + extra_duration)
                return
        self.effects.append(new_effect)

    def has(self, element:Effect):
        for item in self.effects:
            if (item.equals(element)):
                return True

    def remove(self, effect_name:str):
        for effect in self.effects:
            if (effect.getName() == effect_name):
                self.effects.remove(effect)

    def removeByType(self, effect_type:EffectType):
        for effect in self.effects:
            if (effect.getType() == effect_type):
                self.effects.remove(effect)

    def update(self):
        # Decrements the duration of all effects by 1

        for effect in self.effects:
            effect.update()
            if (effect.isExpired()):
                self.effects.remove(effect)

    def addAll(self, list:[]):
        for item in list:
            if (type(item) == Effect):
                self.add(item)

    def addAllFrom(self, another_effects_list):
        for effect in another_effects_list.iterator():
            self.add(effect)

    def addAllFromIntersection(self, another_effects_list):
        for effect in another_effects_list.iterator():
            if (self.has(effect)):
                self.add(effect)