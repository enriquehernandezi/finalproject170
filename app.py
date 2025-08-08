import csv #read csv files
from friend import Person 
from birthday import Birthday
from datetime import datetime
import os #work with file system

class MyFriendsApp:
    def __init__(self):
        self.friends = [] #list to store person objects
        self.filename = "friendsdatabase.csv" #csv saved

    def load_from_file(self):
        print("Loading data from CSV...")
        if not os.path.exists(self.filename): ##check if csv file exists
            print("CSV file not found!")
            return
        with open(self.filename, newline='', encoding='utf-8') as file: #utf8 means it will read special characters specially for @
            reader = csv.DictReader(file) #reads each row as dictionary
            for row in reader: # loops through each friend
                print(f"Loading: {row['first_name']} {row['last_name']}") 
                person = Person(row['first_name'], row['last_name']) #creates person object with first and last name
                if row['birthday_month'] and row['birthday_day']:
                    person.set_birthday(int(row['birthday_month']), int(row['birthday_day'])) #sets day of birthday if month and day are not null and makes strings into integers
                person.city = row['city']
                person.phone = row['phone']
                person.street_address = row['street_address']
                person.nickname = row['nickname']
                person.email_address = row['email_address']
                person.state = row['state']
                person.zip = row['zip'] #loads all details from csv
                self.friends.append(person) #adds friend to app's list

    def save_to_file(self):
        with open(self.filename, "w", newline='', encoding='utf-8') as file: #opens file to overwrite
            writer = csv.DictWriter(file, fieldnames=[
                'first_name', 'last_name', 'birthday_month', 'birthday_day', 'city', 'phone',
                'street_address', 'nickname', 'email_address', 'state', 'zip'])
            writer.writeheader()
            for f in self.friends: #loop all friend objects
                writer.writerow({
                    'first_name': f.first_name,
                    'last_name': f.last_name,
                    'birthday_month': f._birthday.get_month() if f._birthday else '', #if birthday isnt set it leaves blank
                    'birthday_day': f._birthday.get_day() if f._birthday else '',
                    'city': f.city,
                    'phone': f.phone,
                    'street_address': f.street_address,
                    'nickname': f.nickname,
                    'email_address': f.email_address,
                    'state': f.state,
                    'zip': f.zip #writes each object as a row
                })

    def create_friend(self):
        print("\nCreate New Friend")
        first = input("First name: ")
        last = input("Last name: ")
        friend = Person(first, last) #prompts user for first and last name , and creates a new friend

        try:
            month = int(input("Birthday month (1-12): "))
            day = int(input("Birthday day: "))
            friend.set_birthday(month, day) #tries to get birthday details, and if invalid it is skipped
        except:
            pass

        friend.city = input("City: ")
        friend.phone = input("Phone: ")
        friend.street_address = input("Street address: ")
        friend.nickname = input("Nickname: ")
        friend.email_address = input("Email: ")
        friend.state = input("State: ")
        friend.zip = input("ZIP: ") #collects friend details

        self.friends.append(friend)
        print("Friend added successfully!") #adds friend to app and confirms

    def search_friend(self):
        query = input("Search by first or last name: ").lower() #asks user for name and lowercases it
        matches = [f for f in self.friends if query in f.first_name.lower() or query in f.last_name.lower()] #search list by name

        if not matches:
            print("No matches found.") #if nothing found exit
            return

        for i, f in enumerate(matches):
            print(f"{idx + 1}. {f}") #shows matches with a number

        choice = input("Enter number to edit/delete or press Enter to cancel: ")
        if not choice.isdigit(): #asks user to choose match
            return

        selected = matches[int(choice) - 1]
        action = input("Type E to edit or D to delete: ").upper()
        if action == 'D':
            confirm = input("Are you sure? Type YES to confirm: ")
            if confirm.upper() == "YES":
                self.friends.remove(selected)
                print("Friend deleted.")
        elif action == 'E':
            self.edit_friend(selected) #if user selects edit or delete confirm

    def edit_friend(self, friend):
        print("Editing. Leave blank to keep current value.")
        friend.city = input(f"City [{friend.city}]: ") or friend.city
        friend.phone = input(f"Phone [{friend.phone}]: ") or friend.phone
        friend.email_address = input(f"Email [{friend.email_address}]: ") or friend.email_address #edit selected fields and keep past value if input is left blank

    def run_reports(self):
        while True:
            print("\nReports Menu") #shows report menus
            print("3.1 - List of friends alphabetically")
            print("3.2 - List of friends by upcoming birthdays")
            print("3.3 - Mailing labels")
            print("3.9 - Return to previous menu")
            choice = input("Enter choice: ") #Options listed

            if choice == "3.1": #3.1, 3.2, 3.3, 3.4 are submenus for reports
                for f in sorted(self.friends, key=lambda x: (x.last_name, x.first_name)): #sorts and prints alphabetically by first and last name
                    print(f)
            elif choice == "3.2":
                sorted_birthdays = sorted(self.friends, key=lambda f: f._birthday.days_until() if f._birthday else 999) #sorts by how soon their birthday is coming
                for f in sorted_birthdays:
                    print(f"{f} - in {f._birthday.days_until()} days")
            elif choice == "3.3":
                for f in self.friends:
                    print(f"{f.first_name} {f.last_name}\n{f.street_address}\n{f.city}, {f.state} {f.zip}\n") #prints each friend in mail label format
            elif choice == "3.4":
                break #exits report
            else:
                print("Invalid choice.") #for invalid chossing in menu

    def main_menu(self):
        self.load_from_file() #loads data when app starts
        while True:
            print("\nMy Friends App")
            print("1 - Create new friend record")
            print("2 - Search for a friend")
            print("3 - Run reports")
            print("4 - Exit")
            choice = input("Choose an option: ") # shows menu and these are the options

            if choice == "1":
                self.create_friend()
            elif choice == "2":
                self.search_friend()
            elif choice == "3":
                self.run_reports()
            elif choice == "4":
                self.save_to_file()
                print("Goodbye!")
                break
            else:
                print("Invalid selection.") #routes input answer to respective menu choise and saves data when exiting


if __name__ == "__main__":
    app = MyFriendsApp()
    app.main_menu()
