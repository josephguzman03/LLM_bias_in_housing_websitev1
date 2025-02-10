import pandas as pd
import sqlite3

def convert_csv_to_sql():
    csv_file_path = 'housing_prompt_v1_allmodels copy.csv'   # Path to your CSV file
    db_path = 'prompt_database.db'  # This will be the new database created

    # Read data from CSV
    try:
        data = pd.read_csv(csv_file_path)
        print("CSV Load Success: Data loaded successfully!")
    except Exception as e:
        print(f"Error loading CSV data: {e}")
        return

    # Connect to SQLite database
    try:
        conn = sqlite3.connect(db_path)
        print("Database Connection Established!")

        # Convert DataFrame to SQL
        data.to_sql('Prompts', conn, if_exists='replace', index=False)
        print("Data successfully written to the database.")

    except Exception as e:
        print(f"Error with database operation: {e}")

    finally:
        conn.close()
        print("Database connection closed.")

convert_csv_to_sql()


