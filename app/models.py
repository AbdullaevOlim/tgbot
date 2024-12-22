from sqlalchemy import Integer, String, Float, Text, ForeignKey, Column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import os
from dotenv import load_dotenv
from sqlalchemy.future import select


load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))  # Убедитесь, что URL правильный

# Создание асинхронной сессии
async_session = async_sessionmaker(engine)

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))
    publisher: Mapped[str] = mapped_column(String(100))
    year_of_publication: Mapped[int] = mapped_column(Integer)
    pages: Mapped[int] = mapped_column(Integer)
    illustrations: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    
    # Ссылаемся на Branch через внешний ключ
    branch_id: Mapped[int] = mapped_column(Integer, ForeignKey('branches.id'))
    
    # Дополнительная информация
    copies_in_branch: Mapped[int] = mapped_column(Integer)
    students_borrowed: Mapped[int] = mapped_column(Integer)
    faculties_using: Mapped[str] = mapped_column(Text)

    # Связь с таблицей Branch
    branch: Mapped["Branch"] = relationship("Branch", backref="books")
    
    def __repr__(self):
        return f"<Book(title={self.title}, author={self.author})>"

class Branch(Base):
    __tablename__ = 'branches'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    def __repr__(self):
        return f"<Branch(name={self.name})>"

# Создание всех таблиц в базе данных
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
