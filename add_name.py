import json

# Function to add a 'name' key with an empty value to each user entry
def add_name_key_to_file(file_path):
    # Open the JSON file and load its data
    with open(file_path, 'r+') as file:
        user_data = json.load(file)
        
        # Add a 'name' key with an empty value to each user entry
        for user_id in user_data:
            user_data[user_id]['name'] = ''  # Add 'name' key with empty value
        
        # Move the file pointer to the beginning of the file
        file.seek(0)
        # Write the updated data back to the file
        json.dump(user_data, file, indent=4)
        # Truncate the file to the new size
        file.truncate()

# Path to your userdata.json file
file_path = 'C:/Users/JAILOR/Desktop/Git/V5/user_data.json'

# Call the function with the path to your userdata.json file
add_name_key_to_file(file_path)
