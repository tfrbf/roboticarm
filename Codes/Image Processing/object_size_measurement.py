from scipy.spatial.distance import euclidean
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2

# Function to show array of images (intermediate results)
def show_images(images):
    for i, img in enumerate(images):
        cv2.imshow("image_" + str(i), img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Initialize camera
cap = cv2.VideoCapture(1)  # Ensure this is the correct ID for your LG G3 Beat camera
cap.set(3, 3264)  # Width
cap.set(4, 2448)  # Height
cap.set(10, 160)  # Brightness

# Reference object dimensions (known dimensions in cm)
ref_object_width = 2
ref_object_height = 2

# Define minimum and maximum contour area to filter objects
min_contour_area = 200
max_contour_area = 10000

while True:
    # Read frame from camera
    success, image = cap.read()
    if not success:
        break

    # Preprocess the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)

    # Use adaptive thresholding instead of fixed thresholds
    edged = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) == 0:
        cv2.imshow("Measurement", image)
        # Check for key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # Sort contours from left to right as leftmost contour is reference object
    (cnts, _) = contours.sort_contours(cnts)

    # Filter contours by area
    cnts = [x for x in cnts if min_contour_area < cv2.contourArea(x) < max_contour_area]

    if len(cnts) == 0:
        cv2.imshow("Measurement", image)
        # Check for key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # Reference object dimensions
    ref_object = cnts[0]
    box = cv2.minAreaRect(ref_object)
    box = cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    (tl, tr, br, bl) = box
    dist_in_pixel = euclidean(tl, tr)
    pixel_per_cm = dist_in_pixel / ref_object_width

    # Draw remaining contours and calculate dimensions
    for cnt in cnts:
        box = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        (tl, tr, br, bl) = box
        cv2.drawContours(image, [box.astype("int")], -1, (0, 0, 255), 2)
        mid_pt_horizontal = (tl[0] + int(abs(tr[0] - tl[0]) / 2), tl[1] + int(abs(tr[1] - tl[1]) / 2))
        mid_pt_vertical = (tr[0] + int(abs(tr[0] - br[0]) / 2), tr[1] + int(abs(tr[1] - br[1]) / 2))
        width = euclidean(tl, tr) / pixel_per_cm
        height = euclidean(tr, br) / pixel_per_cm
        cv2.putText(image, "{:.1f}cm".format(width), (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        cv2.putText(image, "{:.1f}cm".format(height), (int(mid_pt_vertical[0] + 10), int(mid_pt_vertical[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    # Display the processed frame
    cv2.imshow("Measurement", image)

    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
