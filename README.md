# PHONEBOOK - FASTAPI

This is a FastAPI application for managing a phonebook.

## Installation and Setup Instructions

This guide provides step-by-step instructions on how to install and run the application on a local server. The application is built using FastAPI.

## Prerequisites

Before proceeding with the installation, ensure that you have the following:

* Python (version 3.7 or higher) installed on your system
* 'pip' package manager installed

## Installation

1. Clone the repository from GitHub:
```console
git clone <repository_url>
```
2. Navigate to the project directory:
```console
cd <project_directory>
```
Remember to replace <project_directory> with the path to your project directory.
3. Create and activate a new virtual environment:
```console
# Create a new virtual environment
python3 -m venv venv

# Activate the virtual environment for Windows
venv\Scripts\activate

# Activate the virtual environment for macOS/Linux
source venv/bin/activate
```
4. Install the project dependencies using 'pip' and the provided 'requirements.txt' file:
```console
pip install -r requirements.txt
```
5. Create a '.env' file in the root directory of the project. The file should follow the format:
```console
USERNAME=your_login
PASSWORD=your_password
```
Replace 'your_login' and 'your_password' with your desired values.

## Running the Application

1. Start the local server by running the following command:
```console
uvicorn main:app --reload
```
The application should now be running locally on http://127.0.0.1:8000.
2. Open your web browser and navigate to http://127.0.0.1:8000/docs to access the API documentation.

## Usage
* <b>Homepage:</b> Visit http://127.0.0.1:8000/ to view the list of contacts.
* <b>Create Contact:</b> Navigate to http://127.0.0.1:8000/contact/create to create a new contact.
* <b>View Contact:</b> To view a specific contact, go to http://127.0.0.1:8000/contact/{id}, where <b>{id}</b> is the ID of the contact.
* <b>Edit Contact:</b> Edit a contact by accessing http://127.0.0.1:8000/contact/{id}/edit, where <b>{id}</b> is the ID of the contact you want to edit.
* <b>Delete Contact:</b> Delete a contact by going to http://127.0.0.1:8000/contact/{id}/delete, where <b>{id}</b> is the ID of the contact you want to delete.

<b>Note:</b> Make sure to replace <b>{id}</b> in the URLs above with the actual ID of the contact you want to interact with.

That's it! You have successfully installed and set up the application on your local server. Enjoy using the app!

## License
This project is licensed under the terms of the MIT license.