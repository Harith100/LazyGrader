import cv2
from pyzbar.pyzbar import decode

class BarcodeScanner:
    def __init__(self):
        # Initialize the webcam (0 is the default webcam, change if needed)
        self.cap = cv2.VideoCapture(0)

    def scan_barcode(self):
        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            if not ret:
                break

            # Decode the barcodes in the frame
            barcodes = decode(frame)

            for barcode in barcodes:
                # Extract the barcode data
                barcode_data = barcode.data.decode('utf-8')
                barcode_type = barcode.type

                # Print the barcode data and type
                print(f"Barcode detected: {barcode_data} (Type: {barcode_type})")

                # Draw a rectangle around the barcode
                rect_points = barcode.polygon
                if len(rect_points) == 4:
                    pts = [tuple(point) for point in rect_points]
                    cv2.polylines(frame, [np.array(pts, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=3)

                # Display the barcode data on the screen
                cv2.putText(frame, f"Data: {barcode_data}", (barcode.rect.left, barcode.rect.top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                # Stop the camera after detecting the barcode
                self.cap.release()
                cv2.destroyAllWindows()
                return barcode_data  # Return the barcode data and exit the method

            # Display the resulting frame
            cv2.imshow("Barcode Scanner", frame)

            # Optionally, you can stop the program by pressing the 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the webcam and close all OpenCV windows if no barcode is found
        self.cap.release()
        cv2.destroyAllWindows()

# Example usage
scanner = BarcodeScanner()
barcode_code = scanner.scan_barcode()
print(f"Scanned Barcode Code: {barcode_code}")