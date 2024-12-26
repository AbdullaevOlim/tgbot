from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import async_session, Book, Branch

async def get_book_by_title_and_branch(title: str, branch_name: str):
    async with async_session() as session:
        # Находим филиал по названию
        result = await session.execute(select(Branch).filter(Branch.name == branch_name))
        branch = result.scalars().first()
        
        if branch:
            # Теперь ищем книгу по branch_id
            result = await session.execute(select(Book).filter(Book.title == title, Book.branch_id == branch.id))
            book = result.scalars().first()
            if book:
                return book.copies_in_branch
        return None


async def get_faculties_by_book_and_branch(title: str, branch_name: str):
    async with async_session() as session:
        try:
            # Находим филиал по названию
            result = await session.execute(select(Branch).filter(Branch.name == branch_name))
            branch = result.scalars().first()
            
            if branch:
                # Теперь ищем книгу по branch_id
                result = await session.execute(select(Book.faculties_using).filter(Book.title == title, Book.branch_id == branch.id))
                book = result.scalars().first()
                
                if book:
                    faculties = book.split(", ")  # Разделяем строку по запятой и пробелу
                    return faculties
        except Exception as e:
            print(f"Error in get_faculties_by_book_and_branch: {str(e)}")
            return None

# Функция добавления книги в базу данных
async def add_book_to_db(title, author, publisher, year_of_publication, pages, illustrations, price, 
                          branch_id, copies_in_branch, students_borrowed, faculties_using, session):
    # Создаем книгу с использованием branch_id
    book = Book(
        title=title,
        author=author,
        publisher=publisher,
        year_of_publication=year_of_publication,
        pages=pages,
        illustrations=illustrations,
        price=price,
        branch_id=branch_id,  # Используем branch_id
        copies_in_branch=copies_in_branch,
        students_borrowed=students_borrowed,
        faculties_using=faculties_using
    )
    session.add(book)
    await session.commit()  # Сохраняем изменения в базе


async def add_branch_to_db(branch_name: str):
    async with async_session() as session:
        # Проверка на существование филиала с таким же названием
        existing_branch = await session.execute(select(Branch).filter(Branch.name == branch_name))
        if existing_branch.scalars().first():
            return False  # Филиал с таким именем уже существует

        # Создаем новый филиал
        new_branch = Branch(name=branch_name)
        session.add(new_branch)
        await session.flush()  # Генерируем ID перед коммитом
        await session.commit()
        return True


# Получить книгу по названию
async def get_book_by_title(title: str):
    async with async_session() as session:
        result = await session.execute(select(Book).filter(Book.title == title))
        return result.scalars().first()

# Обновить поле книги в базе данных
async def update_book_field(book_id: int, field: str, new_value: str):
    async with async_session() as session:
        # Получаем книгу по id
        result = await session.execute(select(Book).filter(Book.id == book_id))
        book = result.scalars().first()

        if book:
            setattr(book, field, new_value)
            session.add(book)
            await session.commit()
