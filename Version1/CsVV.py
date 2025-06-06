import pymysql
import csv

class UniversityDataExporter:
    def __init__(self, db_host, db_user, db_password, db_name, output_csv):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.output_csv = output_csv

    def fetch_data(self):
        try:
            # Connect to the database
            connection = pymysql.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            print("Connected to the database successfully!")

            # SQL query to fetch the required data
            query = """
            SELECT 
                Students.UniversityID,
                Students.Name,
                Students.Email,
                AI.Q1_Marks,
                AI.Q2_Marks,
                AI.Q3_Marks,
                AI.Q4_Marks,
                AI.Total,
                AI.SubjectID,
                Subject.SubjectName
            FROM 
                Students
            JOIN 
                Barcode ON Students.UniversityID = Barcode.UniversityID
            JOIN 
                AI ON Barcode.BarcodeID = AI.BarcodeID
            JOIN 
                Subject ON AI.SubjectID = Subject.SubjectID;
            """

            # Execute the query and fetch data
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                # Get column names from the cursor
                column_names = [desc[0] for desc in cursor.description]

            return column_names, rows

        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            return None, None

        finally:
            if 'connection' in locals() and connection.open:
                connection.close()
                print("Database connection closed.")

    def export_to_csv(self, column_names, rows):
        try:
            # Write data to CSV
            with open(self.output_csv, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write header row
                writer.writerow(column_names)
                # Write data rows
                writer.writerows(rows)

            print(f"Data exported successfully to {self.output_csv}!")

        except Exception as e:
            print(f"Error writing to CSV: {e}")

    def fetch_and_export_data(self):
        column_names, rows = self.fetch_data()
        if column_names and rows:
            self.export_to_csv(column_names, rows)

# Example usage
if __name__ == "__main__":
    # Database connection details
    DB_HOST = 'localhost'
    DB_USER = 'root'  # Replace with your MySQL username
    DB_PASSWORD = 'root'  # Replace with your MySQL password
    DB_NAME = 'university'

    # CSV file path
    OUTPUT_CSV = 'students_data.csv'

    # Create an instance of the UniversityDataExporter class
    data_exporter = UniversityDataExporter(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, OUTPUT_CSV)
    # Fetch data and export it to CSV
    data_exporter.fetch_and_export_data()
