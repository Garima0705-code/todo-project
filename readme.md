🚀 Cruzer To-Do Manager

A modern desktop To-Do List application built with Python and CustomTkinter.
Cruzer To-Do Manager helps users create, organize, search, filter, edit, complete, and delete tasks through a clean and responsive graphical interface.

✨ Features

📝 Add new tasks

🎯 Set task priority: Low, Medium, High

📅 Add and validate due dates in YYYY-MM-DD format

✅ Mark tasks as completed or pending

✏️ Edit existing tasks

🗑️ Delete selected tasks

🧹 Clear all tasks with confirmation

🔎 Search tasks by keywords

🔽 Filter tasks by:

All

Pending

Completed

High Priority

🖱️ Drag and drop tasks to reorder them

🌙 Light and Dark mode

📊 Live task statistics showing total, completed, and pending tasks

💾 Automatic local data persistence using tasks.json

⌨️ Keyboard shortcuts for faster task management

🎨 Modern GUI built with CustomTkinter

🛠️ Tech Stack

Language: Python 3

GUI Framework: CustomTkinter

Standard Libraries: json, os, datetime, tkinter

Data Storage: JSON file

📁 Project Structure

PP Project/
│
├── cruzer_todo_manager.py   # Main application
├── tasks.json               # Local task data
└── README.md                # Project documentation

⚙️ Installation

1. Clone the repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "PP Project"

2. Install the required dependency

Make sure Python 3 is installed, then run:

pip install customtkinter

3. Run the application

python cruzer_todo_manager.py

The Cruzer To-Do Manager window will open on your desktop.

📌 How to Use

Add a Task

Enter a task name, select a priority, optionally enter a due date, and click Add Task.

Example:

Task: Complete DBMS assignment
Priority: High
Due Date: 2026-10-10

Manage Tasks

Select a task card and use:

Edit to modify the task

Complete to change its completion status

Delete to remove the task

You can also use the checkbox directly on a task card.

Search and Filter

Use the search box to find tasks by keyword and combine it with the filter menu for quicker results.

Reorder Tasks

Drag a task card and drop it onto another task to change the order.

⌨️ Keyboard Shortcuts

Shortcut

Action

Ctrl + Enter

Add task

Delete

Delete selected task

Ctrl + D

Complete / uncomplete selected task

Ctrl + F

Focus search box

Ctrl + L

Clear all tasks

💾 Data Storage

Tasks are stored locally in tasks.json. Each task contains information such as:

{
  "id": "unique-id",
  "text": "Complete assignment",
  "completed": false,
  "priority": "High",
  "due_date": "2026-10-10",
  "created_at": "2026-10-01 18:30"
}

No external database is required.

🎨 Themes

The application supports:

☀️ Light Mode

🌙 Dark Mode

Use the Dark Mode switch in the application header to change the appearance.

🔐 Validation & Error Handling

The application includes basic validation and error handling for:

Empty task names

Invalid due-date formats

Missing task selection for edit/delete/complete actions

Invalid or corrupted tasks.json data

File read/write errors

📦 Requirements

Python 3.9+ recommended

customtkinter

Install the dependency with:

pip install customtkinter

🚀 Future Improvements

Possible future enhancements include:

Task categories and tags

Notifications and reminders

Recurring tasks

Sorting by priority or due date

Export/import functionality

SQLite database support

User accounts and authentication

Cross-platform packaging as an executable

👩‍💻 Author

Garima Bhardwaj

B.Tech CSE

⭐ If you find this project useful, consider giving the repository a star!