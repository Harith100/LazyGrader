import pymysql
import barcode
from barcode.writer import ImageWriter

class StudentBarcodeGenerator:
    def __init__(self, db_host, db_user, db_password, db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name

    def fetch_student_data(self):
        try:
            # Connect to MySQL using pymysql
            connection = pymysql.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )

            with connection.cursor() as cursor:
                # Query to fetch all UniversityID and Barcode from the Barcode table
                cursor.execute("""SELECT UniversityID, BarcodeID FROM Barcode""")
                students_data = cursor.fetchall()

            return students_data

        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            return []

        finally:
            if 'connection' in locals() and connection.open:
                connection.close()

    def generate_barcode(self, university_id, barcode_number):
        # Generate barcode using python-barcode
        code128 = barcode.get_barcode_class('code128')
        barcode_instance = code128(barcode_number, writer=ImageWriter())

        # Save the barcode image as a PNG file
        barcode_image_path = f"{university_id}_barcode.png"
        barcode_instance.save(barcode_image_path)

        print(f"Barcode for Student {university_id} saved as {barcode_image_path}")

    def generate_barcodes_for_all_students(self):
        students_data = self.fetch_student_data()

        if not students_data:
            print("No student data found.")
            return

        for student in students_data:
            university_id = student[0]
            barcode_number = student[1]
            
            self.generate_barcode(university_id, barcode_number)

# Example usage
if __name__ == "__main__":
    # Database connection details
    DB_HOST = 'localhost'
    DB_USER = 'root'  # Replace with your MySQL username
    DB_PASSWORD = 'root'  # Replace with your MySQL password
    DB_NAME = 'university'  # Replace with your database name

    # Create an instance of the StudentBarcodeGenerator class
    barcode_generator = StudentBarcodeGenerator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    
    # Generate barcodes for all students
    barcode_generator.generate_barcodes_for_all_students()
