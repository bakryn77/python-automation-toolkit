import json #library for handling JSON data
import os #library for handling file paths and checking file existence

FILE_NAME = "contacts.json" #constant for the file name where contacts are stored

def load_data(): #loads contacts from the file
    """Loads the contacts from the file if it exists."""
    if os.path.exists(FILE_NAME): # Check if the file exists
        try: # Try to open the file and load the contacts
            with open(FILE_NAME, "r") as f: # Open the file in read mode
                return json.load(f) # Load the contacts from the file
        except json.JSONDecodeError: # Handle JSON decoding errors
            return [] # Return empty list if file is corrupted
    return [] # Return empty list if file does not exist

def save_data(contacts): #saves contacts to the file
    """Saves the list of contacts to the file."""
    with open(FILE_NAME, "w") as f: # Open the file in write mode
        json.dump(contacts, f, indent=4) # Write the contacts to the file in JSON format with indentation for readability

def add_contacts(contacts): #adds a new contact to the list
    print("\n--- ADD NEW CONTACT ---")
    """Adds a new contact to the list."""
    name = input("enter name: ").strip() # Get the name from user input and remove leading/trailing whitespace
    email = input("enter email: ").strip() # Get the email from user input and remove leading/trailing whitespace
    phone_raw = input("enter phone number: ").strip() # Get the phone number from user input and remove leading/trailing whitespace
    digits = "".join(ch for ch in phone_raw if ch.isdigit()) # Extract only digits from the phone number input

    if len(digits) == 10: # Check if the phone number has exactly 10 digits
        phone = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}" # Format the phone number as (XXX) XXX-XXXX
    else:
        print("Warning: phone number not 10 digits; saving raw input.") # If the phone number is not 10 digits, save the raw input
        phone = phone_raw # Use the raw input as the phone number

    person = { # Create a dictionary to store the contact information
        "name": name,
        "phone": phone,
        "email": email,
    }

    contacts.append(person) # Add the new contact to the list of contacts
    save_data(contacts) # Save the updated list of contacts to the file
    print(f"{name} added successfully!") # Confirmation message after adding the contact

def find_contact(contacts): #finds a contact by name
    """Search for a person by name"""""
    search_name = input("enter name: ").lower() # Get the name to search for from user input and convert it to lowercase for case-insensitive search

    found = False # Flag to check if any contact is found
    for person in contacts: # Iterate through the list of contacts
        if search_name in person["name"].lower(): # Check if the search name is in the contact's name (case-insensitive)
            print(f"\n--- MATCH FOUND ---") # Text to indicate a match has been found
            print(f"Name: {person['name']}") # Print the name of the found contact
            print(f"Phone: {person['phone']}") # Print the phone number of the found contact
            print(f"Email: {person['email']}") # Print the email of the found contact
            found = True  # Set the flag to True if a contact is found

        if not found: # If no contact was found after checking all contacts
            print("No contact found with that name.") # Print a message indicating no contact was found

def view_contacts(contacts): #views all contacts
    """Displays all contacts in the rolodex."""
    if not contacts: # Check if the contacts list is empty
        print("No contacts available.") # Print a message indicating no contacts are available
        return

    print("\n--- ALL CONTACTS ---") # Text to indicate the start of the contact list
    for person in contacts: # Iterate through the list of contacts
        print(f"Name: {person['name']}") # Print the name of the contact
        print(f"Phone: {person['phone']}") # Print the phone number of the contact
        print(f"Email: {person['email']}") # Print the email of the contact
        print("--------------------") # Separator between contacts

def delete_contact(contacts): #deletes a contact by name
    """Deletes a contact by name"""
    name_to_delete = input("Who do you want to delete?: ").lower()

    found = False # Flag to check if any contact is found
    for person in contacts: # Iterate through the list of contacts
        if name_to_delete in person["name"].lower(): # Check if the name to delete is in the contact's name (case-insensitive)
            contacts.remove(person) # Remove the contact from the list
            save_data(contacts) # Save the updated list of contacts to the file
            print(f"{person['name']} deleted successfully!") # Confirmation message after deleting the contact
            found = True  # Set the flag to True if a contact is found
            break

def main(): #main function to run the rolodex program
    contacts = load_data() # Load existing contacts from the file

    while True: # Start an infinite loop to keep the program running
        print("\n=== 📇 THE ROLODEX ===") # Text to indicate the start of the Rolodex program
        print(f"You have {len(contacts)} contacts saved.") # Print the number of contacts saved
        print("1. Add Contact") # Option to add a new contact
        print("2. Find Contact") # Option to find a contact by name
        print("3. View Contacts") # Option to view all contacts
        print("4. Delete Contact") # Option to delete a contact by name
        print("5. Exit") # Option to exit the program

        choice = input("Choose (1/2/3/4/5): ") # Get the user's choice from input

        if choice == "1":
            add_contacts(contacts)  # Pass the list to the function
        elif choice == "2":
            find_contact(contacts)  # Pass the list to the function
        elif choice == "3":
            view_contacts(contacts)
        elif choice == "4":
            delete_contact(contacts)  # Pass the list to the function
        elif choice == "5":
            print("Goodbye! Data saved.")
            break  # <--- This Breaks the Loop and ends the program
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__": # Check if the script is being run directly
    main() # Call the main function to start the Rolodex program
