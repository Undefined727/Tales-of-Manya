
import uuid
from typing import List
from typing import Optional
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from src.main.python.model.item import Item
from src.main.python.model.skill import Skill
from main.python.model.item import ItemSlotType
from src.main.python.model.effect import Effect

# TODO Everything here is hopelessly broken
class Base(DeclarativeBase):
    pass

class DBItemSlot(Base):
    __tablename__ = "ItemSlot"
    id:Mapped[str] = mapped_column(String(32), primary_key=True)
    item_id:Mapped[str] = mapped_column(String, ForeignKey("items.id"))
    slot:Mapped[str] = relationship(back_populates="slots")

    @staticmethod
    def fromSlotList(slotsList, item_id:str):
        result = list()
        for slot in slotsList:
            result.append(DBItemSlot.fromItemSlot(slot, item_id))
        return result

    @staticmethod
    def fromItemSlot(item_slot:ItemSlotType, item_id:str):
        return DBItemSlot(id        = item_slot.value,
                          item_id   = item_id,
                          slot      = item_slot.name)

    def __repr__(self) -> str:
        return f"ItemSlot(id = {self.id!r}, item_id = {self.item_id!r}, slot = {self.slot!r})"

class DBTag(Base):
    __tablename__ = "Tag"
    id:Mapped[str] = mapped_column(String(32), primary_key=True)
    effect_id:Mapped[str] = mapped_column(ForeignKey("Effect.id"))
    item_id:Mapped[str] = mapped_column(ForeignKey("Item.id"))
    skill_id:Mapped[str] = mapped_column(ForeignKey("Skill.id"))
    tag:Mapped[str] = relationship(back_populates="tags")

    @staticmethod
    def fromTagList(tagsList, effect_id:str = None, item_id:str = None, skill_id:str = None):
        result = []
        for tag in tagsList:
            result.append(DBTag.fromTag(tag, effect_id, item_id, skill_id))
        return result

    @staticmethod
    def fromTag(tag, effect_id:str = None, item_id:str = None, skill_id:str = None):
        return DBTag(id         = uuid.uuid5(uuid.NAMESPACE_DNS, "basedstudios.dev"),
                     effect_id  = effect_id,
                     item_id    = item_id,
                     skill_id   = skill_id,
                     name       = tag.name)

    def __repr__(self) -> str:
        return f"ItemSlot(id = {self.id!r}, item_id = {self.item_id!r}, tag = {self.tag!r})"

class DBEffect(Base):
    __tablename__ = "Effect"
    id:Mapped[str] = mapped_column(String(32), primary_key = True)
    item_id:Mapped[str] = mapped_column(ForeignKey("Item.id"))
    skill_id:Mapped[str] = mapped_column(ForeignKey("Skill.id"))
    effect:Mapped[str] = relationship(back_populates="effects")
    effect_type:Mapped[str]
    value:Mapped[Optional[int]]
    duration:Mapped[int]

    @staticmethod
    def fromEffectList(effectsList, item_id:str, skill_id:str):
        result = list()
        for effect in effectsList:
            result.append(DBEffect.fromEffect(effect, item_id, skill_id))
        return result

    @staticmethod
    def fromEffect(effect:Effect, item_id, skill_id):
        return DBEffect(id          = effect.id,
                        item_id     = item_id,
                        skill_id    = skill_id,
                        name        = effect.name,
                        effect_type = effect.effect_type.name,
                        value       = effect.value,
                        duration    = effect.duration)

    def __repr__(self) -> str:
        return f"ItemSlot(id = {self.id!r}, item_id = {self.item_id!r}, effect = {self.effect!r}, value = {self.value!r})"

class DBItem(Base):
    __tablename__ = "Item"
    id:Mapped[str] = mapped_column(String(32), primary_key=True)
    name:Mapped[str] = mapped_column(String(120))
    image_path:Mapped[Optional[str]] = mapped_column(String(256))
    description:Mapped[Optional[str]]

    slots:Mapped[List[DBItemSlot]] = relationship(
        back_populates = "item_id",
        cascade = "all, delete-orphan"
        )

    tags:Mapped[List[DBTag]] = relationship(
        back_populates = "item_id",
        cascade = "all, delete-orphan"
        )

    effects:Mapped[List[DBEffect]] = relationship(
        back_populates = "item_id",
        cascade = "all, delete-orphan"
        )

    @staticmethod
    def fromItem(item:Item):
        slots = DBItemSlot.fromSlotList(item.slots, item_id = item.id)
        tags = DBTag.fromTagList(item.tags, item_id = item.id)
        effects = DBEffect.fromEffectList(item.item_bonuses, item_id = item.id)
        return DBItem(id            = item.id,
                      name          = item.name,
                      image_path    = item.image_path,
                      description   = item.description,
                      slots         = slots,
                      tags          = tags,
                      effects       = effects)

    def __repr__(self) -> str:
        return f"Item(id = {self.id!r}, name = {self.name!r}, image_path = {self.image_path!r}, description = {self.description!r})"

# class DBSkill(Base):
#     __tablename__ = "Skill"
#     id:Mapped[str]
#     name:Mapped[str]
#     manaCost:Mapped[int]
#     tags:Mapped[List[DBTag]] = relationship(
#         back_populates = "skill_id",
#         cascade = "all, delete-orphan"
#     )
#     effects:Mapped[List[DBEffect]] = relationship(
#         back_populates = "skill_id",
#         cascade = "all, delete-orphan"
#     )

#     @staticmethod
#     def fromSkill(skill:Skill):
#         tags = DBTag.fromTagList(skill.tags)
#         effects = DBEffect.fromEffectList(skill.effects)
#         return DBSkill(id       = skill.id,
#                        name     = skill.name,
#                        manaCost = skill.manaCost,
#                        tags     = tags,
#                        effects  = effects)

#     def __repr__(self) -> str:
#         return f"Item(id = {self.id!r}, name = {self.name!r}, manaCost = {self.manaCost!r}, tags = {self.tags!r}, effects = {self.effects!r})"