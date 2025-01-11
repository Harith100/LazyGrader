import random
import string
import pymysql

# Class for handling barcode generation
class BarcodeGenerator:
    def __init__(self, barcode_length=12):
        self.barcode_length = barcode_length

    # Function to generate a unique barcode number
    def generate_unique_barcode(self, barcode_number):
        while True:
            # Check if the barcode already exists
            if not self.is_barcode_exist(barcode_number):
                return barcode_number
            else:
                # Generate a new barcode if the current one already exists
                barcode_number = self._generate_random_barcode()

    # Function to generate a random barcode
    def _generate_random_barcode(self):
        return ''.join(random.choices(string.digits, k=self.barcode_length))

    # Function to check if the barcode exists in the Barcode table
    def is_barcode_exist(self, barcode):
        try:
            # Connect to MySQL using pymysql
            connection = pymysql.connect(
                host='localhost',        # Your MySQL host (e.g., 'localhost')
                database='university',   # Your database name
                user='root',    # Your MySQL username
                password='root' # Your MySQL password
            )

            with connection.cursor() as cursor:
                # Query to check if the barcode exists in the Barcode table
                query = "SELECT COUNT(*) FROM Barcode WHERE BarcodeID = %s"
                cursor.execute(query, (barcode,))

                # If barcode exists, return True, else return False
                count = cursor.fetchone()[0]
                return count > 0

        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            return True
        finally:
            connection.close()


# Function to register a new student and generate a unique barcode
def register_student(student_name, university_id, email, barcode_number=None):
    try:
        # Instantiate BarcodeGenerator class
        barcode_generator = BarcodeGenerator()

        # If barcode_number is provided, use that, else generate a new one
        if barcode_number is None:
            barcode_number = barcode_generator._generate_random_barcode()

        # Generate a unique barcode using the provided or generated barcode number
        barcode = barcode_generator.generate_unique_barcode(barcode_number)

        # Connect to MySQL using pymysql
        connection = pymysql.connect(
            host='localhost',        # Your MySQL host (e.g., 'localhost')
            database='university',   # Your database name
            user='root',    # Your MySQL username
            password='root' # Your MySQL password
        )

        with connection.cursor() as cursor:
            # Insert the student data into the Students table
            cursor.execute("""
                INSERT INTO Students (UniversityID, Name, Email)
                VALUES (%s, %s, %s)
            """, (university_id, student_name, email))

            # Insert the barcode and university ID into the Barcode table
            cursor.execute("""
                INSERT INTO Barcode (UniversityID, BarcodeID)
                VALUES (%s, %s)
            """, (university_id, barcode))

            # Commit the transaction
            connection.commit()

            print(f"Student {student_name} registered successfully with Barcode: {barcode}")

    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    
    finally:
        connection.close()


# Call the register_student function
register_student('Harith Hussain', '12121', 'harithhus123@gmail.com')

