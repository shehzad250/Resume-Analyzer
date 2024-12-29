# import sqlite3

# # Database path (update this if your database is located elsewhere)
# DATABASE_PATH = 'D:/ResumeAnalyzer/database.db'

# def insert_sample_feedback():
#     try:
#         # Connect to the database
#         conn = sqlite3.connect(DATABASE_PATH)
#         cursor = conn.cursor()

#         # Sample feedback entries
#         feedback_entries = [
#             ('John Doe', '2024-11-15', 'Great application!'),
#             ('Jane Smith', '2024-11-15', 'The UI is fantastic!'),
#             ('Alice Johnson', '2024-11-15', 'Loved the analysis feature!'),
#         ]

#         # Insert data into feedback_table
#         cursor.executemany(
#             "INSERT INTO feedback_table (username, date, feedback_text) VALUES (?, ?, ?)",
#             feedback_entries
#         )

#         # Commit changes and close the connection
#         conn.commit()
#         print("Sample feedback entries inserted successfully!")
#     except sqlite3.Error as e:
#         print(f"Error inserting data: {e}")
#     finally:
#         conn.close()

# if __name__ == '__main__':
#     insert_sample_feedback()
