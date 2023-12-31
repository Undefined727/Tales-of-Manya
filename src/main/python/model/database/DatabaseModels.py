from uuid import uuid4
from typing import List
from typing import Optional
from sqlalchemy import String, Integer, Column, ForeignKey, Float
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session

# TODO Everything here is hopelessly broken
class Base(DeclarativeBase):
    pass

# class DBTag(Base):
#     __tablename__ = "Tag"
#     id : Mapped[str] = mapped_column(String(36), primary_key=True)
#     effect_id : Mapped[str] = mapped_column(ForeignKey("Effect.id"))
#     effect : Mapped["DBEffect"] = relationship(back_populates = "tags")
#     item_id : Mapped[str] = mapped_column(ForeignKey("Item.id"))
#     item :  Mapped["DBItem"] = relationship(back_populates = "tags")
#     skill_id : Mapped[str] = mapped_column(ForeignKey("Skill.id"))
#     skill : Mapped["DBSkill"] = relationship(back_populates = "tags")
#     tag : Mapped[str] = mapped_column(String(100))

#     def __repr__(self) -> str:
#         return f"ItemSlot(id = {self.id!r}, item_id = {self.item_id!r}, tag = {self.tag!r})"

# class DBEffect(Base):
#     __tablename__ = "Effect"
#     id : Mapped[str] = mapped_column(String(36), primary_key = True)
#     item_id : Mapped[str] = mapped_column(ForeignKey("Item.id"), nullable = True)
#     item : Mapped["DBItem"] = relationship(back_populates = "effects")
#     skill_id : Mapped[str] = mapped_column(ForeignKey("Skill.id"), nullable = True)
#     skill : Mapped["DBSkill"] = relationship(back_populates = "effects")
#     name : Mapped[str] = mapped_column(String(100), nullable = False)
#     effect_type : Mapped[str] = mapped_column(String(100))
#     value : Mapped[Optional[int]] = mapped_column(Integer)
#     duration : Mapped[int] = mapped_column(Integer)

#     tags : Mapped["DBTag"] = relationship(
#         back_populates = "effect",
#         cascade = "all, delete-orphan"
#     )

#     def __repr__(self) -> str:
#        return f"ItemSlot(id = {self.id!r}, item_id = {self.item_id!r}, effect = {self.effect!r}, value = {self.value!r})"

class DBItem(Base):
    __tablename__ = "Item"
    id : Mapped[str] = mapped_column(String(36), primary_key=True)
    name : Mapped[str] = mapped_column(String(120), unique=True)
    type : Mapped[str] = mapped_column(String(120))
    image_path : Mapped[Optional[str]] = mapped_column(String(256))
    description : Mapped[Optional[str]] = mapped_column(String(1000))

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
    id : Mapped[str] = mapped_column(Integer, primary_key = True)
    name : Mapped[str] = mapped_column(String(120))
    description : Mapped[str] = mapped_column(String(2000))
    character : Mapped[str] = mapped_column(String(120))
    element : Mapped[str] = mapped_column(String(15))
    affinity : Mapped[int] = mapped_column(Integer)
    manaCost : Mapped[int] = mapped_column(Integer)
    motionValue : Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"Skill(id = {self.id!r}, name = {self.name!r}, element = {self.element!r}, manaCost = {self.manaCost!r}, motionValue = {self.motionValue!r})"

class DBCharacter(Base):
    __tablename__ = "Character"
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    name : Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    skill1 : Mapped[DBSkill] = mapped_column(ForeignKey("Skill.name"))
    skill2 : Mapped[DBSkill] = mapped_column(ForeignKey("Skill.name"))
    skill3 : Mapped[DBSkill] = mapped_column(ForeignKey("Skill.name"))
    skill4 : Mapped[DBSkill] = mapped_column(ForeignKey("Skill.name"))
    brilliance : Mapped[int] = mapped_column(Integer, nullable=False)
    surge : Mapped[int] = mapped_column(Integer, nullable=False)
    blaze : Mapped[int] = mapped_column(Integer, nullable=False)
    passage : Mapped[int] = mapped_column(Integer, nullable=False)
    clockwork : Mapped[int] = mapped_column(Integer, nullable=False)
    void : Mapped[int] = mapped_column(Integer, nullable=False)
    foundation : Mapped[int] = mapped_column(Integer, nullable=False)
    frost : Mapped[int] = mapped_column(Integer, nullable=False)
    flow : Mapped[int] = mapped_column(Integer, nullable=False)
    abundance : Mapped[int] = mapped_column(Integer, nullable=False)
    description : Mapped[str] = mapped_column(String(2000))
    basehealth : Mapped[int] = mapped_column(Integer, nullable=False)
    scalehealth : Mapped[float] = mapped_column(Float, nullable=False)
    basemana : Mapped[int] = mapped_column(Integer, nullable=False)
    scalemana : Mapped[float] = mapped_column(Float, nullable=False)
    basedef : Mapped[int] = mapped_column(Integer, nullable=False)
    scaledef : Mapped[float] = mapped_column(Float, nullable=False)
    basespellpower : Mapped[int] = mapped_column(Integer, nullable=False)
    scalespellpower : Mapped[float] = mapped_column(Float, nullable=False)
    baseattack : Mapped[int] = mapped_column(Integer, nullable=False)
    scaleattack : Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        affinities = f"brilliance surge      blaze      passage    clockwork  void       foundation frost      flow       abundance \n"
        affinities += f"{self.brilliance!r:10} {self.surge!r:10} {self.blaze!r:10} {self.passage!r:10} {self.clockwork!r:10} {self.void!r:10} {self.foundation!r:10} {self.frost!r:10} {self.flow!r:10} {self.abundance!r:10}"
        basic_stats = f"health     mana       defense    spellpower attack    \n"
        basic_stats += f"{self.basehealth!r:10}  {self.basemana!r:10}  {self.basedef!r:10} {self.basespellpower!r:10} {self.baseattack!r:10}"
        level_stats = f"health     mana       defense    spellpower attack    \n"
        level_stats += f"{self.scalehealth!r:10}  {self.scalemana!r:10}  {self.scaledef!r:10} {self.scalespellpower!r:10} {self.scaleattack!r:10}"
        return f"id: {self.id}\nname: {self.name}\nskill 1: {self.skill1}\nskill 2: {self.skill2}\nskill 3: {self.skill3}\nskill 4: {self.skill4}\n{affinities}\ndescription: {self.description}\nbase stats: {basic_stats}\nscaling stats: {level_stats}\n"

