import json
import datetime
import os
from time import sleep
from whatsapp import WhatsApp

from pywinauto.keyboard import send_keys

try:
    with open('user_data.json', 'r') as f:
        user_data = json.load(f)
except FileNotFoundError:
    # If the file doesn't exist, start with an empty dictionary
    user_data = {}

def store_data():
    user_id = input("Enter User ID: ")
    if user_id in user_data: 
        print("User already exists.")
    else:
        value1 = input("Enter No1: ")
        value2 = input("Enter No2: ")
        value3 = input("Enter No3: ")
        user_data[user_id] = {'1': value1, '2': value2, '3': value3}
        # Write the updated data to the file
        with open('user_data.json', 'w') as f:
            json.dump(user_data, f,indent=4)

def retrieve_data():
    enter_calls = input("Choose Calls (1/2): ")
    
    if enter_calls == '1':
        user_id = input("Enter User ID: ")
        if user_id in user_data:
            print("choose (1, 2, or 3):", user_data[user_id])
            field = input("Enter field to print (or 'all' to print all fields): ")
            if field.lower() == 'all':
                print(user_data[user_id]["name"])
            elif field in user_data[user_id]:
                add_time = float(input("enter time:: "))
                if add_time <= 12:
                    wa = WhatsApp(user_data[user_id][field], add_time)
                    wa.run_method()
                    add_timer1 = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    print(f"{user_data[user_id][field]} (Called at {add_timer1})")
                    
                    # Get the path to the last recording
                    recordings_folder = r'C:\Users\JAILOR\Documents\Bandicam'
                    recording_files = os.listdir(recordings_folder)
                    last_recording = sorted(recording_files)[-1]  # Assumes files are named in a way that allows sorting
                    
                    timestamped_data = {
                        "user_id": user_id,
                        "name" : user_data[user_id]["name"],
                        "field": field,
                        "number": user_data[user_id][field],
                        "timestamp": add_timer1,
                        "recording": os.path.join(recordings_folder, last_recording)
                    }
                    
                    with open('timestamped_data.json', 'a') as f:
                        json.dump(timestamped_data, f)
                        f.write('\n')  # Add a newline for readability
                    
                    # Open the recording file
                    #os.startfile(timestamped_data["recording"])
                else:
                    print("Time Limit Can't Exceed more than 10 Min")
            else:
                print("Invalid Field")
        else:
            print("User not found.")
      
    if enter_calls=='2':
        user_id = input("Enter User ID: ")
        if user_id in user_data:
            print("choose (1, 2, or 3):", user_data[user_id])
            field1 = input("Enter field to print (or 'all' to print all fields): ")
            field2 = input("Enter field to print (or 'all' to print all fields): ")
            if field1  in user_data[user_id]:
                add_time1=float(input("enter time:: "))
                add_time2=float(input("enter time:: "))
                wa=WhatsApp(user_data[user_id][field1],add_time1)
                wa.run_method() 
                add_timer2 = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                print(f"{user_data[user_id][field1]} (Called at {add_timer2})")

                recordings_folder = r'C:\Users\JAILOR\Documents\Bandicam'
                recording_files = os.listdir(recordings_folder)
                last_recording = sorted(recording_files)[-1]  # Assumes files are named in a way that allows sorting
                    
            # Create a new dictionary to store timestamped data
                timestamped_data = {
                    "user_id": user_id,
                    "field": field1,
                    "number": user_data[user_id][field2],
                    "timestamp": add_timer2,
                    "recording": os.path.join(recordings_folder, last_recording)
                }
                with open('timestamped_data.json', 'a') as f:
                    json.dump(timestamped_data, f)
                    f.write('\n')  # Add a newline for readability
                sleep(1)
                send_keys("^%{VK_NUMPAD0}")
                sleep(3)
                wa=WhatsApp(user_data[user_id][field2],add_time2)
                wa.run_method()
                add_timer3 = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                print(f"{user_data[user_id][field2]} (Called at {add_timer3})")


                recordings_folder = r'C:\Users\JAILOR\Documents\Bandicam'
                recording_files = os.listdir(recordings_folder)
                last_recording = sorted(recording_files)[-1]


                timestamped_data = {
                    "user_id": user_id,
                    "field": field2,
                    "number": user_data[user_id][field2],
                    "timestamp": add_timer3,
                    "recording": os.path.join(recordings_folder, last_recording)
                }
            # Write the timestamped data to a new file
                with open('timestamped_data.json', 'a') as f:
                    json.dump(timestamped_data, f)
                    f.write('\n')  # Add a newline for readability
            else:
                print("Invalid field.")
        else:
            print("User not found.")
    else:
        print("invalid option")  
def print_timestamped_data(user_id): 
    try:
        with open('timestamped_data.json', 'r') as f:
            data_found = False  # Flag to track if data exists for the user ID
            for line in f:
                entry = json.loads(line)  # Parse each line as a separate JSON object
                if entry['user_id'] == user_id:
                    print("-------------------------------------             ")
                    print(f"User ID: {entry['user_id']}")
                    print(f"Field: {entry['field']}")
                    print(f"Value: {entry['number']}")  # Corrected key name
                    print(f"Timestamp: {entry['timestamp']}\n")
                    print("-------------------------------------             ")
                    data_found = True  # Data exists for the specified user ID
            if not data_found:
                print("No data found for the specified user ID.")
    except FileNotFoundError:
        print("No timestamped data file found.")
# Example usage:

while True:
    print("         -------------------------------------             ")
    print("             WELCOME TO PUZHAL PHONE PORTAL              ")
    print("           ----------------------------------             ")
    print("\n1. Store Data\n2. Make Call\n3. Search Data\n4. Quit")
    option = input("Enter your option: ")
    if option == '1':
        store_data()
    elif option == '2':
        retrieve_data()
    elif option == '3':
        user_id_input = input("Enter User ID to retrieve data: ")
        print_timestamped_data(user_id_input)
    elif option == '4':
        break
    else:
        print("Invalid option. Please try again.")
 
