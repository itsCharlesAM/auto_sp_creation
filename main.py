import os
import pyodbc
import chardet
import re


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']


def execute_sql_batches(cursor, sql_script):
    # Normalize line endings and split by GO surrounded by newlines (case-insensitive)
    batches = re.split(r'(?im)^\s*GO\s*$', sql_script, flags=re.MULTILINE)
    for batch in batches:
        batch = batch.strip()
        if batch:
            try:
                cursor.execute(batch)
            except Exception as e:
                print(f"Error executing batch:\n{batch[:100]}...\nError: {e}")


def create_stored_procedures(server, database, username, password, sql_files_directory):
    try:
        # Connect to the SQL Server
        connection = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        )
        cursor = connection.cursor()

        # Confirm connected database
        cursor.execute("SELECT DB_NAME() AS CurrentDatabase")
        row = cursor.fetchone()
        print(
            f"Connected to server: {server}, database: {row.CurrentDatabase}")

        # Iterate over all .sql files in the specified directory
        for filename in os.listdir(sql_files_directory):
            if filename.endswith(".sql"):
                file_path = os.path.join(sql_files_directory, filename)
                print(f"Processing file: {filename}")

                # Detect file encoding
                encoding = detect_encoding(file_path)
                print(f"Detected encoding for {filename}: {encoding}")

                # Read the SQL file content with the correct encoding
                with open(file_path, "r", encoding=encoding) as sql_file:
                    sql_script = sql_file.read()

                # Remove any existing USE [SomeDatabase] statements
                sql_script = re.sub(
                    r'(?i)^\s*USE\s+\[.*?\]\s*\n?', '', sql_script)

                # Insert the correct USE [DB] and GO at the top
                sql_script = f"USE [{database}]\nGO\n{sql_script.strip()}"

                # Execute the SQL script in batches
                try:
                    execute_sql_batches(cursor, sql_script)
                    connection.commit()
                    print(
                        f"Stored procedure from {filename} created successfully.")
                except Exception as e:
                    print(f"Error executing file {filename}: {e}")

        cursor.close()
        connection.close()
        print("All files processed successfully.")

    except Exception as ex:
        print(f"Failed to connect to the server: {ex}")


# Input parameters
server = "*****"
database = "*****"
username = "*****"
password = "*****"

# Directory containing your .sql files
sql_files_directory = r"D:\Softwares\Neco App\SPs"

# Call the function
create_stored_procedures(server, database, username,
                         password, sql_files_directory)
