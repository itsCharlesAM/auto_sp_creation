import os
import pyodbc
import chardet


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']


def execute_sql_batches(cursor, sql_script):
    # Split the script into batches by 'GO' (case-insensitive, surrounded by newlines)
    batches = [batch.strip()
               for batch in sql_script.split('\nGO\n') if batch.strip()]
    for batch in batches:
        try:
            cursor.execute(batch)
        except Exception as e:
            print(f"Error executing batch: {batch[:100]}... \nError: {e}")


def create_stored_procedures(server, database, username, password, sql_files_directory):
    try:
        # Connect to the SQL Server
        connection = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        )
        cursor = connection.cursor()
        print(f"Connected to server: {server}, database: {database}")

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

                # Replace the USE statement with the target database name
                sql_script = sql_script.replace(
                    "USE [T0db01]", f"USE [{database}]")

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
server = "185.252.86.138"  # Replace with your SQL Server name or IP
database = "dbname"  # Replace with your target database name
username = "username"  # Replace with your SQL Server username
password = "password"  # Replace with your SQL Server password

# Replace with the path to your .sql files
sql_files_directory = r"path"

# Call the function
create_stored_procedures(server, database, username,
                         password, sql_files_directory)
