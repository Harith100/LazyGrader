import pymysql
import barcode
from barcode.writer import ImageWriter

# Function to fetch student data and generate barcode images
def generate_barcode_for_all_students():
    try:
        # Connect to MySQL using pymysql
        connection = pymysql.connect(
            host='localhost',        # Your MySQL host (e.g., 'localhost')
            database='university',   # Your database name
            user='root',    # Your MySQL username
            password='root' # Your MySQL password
        )

        with connection.cursor() as cursor:
            # Query to fetch all UniversityID and Barcode from the Answer_Sheets table
            cursor.execute("""
                SELECT University_ID, Barcode FROM Answer_Sheets
            """)
            students_data = cursor.fetchall()

            # Iterate over each student and generate barcode image
            for student in students_data:
                university_id = student[0]
                barcode_number = student[1]
                
                # Generate barcode using python-barcode
                code128 = barcode.get_barcode_class('code128')
                barcode_instance = code128(barcode_number, writer=ImageWriter())

                # Save the barcode image as a PNG file
                barcode_image_path = f"{university_id}_barcode.png"
                barcode_instance.save(barcode_image_path)

                print(f"Barcode for Student {university_id} saved as {barcode_image_path}")

    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    
    finally:
        connection.close()

# Call the function to generate barcodes for all students
generate_barcode_for_all_students()
