from uuid import uuid4
from typing import List
from typing import Optional
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session

# TODO Everything here is hopelessly broken
class Base(DeclarativeBase):
    pass

# class DBItemSlot(Base):
#     __tablename__ = "ItemSlot"
#     id : Mapped[str] = mapped_column(String(36), primary_key=True)
#     item_id : Mapped[str] = mapped_column(String(36), ForeignKey("Item.id"))
#     item :  Mapped["DBItem"] = relationship(back_populates = "slots")
#     slot : Mapped[str] = mapped_column(String(100))

#     def __repr__(self) -> str:
#         return f"ItemSlot(id = {self.id!r}, item_id = {self.item_id!r}, slot = {self.slot!r})"

class DBTag(Base):
    __tablename__ = "Tag"
    id : Mapped[str] = mapped_column(String(36), primary_key=True)
    effect_id : Mapped[str] = mapped_column(ForeignKey("Effect.id"))
    effect : Mapped["DBEffect"] = relationship(back_populates = "tags")
    item_id : Mapped[str] = mapped_column(ForeignKey("Item.id"))
    item :  Mapped["DBItem"] = relationship(back_populates = "tags")
    skill_id : Mapped[str] = mapped_column(ForeignKey("Skill.id"))
    skill : Mapped["DBSkill"] = relationship(back_populates = "tags")
    tag : Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"ItemSlot(id = {self.id!r}, item_id = {self.item_id!r}, tag = {self.tag!r})"

class DBEffect(Base):
    __tablename__ = "Effect"
    id : Mapped[str] = mapped_column(String(36), primary_key = True)
    item_id : Mapped[str] = mapped_column(ForeignKey("Item.id"), nullable = True)
    item : Mapped["DBItem"] = relationship(back_populates = "effects")
    skill_id : Mapped[str] = mapped_column(ForeignKey("Skill.id"), nullable = True)
    skill : Mapped["DBSkill"] = relationship(back_populates = "effects")
    name : Mapped[str] = mapped_column(String(100), nullable = False)
    effect_type : Mapped[str] = mapped_column(String(100))
    value : Mapped[Optional[int]] = mapped_column(Integer)
    duration : Mapped[int] = mapped_column(Integer)

    tags : Mapped["DBTag"] = relationship(
        back_populates = "effect",
        cascade = "all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"ItemSlot(id = {self.id!r}, item_id = {self.item_id!r}, effect = {self.effect!r}, value = {self.value!r})"

class DBItem(Base):
    __tablename__ = "Item"
    id : Mapped[str] = mapped_column(String(36), primary_key=True)
    name : Mapped[str] = mapped_column(String(120), unique=True)
    type : Mapped[str] = mapped_column(String(120))
    image_path : Mapped[Optional[str]] = mapped_column(String(256))
    description : Mapped[Optional[str]] = mapped_column(String(1000))

    tags : Mapped[List[DBTag]] = relationship(
        back_populates = "item",
        cascade = "all, delete-orphan"
        )

    effects : Mapped[List[DBEffect]] = relationship(
        back_populates = "item",
        cascade = "all, delete-orphan"
        )

    def __repr__(self) -> str:
        return f"Item(id = {self.id!r}, name = {self.name!r}, image_path = {self.image_path!r}, description = {self.description!r})"
    
class DBItemStat(Base):
    __tablename__ = "ItemStat"
    id : Mapped[str] = mapped_column(String(36), primary_key=True)
    item : Mapped[str] = mapped_column(String(120))
    stat : Mapped[str] = mapped_column(String(120))
    value : Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"ItemStat(id = {self.id!r}, item = {self.item!r}, stat = {self.stat!r}, value = {self.value!r})"

class DBSkill(Base):
    __tablename__ = "Skill"
    id : Mapped[str] = mapped_column(String(36), primary_key=True)
    name : Mapped[str] = mapped_column(String(100))
    manaCost : Mapped[int] = mapped_column(Integer)
    tags : Mapped[List[DBTag]] = relationship(
        back_populates = "skill",
        cascade = "all, delete-orphan"
    )
    effects : Mapped[List[DBEffect]] = relationship(
        back_populates = "skill",
        cascade = "all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Item(id = {self.id!r}, name = {self.name!r}, manaCost = {self.manaCost!r}, tags = {self.tags!r}, effects = {self.effects!r})"

# ## Initialization ###
from sqlalchemy import create_engine
engine = create_engine("sqlite:///src/main/python/catgirl-dungeon.db", echo = True)

# ## This line resets the whole database ###
#Base.metadata.drop_all(engine)

# ## This line creates the database as described in the classes above ###
#Base.metadata.create_all(engine)

# # ## Example code to add an Item ###
# with Session(engine) as session:
#     item = DBItem(
#                    id = str(uuid4()),
#                    name = "Purveyor of the Nyaight",
#                    type = "WEAPON",
#                    image_path = "katana.png",
#                    description = "This sword looks like it was made by a catgirl trying to be very dramatic"
#                   )
#     session.add(item)
#     session.commit()
#     print("200 - CODE ran without a hitch")