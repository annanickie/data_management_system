import json
import os
import re

class UserManager:
    def __init__(self, filename='users.json'):
        """
        Initializes the UserManager with a specified filename for storing user data.
        Loads users from the file if it exists.
        """
        self.filename = filename
        self.users = []
        self.load_users()

    def load_users(self):
        """
        Loads users from a JSON file. If the file does not exist, initializes an empty user list.
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.users = json.load(file)
        else:
            self.users = []

    def save_users(self):
        """
        Saves the current list of users to a JSON file.
        """
        with open(self.filename, 'w') as file:
            json.dump(self.users, file, indent=4)

    def create_user(self, user):
        """
        Creates a new user. Checks for unique user ID and valid email format.
        Returns True if the user is successfully created, otherwise False.
        """
        if self.read_user(user['id']):
            print("User with this ID already exists.")
            return False
        if not self.validate_email(user['email']):
            print("Invalid email format.")
            return False
        self.users.append(user)
        self.save_users()
        return True

    def read_user(self, user_id=None):
        """
        Reads a user by ID. If no ID is provided, returns all users.
        Returns the user data or None if the user is not found.
        """
        if user_id:
            for user in self.users:
                if user['id'] == user_id:
                    return user
            return None
        else:
            return self.users

    def update_user(self, user_id, updated_user):
        """
        Updates an existing user identified by user ID with new data.
        Checks for valid email format if the email field is updated.
        Returns True if the user is successfully updated, otherwise False.
        """
        for user in self.users:
            if user['id'] == user_id:
                if 'email' in updated_user and not self.validate_email(updated_user['email']):
                    print("Invalid email format.")
                    return False
                user.update(updated_user)
                self.save_users()
                return True
        return False

    def delete_user(self, user_id):
        """
        Deletes a user by ID.
        Returns True if the user is successfully deleted, otherwise False.
        """
        for user in self.users:
            if user['id'] == user_id:
                self.users.remove(user)
                self.save_users()
                return True
        return False

    def search_users(self, name=None, email=None, age=None):
        """
        Searches for users based on specified criteria: name, email, and age.
        Returns a list of users that match the criteria.
        """
        results = self.users
        if name:
            results = [user for user in results if user['name'].lower() == name.lower()]
        if email:
            results = [user for user in results if user['email'].lower() == email.lower()]
        if age:
            results = [user for user in results if user['age'] == age]
        return results

    @staticmethod
    def validate_email(email):
        """
        Validates the format of an email address using a regular expression.
        Returns True if the email format is valid, otherwise False.
        """
        # Simple regex for email validation
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None

def main():
    """
    Main function to run the user management system.
    Provides a console-based interface for CRUD operations.
    """
    user_manager = UserManager()
    
    while True:
        print("\nUser Management System")
        print("1. Create User")
        print("2. Read User")
        print("3. Update User")
        print("4. Delete User")
        print("5. Search Users")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            # Prompt for user details
            user = {
                'id': input("Enter ID: "),
                'name': input("Enter Name: "),
                'email': input("Enter Email: "),
                'age': int(input("Enter Age: "))
            }
            if user_manager.create_user(user):
                print("User created successfully.")
            else:
                print("User creation failed. ID must be unique or invalid email format.")
        
        elif choice == '2':
            # Prompt for user ID
            user_id = input("Enter user ID to retrieve (leave blank to retrieve all): ")
            if user_id:
                user = user_manager.read_user(user_id)
                if user:
                    print(f"User Found: {user}")
                else:
                    print("User not found.")
            else:
                users = user_manager.read_user()
                print("All Users:")
                for user in users:
                    print(user)
        
        elif choice == '3':
            # Prompt for user ID and updated details
            user_id = input("Enter user ID to update: ")
            updated_user = {}
            name = input("Enter new Name (leave blank to skip): ")
            if name:
                updated_user['name'] = name
            email = input("Enter new Email (leave blank to skip): ")
            if email:
                updated_user['email'] = email
            age = input("Enter new Age (leave blank to skip): ")
            if age:
                updated_user['age'] = int(age)
            
            if user_manager.update_user(user_id, updated_user):
                print("User updated successfully.")
            else:
                print("User not found or invalid email format.")
        
        elif choice == '4':
            # Prompt for user ID
            user_id = input("Enter user ID to delete: ")
            if user_manager.delete_user(user_id):
                print("User deleted successfully.")
            else:
                print("User not found.")
        
        elif choice == '5':
            # Prompt for search criteria
            name = input("Enter name to search (leave blank to skip): ")
            email = input("Enter email to search (leave blank to skip): ")
            age = input("Enter age to search (leave blank to skip): ")
            age = int(age) if age else None
            
            users = user_manager.search_users(name=name, email=email, age=age)
            if users:
                print("Users Found:")
                for user in users:
                    print(user)
            else:
                print("No users found.")
        
        elif choice == '6':
            break
        
        else:
            print("Invalid choice. Please try again.")

        # Prompt for feedback
        feedback = input("Would you like to provide feedback on your experience? (yes/no): ")
        if feedback.lower() == 'yes':
            user_feedback = input("Please enter your feedback: ")
            print("Thank you for your feedback!")

if __name__ == '__main__':
    main()
