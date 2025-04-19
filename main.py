
import json  # Import the json module to handle reading and writing book data to files

class BookCollection:
    def __init__(self):
        """Initialize a new book collection with an empty list and set up file storage."""
        self.book_list = []  # Create an empty list to store all book entries
        self.storage_file = "book_data.json"  # Set the filename for saving/loading data
        self.read_from_file()  # Load existing data from the file (if any)

    def read_from_file(self):
        """Load saved books from a JSON file into memory. Start with an empty collection if file is missing or corrupted."""
        try:
            with open(self.storage_file, "r") as file:  # Try opening the file for reading
                loaded_books = json.load(file)  # Load and parse JSON data
                # Filter out invalid book entries
                self.book_list = [
                    book for book in loaded_books
                    if isinstance(book, dict) and "title" in book and "author" in book
                ]
        except (FileNotFoundError, json.JSONDecodeError):  # If file doesn't exist or is corrupted
            self.book_list = []  # Start with an empty list

    def save_to_file(self):
        """Store the current book collection to a JSON file for permanent storage."""
        with open(self.storage_file, "w") as file:  # Open the file in write mode
            json.dump(self.book_list, file, indent=4)  # Save the list to file with indentation for readability

    def create_new_book(self):
        """Add a new book to the collection by gathering information from the user."""
        while True:
            book_title = input("Enter the book title: ").strip()  # Prompt user for book title
            if book_title:  # Check that title is not empty
                break
            print("Title cannot be empty. Please try again.")  # Warn and retry if empty

        # Prompt user for remaining details
        book_author = input("Enter author: ").strip()
        publication_year = input("Enter publication year: ").strip()
        book_genre = input("Enter genre: ").strip()
        is_book_read = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

        # Create a new dictionary for the book
        new_book = {
            "title": book_title,
            "author": book_author,
            "year": publication_year,
            "genre": book_genre,
            "read": is_book_read,
        }

        self.book_list.append(new_book)  # Add the new book to the list
        self.save_to_file()  # Save the updated list to file
        print("Book added successfully!\n")  # Confirm to user

    def delete_book(self):
        """Remove a book from the collection using its title."""
        book_title = input("Enter the title of the book to remove: ").strip()  # Get title from user

        for book in self.book_list:
            if book.get("title", "").lower() == book_title.lower():  # Match title ignoring case
                self.book_list.remove(book)  # Remove the matched book
                self.save_to_file()  # Save the updated list
                print("Book removed successfully!\n")  # Confirm to user
                return
        print("Book not found")  # Inform if no match is found

    def find_book(self):
        """Search for books in the collection by title or author name."""
        search_type = input("Search by:\n1. Title\n2. Author\nEnter your choice: ")  # Ask how to search
        search_text = input("Enter search term: ").lower()  # Get search input and convert to lowercase

        # Filter books that match the search term in title or author
        found_books = [
            book for book in self.book_list
            if search_text in book.get("title", "").lower() or search_text in book.get("author", "").lower()
        ]

        if found_books:  # If matches found
            print("Matching Books:")
            for index, book in enumerate(found_books, 1):  # Enumerate matching books
                reading_status = "Read" if book.get("read", False) else "Unread"
                print(
                    f"{index}. {book.get('title', 'N/A')} by {book.get('author', 'N/A')} "
                    f"({book.get('year', 'N/A')}) - {book.get('genre', 'N/A')} - {reading_status}"
                )
        else:
            print("No matching books found.\n")  # Inform if none found

    def update_book(self):
        """Modify the details of an existing book in the collection."""
        book_title = input("Enter the title of the book you want to edit: ").strip()  # Get title to edit

        for book in self.book_list:
            if book.get("title", "").lower() == book_title.lower():  # Find matching book
                print("Leave blank to keep existing value.")

                # Ask for new details; keep old if input is blank
                book["title"] = input(f"New title ({book.get('title')}): ").strip() or book["title"]
                book["author"] = input(f"New author ({book.get('author')}): ").strip() or book["author"]
                book["year"] = input(f"New year ({book.get('year')}): ").strip() or book["year"]
                book["genre"] = input(f"New genre ({book.get('genre')}): ").strip() or book["genre"]
                book["read"] = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

                self.save_to_file()  # Save updated list
                print("Book updated successfully!\n")  # Confirm to user
                return
        print("Book not found!\n")  # Inform if book not found

    def show_all_books(self):
        """Display all books in the collection with their details."""
        if not self.book_list:  # Check if collection is empty
            print("Your collection is empty.\n")
            return

        print("Your Book Collection:")
        for index, book in enumerate(self.book_list, 1):  # Enumerate all books
            reading_status = "Read" if book.get("read", False) else "Unread"
            print(
                f"{index}. {book.get('title', 'N/A')} by {book.get('author', 'N/A')} "
                f"({book.get('year', 'N/A')}) - {book.get('genre', 'N/A')} - {reading_status}"
            )
        print()  # Print blank line for spacing

    def show_reading_progress(self):
        """Calculate and display statistics about your reading progress."""
        total_books = len(self.book_list)  # Total books in collection
        completed_books = sum(1 for book in self.book_list if book.get("read", False))  # Count of read books
        completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0  # Avoid division by zero

        print(f"Total books in collection: {total_books}")  # Show total count
        print(f"Reading progress: {completion_rate:.2f}%\n")  # Show reading percentage

    def start_application(self):
        """Run the main application loop with a user-friendly menu interface."""
        while True:
            # Display menu options
            print("📚 Welcome to Your Book Collection Manager! 📚")
            print("1. Add a new book")
            print("2. Remove a book")
            print("3. Search for books")
            print("4. Update book details")
            print("5. View all books")
            print("6. View reading progress")
            print("7. Exit")

            user_choice = input("Please choose an option (1-7): ").strip()  # Get user selection

            # Handle menu choices
            if user_choice == "1":
                self.create_new_book()
            elif user_choice == "2":
                self.delete_book()
            elif user_choice == "3":
                self.find_book()
            elif user_choice == "4":
                self.update_book()
            elif user_choice == "5":
                self.show_all_books()
            elif user_choice == "6":
                self.show_reading_progress()
            elif user_choice == "7":
                self.save_to_file()  # Save changes before exiting
                print("Thank you for using Book Collection Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.\n")  # Handle invalid input

# This block runs the application when the script is executed
if __name__ == "__main__":
    book_manager = BookCollection()  # Create an instance of the BookCollection class
    book_manager.start_application()  # Start the app's main loop
