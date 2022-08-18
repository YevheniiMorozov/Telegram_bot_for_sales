from aiogram import types, Bot
from gino.schema import GinoSchemaVisitor
from gino import Gino
from data.config import POSTGRESURI
from sqlalchemy import sql, Column, Sequence, Integer, BigInteger, String, Float, TIMESTAMP, JSON, Boolean


db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(BigInteger)
    full_name = Column(String(200))
    user_name = Column(String(100))
    shipping_address = Column(String(500), default=None)
    phone_number = Column(String(20), default=None)

    query: sql.Select


class Item(db.Model):
    __tablename__ = 'items'

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    img = Column(String(250))
    category = Column(String(50))
    name = Column(String(50))
    description = Column(String(250))
    price = Column(Float(20))
    comment = Column(String(50))
    query: sql.Select


class Purchase(db.Model):
    __tablename__ = 'purchase'

    id = Column(Integer, Sequence('purchase_id_seq'), primary_key=True)
    buyer = Column(BigInteger)
    item_name = Column(String(200))
    amount = Column(Float)
    quantity = Column(Integer)
    purchase_time = Column(TIMESTAMP)
    sucsessful = Column(Boolean, default=False)
    query: sql.Select


class DBCommands:

    async def get_user(self, user_id):
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def add_new_user(self) -> User:
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
        if old_user:
            return old_user
        else:
            new_user = User()
            new_user.user_id = user.id
            new_user.user_name = user.username
            new_user.full_name = user.full_name
            await new_user.create()
            return new_user

    async def get_buyer(self, user_id):
        return await Purchase.query.where(Purchase.buyer == user_id).gino.all()

    async def delete_purchase_buyer(self, user_id):
        await Purchase.delete.where(Purchase.buyer == user_id).gino.all()

    async def delete_purchase_item(self, user_id, item_name):
        await Purchase.delete.where(Purchase.buyer == user_id and Purchase.item_name == item_name).gino.all()

    async def auto_delete_purchase(self, timestamp):
        await Purchase.delete.where(Purchase.purchase_time == timestamp).gino.all()

    async def count_user(self):
        total = await db.func.count(User.id).gino.scalar()
        return total

    async def show_items(self, category):
        items = await Item.query.where(Item.category == category).gino.all()
        return items

    async def delete_items(self, name):
        await Item.delete.where(Item.name == name).gino.status()

    async def update_user(self, user_id, name, address, phone):
        await User.update.where(User.user_id == user_id).values(
            User.full_name == name, User.phone_number == phone, User.shipping_address == address).gino.first()


async def create_db():
    await db.set_bind(POSTGRESURI)
    db.gino: GinoSchemaVisitor
    # await db.gino.drop_all()
    await db.gino.create_all()
