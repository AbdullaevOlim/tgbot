from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from requests import get_book_by_title_and_branch, get_faculties_by_book_and_branch, add_book_to_db, add_branch_to_db, get_book_by_title, update_book_field
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.future import select
from models import async_session, Branch


router = Router()

class EditBookForm(StatesGroup):
    book_title = State()  # Для ввода названия книги
    edit_field = State()  # Для выбора поля для редактирования
    new_value = State()

# Добавим состояние для редактирования филиала
class EditBranchForm(StatesGroup):
    branch_name = State()  # Состояние для ввода текущего названия филиала
    new_branch_name = State()  # Состояние для ввода нового названия филиала

# Состояния для команд
class Form(StatesGroup):
    book_title = State()  # Состояние для ввода названия книги
    branch_name = State()  # Состояние для ввода названия филиала
    command = State()  # Состояние для ввода команды (count_books или count_faculties)

class AddBookForm(StatesGroup):
    book_data = State()  # Состояние для ввода данных книги

class AddBranchForm(StatesGroup):
    branch_name = State()  # Состояние для ввода названия филиала

# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для обслуживания библиотеки.\n"
        "Вот что я могу:\n"
        "/count_books - Посчитать количество экземпляров книги в филиале.\n"
        "/count_faculties - Посчитать факультеты, на которых используется книга в филиале.\n"
        "/add_book - Добавить новую книгу в библиотеку.\n"
        "/add_branch - Добавить новый филиал в библиотеку.\n"
        "/edit_book - Изменить информацию о книге.\n"
        "/edit_branch - Изменить информацию о филиале.\n"
    )

# Обработчик команды /add_book
@router.message(Command('add_book'))
async def cmd_add_book(message: Message, state: FSMContext):
    await state.set_state(AddBookForm.book_data)  # Устанавливаем состояние для ввода данных книги
    await message.answer(
        "Введите данные книги через запятую в следующем формате:\n"
        "Название, Автор, Издательство, Год издания, Количество страниц, Количество иллюстраций, Стоимость, Филиал, Количество экземпляров, Количество студентов, Факультеты (через запятую)"
    )

# Обработчик команды /add_branch
@router.message(Command('add_branch'))
async def cmd_add_branch(message: Message, state: FSMContext):
    await state.set_state(AddBranchForm.branch_name)  # Устанавливаем состояние для ввода названия филиала
    await message.answer("Введите название нового филиала:")

# Обработчик команды /count_books
@router.message(Command('count_books'))
async def cmd_count_books(message: Message, state: FSMContext):
    await state.set_state(Form.command)  # Устанавливаем состояние для команды
    await state.update_data(command='count_books')  # Сохраняем команду
    await message.answer("Введите название книги:")
    await state.set_state(Form.book_title)  # Переход в состояние для ввода названия книги

# Обработчик команды /count_faculties
@router.message(Command('count_faculties'))
async def cmd_count_faculties(message: Message, state: FSMContext):
    await state.set_state(Form.command)  # Устанавливаем состояние для команды
    await state.update_data(command='count_faculties')  # Сохраняем команду
    await message.answer("Введите название книги:")
    await state.set_state(Form.book_title)  # Переход в состояние для ввода названия книги

@router.message(Command('edit_book'))
async def cmd_edit_book(message: Message, state: FSMContext):
    await state.set_state(EditBookForm.book_title)
    await message.answer("Введите название книги, которую хотите отредактировать:")

# Обработчик команды /edit_branch
@router.message(Command('edit_branch'))
async def cmd_edit_branch(message: Message, state: FSMContext):
    await state.set_state(EditBranchForm.branch_name)  # Переход в состояние для ввода текущего названия филиала
    await message.answer("Введите название филиала, который вы хотите редактировать:")

# Обработка ввода названия филиала для команды /add_branch
@router.message(AddBranchForm.branch_name)
async def process_new_branch_name(message: Message, state: FSMContext):
    branch_name = message.text.strip()

    # Вызываем функцию добавления филиала в базу данных
    branch_added = await add_branch_to_db(branch_name)

    if branch_added:
        await message.answer(f"Филиал '{branch_name}' успешно добавлен в базу данных.")
    else:
        await message.answer(f"Филиал с названием '{branch_name}' уже существует.")

    # Завершаем состояние
    await state.clear()  # Очистка состояния после завершения работы


@router.message(Form.book_title)
async def process_book_title(message: Message, state: FSMContext):
    book_title = message.text.strip()

    # Получаем данные из состояния
    data = await state.get_data()
    command = data.get("command")

    # Запрашиваем название филиала
    if command in ['count_books', 'count_faculties']:
        await state.update_data(book_title=book_title)  # Сохраняем название книги
        await message.answer("Введите название филиала:")
        await state.set_state(Form.branch_name)  # Переходим в состояние для ввода филиала

