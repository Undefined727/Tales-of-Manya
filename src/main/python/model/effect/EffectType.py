from enum import Enum

class EffectType(Enum):
    NONE                    = -1
    ATTACK_FLAT             =  0
    ATTACK_PCT              =  1
    DEFENSE_FLAT            =  2
    DEFENSE_PCT             =  3
    DAMAGE_OVER_TIME_FLAT   =  4
    DAMAGE_OVER_TIME_PCT    =  5
    SPELLPOWER_FLAT         =  6
    SPELLPOWER_PCT          =  7
    HEALTH_FLAT             =  8
    HEALTH_PCT              =  9
    MANA_FLAT               = 10
    MANA_PCT                = 11
    MANA_EFFICIENCY         = 12
    MANA_RECOVERY           = 13
    HEALING_PCT             = 14
    INCOMING_DAMAGE_FLAT    = 15
    INCOMING_DAMAGE_PCT     = 16
