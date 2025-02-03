import json
import os
from abc import ABC, abstractmethod
from typing import List


# Классы сущностей
class Book:

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"Книга: {self.title}. Автор: {self.author}"


class Reader:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Читатель: {self.name}. Возраст: {self.age}"


class Librarian:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Библиотекарь: {self.name}"


# Singleton для библиотеки
class Library:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.books = []
            cls._instance.readers = []
            cls._instance.librarians = []
        return cls._instance

    def add_book(self, book: Book):
        self.books.append(book)

    def remove_book(self, book: Book):
        self.books.remove(book)

    def add_reader(self, reader: Reader):
        self.readers.append(reader)

    def add_librarian(self, librarian: Librarian):
        self.librarians.append(librarian)

    def list_books(self):
        return self.books

    def list_readers(self):
        return self.readers

    def list_librarian(self):
        return self.librarians

    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as fh:
            json.dump([book.__dict__ for book in self.books], fh, ensure_ascii=False, indent=4)

    def load_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as fh:
                books_data = json.load(fh)
                print(books_data)


# Фабрика для создания книг, читателей, библиотекарей
class EntityFactory:
    @staticmethod
    def create_book(title: str, author: str) -> Book:
        return Book(title, author)

    @staticmethod
    def create_reader(name: str, age: int) -> Reader:
        return Reader(name, age)

    @staticmethod
    def create_librarian(name: str) -> Librarian:
        return Librarian(name)


# Паттерн Command
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class AddBookCommand(Command):
    def __init__(self, library: Library, book: Book):
        self.library = library
        self.book = book

    def execute(self):
        self.library.add_book(self.book)


class RemoveBookCommand(Command):

    def __init__(self, library: Library, book: Book):
        self.library = library
        self.book = book

    def execute(self):
        self.library.remove_book(self.book)


class AddReaderCommand(Command):

    def __init__(self, library: Library, reader: Reader):
        self.library = library
        self.reader = reader

    def execute(self):
        self.library.add_reader(self.reader)


class AddLibrarianCommand(Command):

    def __init__(self, library: Library, librarian: Librarian):
        self.library = library
        self.librarian = librarian

    def execute(self):
        self.library.add_librarian(self.librarian)


# Логгер. Паттерн Observer
class Logger:
    def log(self, message: str):
        with open('library_log.txt', 'a', encoding='utf-8') as fh:
            fh.write(message + '\n')


# Стратегия для поиска
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, books: List[Book], query: str) -> List[Book]:
        pass


class TitleSearchStrategy(SearchStrategy):
    def search(self, books: List[Book], query: str) -> List[Book]:
        return [book for book in books if query.lower() in book.title.lower()]


class AuthorSearchStrategy(SearchStrategy):
    def search(self, books: List[Book], query: str) -> List[Book]:
        return [book for book in books if query.lower() in book.author.lower()]


class ReaderSearchStrategy(SearchStrategy):

    def search(self, readers: List[Reader], query: str) -> List[Reader]:
        return [reader for reader in readers if query.lower() in reader.name.lower()]


class LibrarianSearchStrategy(SearchStrategy):

    def search(self, librarians: List[Librarian], query: str) -> List[Librarian]:
        return [librarian for librarian in librarians if query.lower() in librarian.name.lower()]


if __name__ == '__main__':
    book1 = EntityFactory.create_book("1984", "Джордж Оруэлл")
    book2 = EntityFactory.create_book("О дивный новый мир", "Олдос Хаксли")
    book3 = EntityFactory.create_book("Зов Ктулху", "Говард Лавкравт")
    book4 = EntityFactory.create_book("451' по Фаренгейту", "Рэй Брэдбери")
    reader1 = EntityFactory.create_reader("Василий Зайцев", 25)
    reader2 = EntityFactory.create_reader("Елена Малышева", 35)
    librarian = EntityFactory.create_librarian("Виктор Степанов")

    library = Library()
    logger = Logger()

    add_book_command = AddBookCommand(library, book1)
    add_book_command.execute()
    logger.log(f"Добавлена книга. {book1}")

    add_book_command = AddBookCommand(library, book2)
    add_book_command.execute()
    logger.log(f"Добавлена книга. {book2}")

    add_book_command = AddBookCommand(library, book3)
    add_book_command.execute()
    logger.log(f"Добавлена книга. {book3}")

    remove_book_command = RemoveBookCommand(library, book2)
    remove_book_command.execute()
    logger.log(f"Удалена книга. {book2}")

    add_book_command = AddBookCommand(library, book4)
    add_book_command.execute()
    logger.log(f"Добавлена книга. {book4}")

    add_reader_command = AddReaderCommand(library, reader1)
    add_reader_command.execute()
    logger.log(f"Добавлен читатель. {reader1}")

    add_reader_command = AddReaderCommand(library, reader2)
    add_reader_command.execute()
    logger.log(f"Добавлен читатель. {reader2}")

    add_librarian_command = AddLibrarianCommand(library, librarian)
    add_librarian_command.execute()
    logger.log(f"Библиотекарь: {librarian}")

    title_search_strategy = TitleSearchStrategy()
    results = title_search_strategy.search(library.list_books(), "1984")
    print("Результат поиска по названию:", [str(book) for book in results])

    author_search_strategy = AuthorSearchStrategy()
    results = author_search_strategy.search(library.list_books(), "Говард Лавкравт")
    print("Результат поиска по автору:", [str(book) for book in results])

    reader_search_strategy = ReaderSearchStrategy()
    results = reader_search_strategy.search(library.list_readers(), "Елена Малышева")
    print("Найден читатель:", [str(reader) for reader in results])

    librarian_search_strategy = LibrarianSearchStrategy()
    results = librarian_search_strategy.search(library.list_librarian(), "Виктор Степанов")
    print("Библиотекарь:", [str(librarian) for librarian in results])

    library.save_to_file("library.json")

    new_library = Library()
    new_library.load_from_file("library.json")
    print("Книги в библиотеке:", [str(book) for book in new_library.list_books()])