@router.message(Form.branch_name)
async def process_branch_name(message: Message, state: FSMContext):
    branch_name = message.text.strip()

    # Получаем данные из состояния
    data = await state.get_data()
    book_title = data.get("book_title")
    command = data.get("command")

    if command == 'count_books':
        # Получаем количество экземпляров книги в указанном филиале
        copies = await get_book_by_title_and_branch(book_title, branch_name)
        if copies is not None:
            await message.answer(
                f"В филиале '{branch_name}' имеется {copies} экземпляров книги '{book_title}'."
            )
        else:
            await message.answer(f"Книга '{book_title}' не найдена в филиале '{branch_name}'.")
    elif command == 'count_faculties':
        # Получаем факультеты, на которых используется книга
        faculties = await get_faculties_by_book_and_branch(book_title, branch_name)

        if faculties is not None:
            if faculties:
                # Выводим факультеты
                faculties_text = "\n".join([f"{i+1}. {faculty}" for i, faculty in enumerate(faculties)])
                await message.answer(
                    f"Книга '{book_title}' используется на следующих факультетах в филиале '{branch_name}':\n"
                    f"{faculties_text}\n"
                    f"Всего факультетов: {len(faculties)}."
                )
            else:
                await message.answer(f"Книга '{book_title}' не используется на факультетах в филиале '{branch_name}'.")
        else:
            await message.answer(f"Книга '{book_title}' не найдена в филиале '{branch_name}'.")

    # Завершаем состояние
    await state.clear()  # Очистка состояния после завершения работы

@router.message(AddBookForm.book_data)
async def process_book_data(message: Message, state: FSMContext):
    book_data = message.text.strip()

    # Разбиваем введенную строку по запятой
    try:
        data = [item.strip() for item in book_data.split(",")]

        if len(data) < 11:
            raise ValueError("Некорректное количество данных. Ожидается минимум 11 элементов.")

        title, author, publisher, year_of_publication, pages, illustrations, price, branch_name, copies_in_branch, students_borrowed, *faculties_using = data
        faculties_using = ', '.join(faculties_using)

        # Преобразуем типы данных
        year_of_publication = int(year_of_publication)
        pages = int(pages)
        illustrations = int(illustrations)
        price = float(price)
        copies_in_branch = int(copies_in_branch)
        students_borrowed = int(students_borrowed)

        # Получаем branch_id по имени филиала
        async with async_session() as session:
            result = await session.execute(select(Branch).filter(Branch.name == branch_name))
            branch = result.scalars().first()

            if not branch:
                # Если филиал не найден, создаем новый
                print(f"Филиал '{branch_name}' не найден. Создаем новый филиал.")  # Логируем
                new_branch = Branch(name=branch_name)  # Создаем новый филиал
                session.add(new_branch)
                await session.flush()  # Вставляем филиал и получаем его ID
                branch = new_branch
                print(f"Новый филиал добавлен с ID: {branch.id}")  # Логируем ID нового филиала

            # Добавляем книгу в базу данных с найденным или созданным филиалом
            await add_book_to_db(
                title, author, publisher, year_of_publication, pages, illustrations, price, 
                branch.id, copies_in_branch, students_borrowed, faculties_using,
                session  # Передаем сессию
            )

            await message.answer(f"Книга '{title}' успешно добавлена в библиотеку!")

    except ValueError as e:
        await message.answer(f"Ошибка при добавлении книги: {str(e)}.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}.")
    
    await state.clear()

@router.message(EditBookForm.book_title)
async def process_edit_book_title(message: Message, state: FSMContext):
    book_title = message.text.strip()

    # Проверяем, существует ли книга с таким названием
    book = await get_book_by_title(book_title)
    if book:
        await state.update_data(book_id=book.id, book_title=book.title)
        await message.answer(f"Вы выбрали редактирование книги '{book_title}'. Что вы хотите изменить?\n"
                             "1. Название книги\n"
                             "2. Автор\n"
                             "3. Издательство\n"
                             "4. Год издания\n"
                             "5. Количество страниц\n"
                             "6. Количество иллюстраций\n"
                             "7. Стоимость\n"
                             "8. Филиал\n"
                             "9. Количество экземпляров\n"
                             "10. Количество студентов, которым выдана\n"
                             "11. Факультеты\n"
                             "12. Вернуться в главное меню")
        await state.set_state(EditBookForm.edit_field)
    else:
        await message.answer(f"Книга с названием '{book_title}' не найдена. Пожалуйста, попробуйте снова.")
        await state.clear()

