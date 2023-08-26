from enum import Enum

class Error(Enum):
    INEXISTENT_SLOT = "The slot does not exist"
    SLOT_TAKEN = "There is already an item equipped on that slot"
    NO_ITEM = "There is no item on that slot"
    ITEM_NOT_FOUND = "The item requested was not found"
    CANNOT_BE_NEGATIVE = "This field cannot be negative"
    CANNOT_BE_BELOW_ONE = "This field cannot go below 1"
    ILLEGAL_RANGE = "The number passed is not within the legal range."
    EXPIRED_EFFECT = "This effect is expired"