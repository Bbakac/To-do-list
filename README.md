# To Do List Application

This project is a To Do List application that allows users to manage their tasks. Users can add, update, delete, and archive tasks. Additionally, it provides secure user registration and login features.

## Features

- User registration and login
- Add, update, and delete tasks
- Toggle task completion status
- Filter tasks (completed/not completed)
- Filter tasks by priority
- Sort tasks by date
- View archived tasks
- Static file support

## Technologies

- **Backend**: FastAPI
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript

## Requirements

- Python 3.7 or higher
- Uvicorn
- FastAPI
- SQLAlchemy
- Passlib

Install the required libraries:
pip install fastapi uvicorn sqlalchemy passlib

Running the Application
To start the FastAPI application, use the following command:
uvicorn fastAPI:app --reload

##Usage

Homepage: Fill in the fields to add a task and click the "Add Task" button.
Register: Follow the "Register" link to create a new user account.
Login: If you already have an account, use the "Login" link to access your account.
