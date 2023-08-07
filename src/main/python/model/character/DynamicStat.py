import util.IllegalArgumentException as IllegalArgumentException

class DynamicStat:
    current_value = 0
    max_value = 0

    def __init__(self, max_value):
        self.max_value = max_value
        self.fill()

    def getCurrentValue(self):
        return self.current_value

    def getMaxValue(self):
        return self.max_value

    def getPercentage(self):
        return (self.current_value * 100) / self.max_value

    def setCurrentValue(self, new_value):
        if (new_value > self.max_value):
            self.current_value = self.max_value
        elif (new_value < 0):
            self.current_value = 0
        else:
            self.current_value = new_value

    def setMaxValue(self, new_value):
        self.max_value = new_value

    def setPercentage(self, new_percentage):
        # Sets the 'current_value' field to a percentage of the 'max_value'.
        # The parameter must be a number between 0 and 1.

        if (new_percentage <= 0 or new_percentage > 1):
            raise IllegalArgumentException("The number passed is not within the legal range.")
        else:
            self.current_value = self.max_value * new_percentage

    def replenish(self, amount):
        # Increments the 'current_value' by the value passed, observing the maximum.

        result = self.current_value + amount
        if (result > self.max_value):
            self.current_value = self.max_value
        else:
            self.current_value = result

    def fill(self):
        # Restores the 'current_value' field to the maximum value
        self.current_value = self.max_value

    def incrementMaxBy(self, value, update_current = False):
        # Increments the parameter 'value' to the 'max_value' field.
        # If the 'update_current' flag is marked true, it also adds the value to
        # the 'current_value' field.

        self.max_value += value
        if (update_current):
            self.current_value += value

    def increaseBy(self, value):
        # Adds the given parameter to the current value.
        # Raises an exception when the value is negative.

        if (value < 0):
            raise IllegalArgumentException("Cannot increase by a negative amount.")
        self.current_value += value
        if (self.current_value > self.max_value):
            self.current_value = self.max_value

    def decreaseBy(self, value):
        # Decreases the current value by the given amount.
        # Raises an exception when the value is negative.

        if (value < 0):
            raise IllegalArgumentException("Cannot decrease by a negative amount.")
        self.current_value -= value