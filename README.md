# Task Manage

**Task Manage** is a Python-based task management tool built with PyQt5. It helps you organize your to-do list using three categories: **Active**, **Completed**, and **Trash**. Tasks can be freely moved among these tabs. The application also supports global font size adjustment and saves daily task logs (in JSON format) to keep track of task modifications, completion status, and timestamps.

## Features

- **Task Management**
  - **Add Tasks:** Add new tasks in the Active tab.
  - **Edit Tasks:** Modify tasks by double-clicking on an item or using a context menu. (will be updated in next commit)
  - **Task Status Changes:**  
    - Mark tasks as completed (moves them from Active to Completed).  
    - Delete tasks (if entered incorrectly, move them to Trash; completed tasks can also be deleted to Trash).  
    - Restore tasks from Trash or Completed back to Active.
- **Global Font Adjustment**
  - Change the font size across all tabs and widgets dynamically using a QSpinBox.
- **Daily Log Storage**
  - Tasks are saved daily with a JSON file (named using the current date) that records task text, status, unique IDs, and timestamps.

## Requirements

- Python 3.x
- PyQt5

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/task-manage.git
   cd task-manage
