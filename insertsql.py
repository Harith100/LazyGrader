import pymysql

def insert_to_ai(data_sql):
    """
    Inserts a record into the AI table in the MySQL database.
    
    Args:
        data_sql (dict): A dictionary containing the following keys:
            - barcode (str): The Barcode ID.
            - subject_id (str): The Subject ID.
            - Q1_Marks (int): Marks for Question 1.
            - Q2_Marks (int): Marks for Question 2.
            - Q3_Marks (int): Marks for Question 3.
            - Q4_Marks (int): Marks for Question 4.
    """
    # Database connection details
    db_config = {
        "host": "localhost",
        "user": "root",      # Replace with your MySQL username
        "password": "root",  # Replace with your MySQL password
        "database": "university"      # Replace with your MySQL database name
    }

    # SQL query for inserting data
    insert_query = """
        INSERT INTO AI (BarcodeID, SubjectID, Q1_Marks, Q2_Marks, Q3_Marks, Q4_Marks)
        VALUES (%(barcode)s, %(subject_id)s, %(Q1_Marks)s, %(Q2_Marks)s, %(Q3_Marks)s, %(Q4_Marks)s)
    """

    try:
        # Establish connection to the database
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Execute the insert query
            cursor.execute(insert_query, data_sql)
            connection.commit()
            print("Data successfully inserted into the AI table.")
    except pymysql.MySQLError as e:
        # Rollback transaction in case of error
        connection.rollback()
        print(f"Failed to insert data into the AI table: {e}")
    finally:
        # Close the database connection
        connection.close()

# Example usage
if __name__ == "__main__":
    # Example data_sql dictionary
    data_sql = {
        "barcode": "502101175922",
        "subject_id": "AIT301",
        "Q1_Marks": 12,
        "Q2_Marks": 18,
        "Q3_Marks": 12,
        "Q4_Marks": 20,
    }

    # Call the function to insert data
    insert_to_ai(data_sql)