@router.message(EditBookForm.edit_field)
async def process_edit_field(message: Message, state: FSMContext):
    choice = message.text.strip()

    # Проверяем выбор пользователя
    fields = {
        "1": "title",
        "2": "author",
        "3": "publisher",
        "4": "year_of_publication",
        "5": "pages",
        "6": "illustrations",
        "7": "price",
        "8": "branch",
        "9": "copies_in_branch",
        "10": "students_borrowed",
        "11": "faculties_using",
    }

    if choice in fields:
        field = fields[choice]
        await state.update_data(field=field)

        # Запрашиваем новое значение для выбранного поля
        if field == "branch":
            await message.answer("Введите название нового филиала:")
        else:
            await message.answer(f"Введите новое значение для поля '{field}':")
        await state.set_state(EditBookForm.new_value)
    elif choice == "12":
        # Возвращаемся в главное меню
        await message.answer("Возвращаюсь в главное меню.")
        await state.clear()
    else:
        await message.answer("Неверный выбор. Пожалуйста, выберите правильный номер из списка.")

@router.message(EditBookForm.new_value)
async def process_new_value(message: Message, state: FSMContext):
    new_value = message.text.strip()
    data = await state.get_data()
    book_id = data.get("book_id")
    field = data.get("field")

    # Обновляем поле в базе данных
    try:
        if field == "year_of_publication" or field == "pages" or field == "illustrations" or field == "copies_in_branch" or field == "students_borrowed":
            new_value = int(new_value)
        elif field == "price":
            new_value = float(new_value)
        elif field == "faculties_using":
            # Факультеты вводятся как строка, разделенная запятой
            new_value = ', '.join(new_value.split(','))

        # Обновляем книгу в базе данных
        await update_book_field(book_id, field, new_value)

        await message.answer(f"Поле '{field}' успешно обновлено на '{new_value}'.")
        await state.clear()
    except ValueError as e:
        await message.answer(f"Ошибка при обновлении: {str(e)}")
        await state.clear()

@router.message(EditBranchForm.branch_name)
async def process_branch_name_for_edit(message: Message, state: FSMContext):
    branch_name = message.text.strip()

    # Логируем введенное название филиала
    print(f"Пользователь ввел название филиала для редактирования: '{branch_name}'")

    # Проверяем, существует ли филиал с таким названием в базе данных
    async with async_session() as session:
        result = await session.execute(select(Branch).filter(Branch.name == branch_name))
        branch = result.scalars().first()

    if branch:
        # Если филиал найден, переходим к следующему состоянию для ввода нового названия
        await state.update_data(branch_name=branch_name)
        await state.set_state(EditBranchForm.new_branch_name)
        await message.answer(f"Пожалуйста, введите новое название для этого филиала:")
    else:
        # Если филиал не найден, сообщаем пользователю
        await message.answer(f"Филиал с названием '{branch_name}' не найден. Пожалуйста, попробуйте снова.")
        await state.clear()  # Очистка состояния, если филиал не найден

@router.message(EditBranchForm.new_branch_name)
async def process_new_edit_branch_name(message: Message, state: FSMContext):
    new_branch_name = message.text.strip()

    # Получаем данные из состояния (текущее название филиала)
    data = await state.get_data()
    old_branch_name = data.get("branch_name")

    # Логируем новое название филиала
    print(f"Пользователь ввел новое название филиала: '{new_branch_name}'")

    # Проверяем, существует ли филиал с новым названием
    async with async_session() as session:
        result = await session.execute(select(Branch).filter(Branch.name == new_branch_name))
        existing_branch = result.scalars().first()

    if existing_branch:
        # Если филиал с таким названием уже существует, сообщаем пользователю
        await message.answer(f"Филиал с названием '{new_branch_name}' уже существует. Пожалуйста, выберите другое название.")
        return

    # Обновляем название филиала
    async with async_session() as session:
        # Находим филиал с старым названием
        result = await session.execute(select(Branch).filter(Branch.name == old_branch_name))
        branch = result.scalars().first()

        if branch:
            # Обновляем название филиала
            branch.name = new_branch_name
            await session.commit()  # Сохраняем изменения в базе данных
            await message.answer(f"Название филиала '{old_branch_name}' было успешно изменено на '{new_branch_name}'.")
        else:
            await message.answer(f"Филиал с названием '{old_branch_name}' не найден в базе данных.")

    # Завершаем состояние
    await state.clear()  # Очистка состояния после завершения работы
