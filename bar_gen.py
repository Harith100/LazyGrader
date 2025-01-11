#barcode generator
import barcode
from barcode.writer import ImageWriter
from PIL import Image

# Function to generate barcode and return both the image and code
def generate_barcode(code_data, filename):
    # Use 'code128' format (or 'itf' for Interleaved 2 of 5)
    barcode_format = barcode.get_barcode_class('code128')  # or 'itf' for interleaved 2 of 5
    
    # Create the barcode object
    barcode_obj = barcode_format(code_data, writer=ImageWriter())
    
    # Save the barcode as an image
    barcode_obj.save(filename)
    
    # Open the image using Pillow
    img = Image.open(f"{filename}.png")
    img.show()  # Display the barcode image
    
    # Return the barcode data (code)
    return code_data

# Example usage
barcode_data = "12345"  # 5-digit barcode data
filename = "barcode_5digit"

generated_code = generate_barcode(barcode_data, filename)
print("Generated Barcode Code:", generated_code)