class DBConversation(Base):
    __tablename__ = "Conversation"
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    name : Mapped[str] = mapped_column(String(120), unique = True)
    head_node : Mapped[int] = mapped_column(ForeignKey("Dialogue.id"))

    def __repr__(self) -> str:
        return f"ID: {self.id}, name: {self.name}, head_node: {self.head_node}"

class DBDialogue(Base):
    __tablename__ = "Dialogue"
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    parent_id : Mapped[int] = mapped_column(ForeignKey("Dialogue.id"), nullable = True)
    conversation : Mapped[int] = mapped_column(ForeignKey("Conversation.id"), nullable = True)
    tag : Mapped[str] = mapped_column(String(120), nullable = True)
    leading_text : Mapped[str] = mapped_column(String(500), nullable = True)
    content : Mapped[str] = mapped_column(String(500))
    character_id : Mapped[int] = mapped_column(Integer)
    emotion : Mapped[str] = mapped_column(String(120))
    reward_friendship : Mapped[int] = mapped_column(Integer)
    reward_xp : Mapped[int] = mapped_column(Integer)
    reward_items : Mapped[List["DBReward"]] = relationship()
    quest : Mapped[int] = mapped_column(ForeignKey("Quest.id"), nullable = True)

    def __repr__(self):
        return f"ID: {self.id}, tag: {self.tag}, character_id: {self.character_id}, emotion: {self.emotion}, rewards: {self.reward_friendship} {self.reward_xp}, content: {self.content}"

class DBReward(Base):
    __tablename__ = "Reward"
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    item_id : Mapped[int] = mapped_column(ForeignKey("Item.id"))
    dialogue_id : Mapped[int] = mapped_column(ForeignKey("Dialogue.id"))

    def __repr__(self) -> str:
        return f"ID: {self.id}, Item: {self.item_id}, Dialogue: {self.dialogue_id}"

class DBQuest(Base):
    __tablename__ = "Quest"
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    name : Mapped[str] = mapped_column(String(120), unique = True)
    description : Mapped[str] = mapped_column(String(500))

    def __repr__(self) -> str:
        return f"ID: {self.id}, name: {self.name}, description: {self.description}"

class DBSubquest(Base):
    __tablename__ = "Subquest"
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    name : Mapped[str] = mapped_column(String(120), unique = True)
    type : Mapped[str] = mapped_column(String(120), nullable = False)
    data : Mapped[str] = mapped_column(String(500), nullable = False)
    goal : Mapped[int] = mapped_column(Integer, nullable = False)
    xp : Mapped[int] = mapped_column(Integer)
    parent : Mapped[int] = mapped_column(ForeignKey("Quest.id"))

    def __repr__(self) -> str:
        return f"ID: {self.id}, name: {self.name}, type: {self.type}, data: {self.data}, XP: {self.xp}"

class DBSubquestConversation(Base):
    __tablename__ = "SubquestConversation"
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    map_index : Mapped[int] = mapped_column(Integer, nullable = False)
    parent : Mapped[int] = mapped_column(ForeignKey("Subquest.id"))
    conversation: Mapped[int] = mapped_column(ForeignKey("Conversation.id"))

    def __repr__(self) -> str:
        return f"ID: {self.id}, index: {self.map_index}, parent subquest: {self.parent}, conversation ID: {self.conversation}"

class DBSubquestReward(Base):
    __tablename__ = "SubquestReward"
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    item_id : Mapped[int] = mapped_column(ForeignKey("Item.id"))
    subquest_id : Mapped[int] = mapped_column(ForeignKey("Subquest.id"))

    def __repr__(self) -> str:
        return f"ID: {self.id}, Item: {self.item_id}, Subquest: {self.subquest_id}"

class DBSubquestFollowup(Base):
    __tablename__ = "SubquestFollowup"
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    parent : Mapped[int] = mapped_column(ForeignKey("Subquest.id"), nullable = False)
    child : Mapped[int] = mapped_column(ForeignKey("Subquest.id"), nullable = False)

    def __repr__(self) -> str:
        return f"ID: {self.id}, parent: {self.parent}, child: {self.child}"

class DBRegion(Base):
    __tablename__ = "Region"
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    name : Mapped[str] = mapped_column(String(120), nullable = False, unique = True)

    def __repr__(self) -> str:
        return f"ID: {self.id}, name: {self.name}"

class DBQuestRegion(Base):
    __tablename__ = "QuestRegion"
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    quest : Mapped[int] = mapped_column(ForeignKey("Quest.id"))
    region : Mapped[int] = mapped_column(ForeignKey("Region.id"))

    def __repr__(self) -> str:
       return f"ID: {self.id}, quest: {self.quest}, region: {self.region}"

# ## Initialization ###
from sqlalchemy import create_engine
engine = create_engine("sqlite:///src/main/python/catgirl-dungeon.db", echo = True)


## This line resets the whole database ###
# Base.metadata.drop_all(engine)

# ## This line creates the database as described in the classes above ###
Base.metadata.create_all(engine)

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