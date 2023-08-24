
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"
    id:Mapped[str] = mapped_column(String(32), primary_key=True)
    name:Mapped[str] = mapped_column(String(120))
    image_path:Mapped[str] = mapped_column(String(256))
    description:Mapped[Optional[str]]

    slots:Mapped[List["item_slots"]] = relationship(
        back_populates = "item_id",
        cascade = "all, delete-orphan"
        )

    tags:Mapped[List["item_tags"]] = relationship(
        back_populates = "item_id",
        cascade = "all, delete-orphan"
        )

    effects:Mapped[List["item_effects"]] = relationship(
        back_populates = "slot",
        cascade = "all, delete-orphan"
        )

    def __repr__(self) -> str:
        return f"Item(id = {self.id!r}, name = {self.name!r}, image_path = {self.image_path!r}, description = {self.description!r})"

class ItemSlot(Base):
    __tablename__ = "item_slots"
    id:Mapped[str] = mapped_column(String(32), primary_key=True)
    item_id:Mapped[str] = mapped_column(ForeignKey("items.id"))
    slot:Mapped[str] = relationship(back_populates="slots")

    def __repr__(self) -> str:
        return f"ItemSlot(id = {self.id!r}, item_id = {self.item_id!r}, slot = {self.slot!r})"

class ItemTag(Base):
    __tablename__ = "item_tags"
    id:Mapped[str] = mapped_column(String(32), primary_key=True)
    item_id:Mapped[str] = mapped_column(ForeignKey("items.id"))
    tag:Mapped[str] = relationship(back_populates="tags")

    def __repr__(self) -> str:
        return f"ItemSlot(id = {self.id!r}, item_id = {self.item_id!r}, tag = {self.tag!r})"

class ItemEffect(Base):
    __tablename__ = "item_slots"
    id:Mapped[str] = mapped_column(String(32), primary_key=True)
    item_id:Mapped[str] = mapped_column(ForeignKey("items.id"))
    effect:Mapped[str] = relationship(back_populates="effects")
    value:Mapped[Optional[int]]

    def __repr__(self) -> str:
        return f"ItemSlot(id = {self.id!r}, item_id = {self.item_id!r}, effect = {self.effect!r}, value = {self.value!r})"