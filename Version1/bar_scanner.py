import cv2
from pyzbar.pyzbar import decode

class BarcodeScanner:
    def __init__(self):
        # Initialize webcam capture
        self.cap = cv2.VideoCapture(0)
    
    def scan_barcode(self):
        while True:
            # Capture frame-by-frame from webcam
            ret, frame = self.cap.read()
            
            if not ret:
                print("Failed to grab frame")
                break
            
            # Decode the barcodes in the frame
            barcodes = decode(frame)
            
            for barcode in barcodes:
                # Get the barcode data
                barcode_data = barcode.data.decode('utf-8')
                barcode_type = barcode.type
                
                # Draw a rectangle around the barcode
                rect_points = barcode.polygon
                if len(rect_points) == 4:
                    pts = [tuple(point) for point in rect_points]
                    pts = cv2.polylines(frame, [np.array(pts, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=3)
                
                # Display the barcode data on the image
                x, y, w, h = barcode.rect
                cv2.putText(frame, f'{barcode_data} ({barcode_type})', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                # Stop the webcam if a barcode is found
                print(f"Barcode found: {barcode_data}")
                self.cap.release()  # Stop webcam
                cv2.destroyAllWindows()  # Close any open OpenCV windows
                return barcode_data
            
            # Display the resulting frame with the barcode highlighted
            cv2.imshow("Barcode Scanner", frame)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release the webcam and close any OpenCV windows
        self.cap.release()
        cv2.destroyAllWindows()
    
    def stop_scanner(self):
        """Method to stop the webcam feed manually if needed"""
        self.cap.release()
        cv2.destroyAllWindows()


# Create an instance of the BarcodeScanner class
scanner = BarcodeScanner()

# Call the scan_barcode method to start scanning
barcode = scanner.scan_barcode()

# Print the scanned barcode data
print(f"Scanned Barcode Data: {barcode}")
