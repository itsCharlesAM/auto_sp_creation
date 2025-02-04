# Auto Execute SQL Scripts in SQL Server

If you have problem with creating a lot of Stored Procedures (or any other `.sql` scripts) on serveral databases, you are in the right place!

This Python script reads `.sql` files from a specified directory and executes them on a Microsoft SQL Server database. It supports encoding detection and batch execution using `pyodbc`.

## Features

- **Auto Encoding Detection**: Detects file encoding using `chardet` to prevent encoding issues.
- **Batch Execution**: Splits SQL scripts by `GO` statements and executes them safely.
- **Dynamic Database Selection**: Replaces `USE [previous_databse]` with the target database name.
- **Error Handling**: Logs execution errors without stopping the entire process.

## Requirements

- `Python 3.x`
- `pyodbc`
- `chardet`
- `Microsoft ODBC Driver for SQL Server`

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/itsCharlesAM/auto_sp_creation.git

2. Install dependencies:
   ```sh
   pip install pyodbc chardet

## Usage
1. Update the script with your SQL Server credentials:
   ```sh
    server = "your_server"
    database = "your_database"
    username = "your_username"
    password = "your_password"
    sql_files_directory = r"your_sql_files_directory"

2. Run the script:
   ```sh
    python script.py

## Notes
- Ensure the `.sql` files in `sql_files_directory` are correctly formatted.
- Requires `ODBC Driver 17 for SQL Server` installed on the system.
- Handles encoding issues automatically.
