
import streamlit as st
import json
import os

class BookCollection:
    def __init__(self):
        self.book_list = []
        self.storage_file = "book_data.json"
        self.read_from_file()

    def read_from_file(self):
        try:
            with open(self.storage_file, "r") as file:
                loaded_books = json.load(file)
                self.book_list = [
                    book for book in loaded_books
                    if isinstance(book, dict) and "title" in book and "author" in book
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    def save_to_file(self):
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)

    def add_book(self, book):
        self.book_list.append(book)
        self.save_to_file()

    def delete_book(self, title):
        self.book_list = [b for b in self.book_list if b["title"].lower() != title.lower()]
        self.save_to_file()

    def update_book(self, original_title, updated_book):
        for i, book in enumerate(self.book_list):
            if book["title"].lower() == original_title.lower():
                self.book_list[i] = updated_book
                break
        self.save_to_file()

    def search_books(self, search_text):
        return [
            book for book in self.book_list
            if search_text.lower() in book["title"].lower() or search_text.lower() in book["author"].lower()
        ]

    def get_progress(self):
        total = len(self.book_list)
        read = sum(1 for book in self.book_list if book.get("read", False))
        return total, read, (read / total * 100 if total else 0)

# ---------- STREAMLIT INTERFACE ----------

st.set_page_config(page_title="📚 Personal Library", layout="centered")
st.title("📚 Personal Library Manager")

book_manager = BookCollection()

menu = st.sidebar.selectbox("Menu", ["Add Book", "View Books", "Update Book", "Delete Book", "Search", "Reading Progress"])

if menu == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.text_input("Year")
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?")

    if st.button("Add Book"):
        if title and author:
            new_book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
            book_manager.add_book(new_book)
            st.success("Book added successfully!")
        else:
            st.error("Title and Author are required.")

elif menu == "View Books":
    st.subheader("Your Book Collection")
    if not book_manager.book_list:
        st.info("No books found.")
    else:
        for idx, book in enumerate(book_manager.book_list, 1):
            st.write(f"**{idx}. {book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")

elif menu == "Update Book":
    st.subheader("Update a Book")
    titles = [book["title"] for book in book_manager.book_list]
    if titles:
        selected_title = st.selectbox("Select book to update", titles)
        book_to_edit = next(b for b in book_manager.book_list if b["title"] == selected_title)

        title = st.text_input("Title", value=book_to_edit["title"])
        author = st.text_input("Author", value=book_to_edit["author"])
        year = st.text_input("Year", value=book_to_edit["year"])
        genre = st.text_input("Genre", value=book_to_edit["genre"])
        read = st.checkbox("Read", value=book_to_edit["read"])

        if st.button("Update Book"):
            updated_book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
            book_manager.update_book(selected_title, updated_book)
            st.success("Book updated successfully!")
    else:
        st.info("No books available to update.")

elif menu == "Delete Book":
    st.subheader("Delete a Book")
    titles = [book["title"] for book in book_manager.book_list]
    if titles:
        selected_title = st.selectbox("Select book to delete", titles)
        if st.button("Delete"):
            book_manager.delete_book(selected_title)
            st.success("Book deleted successfully.")
    else:
        st.info("No books available to delete.")

elif menu == "Search":
    st.subheader("Search Books")
    search_term = st.text_input("Search by title or author")
    if search_term:
        results = book_manager.search_books(search_term)
        if results:
            for idx, book in enumerate(results, 1):
                st.write(f"**{idx}. {book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("No matching books found.")

elif menu == "Reading Progress":
    st.subheader("📈 Reading Progress")
    total, read, progress = book_manager.get_progress()
    st.write(f"Total Books: **{total}**")
    st.write(f"Books Read: **{read}**")
    st.progress(progress / 100)
    st.write(f"**Progress: {progress:.2f}%**")

