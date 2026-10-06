# ==============================================================================
# SECTION 1: IMPORTS
# ==============================================================================
from collections.abc import AsyncGenerator
# a private, internal implementation detail used to define asynchronous generators
# asynchronous generator is a function that contains both async def and the yield statement.
#  • __anext__(): Awaits and retrieves the next value.
# • asend(): Sends a value into the generator asynchronously.
# • athrow(): Raises an exception inside the generator asynchronously.
# • aclose(): Closes the generator asynchronously.

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Text, DateTime,ForeignKey
# SQLAlchemy as a blueprint system. Instead of writing raw database code (SQL), you use these Python components to describe exactly what your database tables and columns should look like.
from sqlalchemy.dialects.postgresql import UUID
# used to import a specific, heavy-duty data type called a Universally Unique Identifier (UUID) that is natively optimized for PostgreSQL databases.
# for users for example

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# its for database to work in cordination establish, configure and work to add in your db

from sqlalchemy.orm import DeclarativeBase, relationship
from fastapi import Depends
# declarative base make the classes inherate the sql alchemy method and attributies to work and relationship create realtion ship of the database

from fastapi_users.db import SQLAlchemyUserDatabase,SQLAlchemyBaseUserTableUUID
# ==============================================================================
# SECTION 2: CONFIGURATION & BASE SETTINGS
# ==============================================================================
DataBase_URL = "sqlite+aiosqlite:///./test.db"
# if we have this database it automaticly so you can read and write if not it create it for you

class Base(DeclarativeBase):
    pass
class User(SQLAlchemyBaseUserTableUUID,Base):
    posts=relationship("Post",back_populates="user")


# ==============================================================================
# SECTION 3: DATABASE MODELS (TABLE BLUEPRINTS)
# ==============================================================================
class Post(Base):
    __tablename__ = "Posts"
# table name is posts in the database

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey("user.id"),nullable=False)
    caption = Column(Text)
    URL = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow)
    file_type=Column(String,nullable=False)

    user=relationship("User",back_populates="posts")
# ==============================================================================
# SECTION 4: ENGINE & SESSION PLUMBING
# ==============================================================================
engine = create_async_engine(DataBase_URL)
# it is the bridge between this file and the actual database it handle the actual low-level coding

AsyncSessionMaker = async_sessionmaker(engine, expire_on_commit=False)
# session maker work it around and make sure its alive


# ==============================================================================
# SECTION 5: DATA LIFECYCLE GENERATOR
# ==============================================================================

async def create_db_and_tables():
    # 1. Open a direct, high-performance connection channel to the database.
    #    'engine.begin()' starts a secure database transaction block.
    async with engine.begin() as conn:
        # 2. Tell SQLAlchemy to look at your 'Base' blueprints, scan all the tables
        #    you created (like your 'Post' class), and physically build them inside the database file.
        #    'run_sync' bridges our async connection to SQLAlchemy's internal table-creation tool.
        await conn.run_sync(Base.metadata.create_all)


async def get_async_sessionl() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker() as session:
        yield session
#this whole functio generator that use yeild use this to write and read the database while the data base still have safe streem under the hode
async def get_user_db(session:AsyncSession=Depends(get_async_sessionl)):
    yield SQLAlchemyUserDatabase(session,User)