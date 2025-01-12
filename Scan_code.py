from pyzbar.pyzbar import decode
import cv2

def scan_barcode_from_image(image_path):
    """
    Scans the barcode from an image file and returns the decoded data.

    Parameters:
        image_path (str): Path to the image file containing the barcode.

    Returns:
        str: Decoded barcode data if a barcode is found, otherwise None.
    """
    try:
        # Load the image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Unable to load image. Please check the image path.")

        # Decode the barcode(s) in the image
        barcodes = decode(image)
        
        if not barcodes:
            print("No barcode found in the image.")
            return None

        for barcode in barcodes:
            # Decode the barcode data
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type

            print(f"Barcode found: {barcode_data} (Type: {barcode_type})")
            return barcode_data  # Return the first barcode's data

    except Exception as e:
        print(f"Error scanning barcode: {e}")
        return None
image_path = r"C:\Users\Rohit Francis\Documents\GitHub\LazyGrader\12121_barcode.png.png"  # Replace with your image path
barcode_data = scan_barcode_from_image(image_path)
if barcode_data:
    print(f"Decoded Barcode Data: {barcode_data}")
    # return barcode_data
else:
    print("No barcode data found.")
    # return None