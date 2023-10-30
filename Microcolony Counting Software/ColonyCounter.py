#Code adapted from: http://www.sixthresearcher.com/counting-blue-and-white-bacteria-colonies-with-python-and-opencv/
#Author: Alvaro Sebastian
#Code also adapted from: https://github.com/Cameron-Ray/lensless-microscopy/tree/main
#Author: Cameron Ray - University of Cape Town

#Adapted by: Lila Heath

import cv2
import numpy as np

# Load the bacterial colony image 
image_orig = cv2.imread(r"C:\Users\Lila Heath\OneDrive\Desktop\THESIS\lensless-microscopy-main\colony-counting\colony_count_test_2.jpg")
height_orig, width_orig = image_orig.shape[:2]

# Create a mask highlighting the bacteria
lower = np.array([0,0,0])
upper = np.array([180,180,180])
image_mask = cv2.inRange(image_orig, lower, upper)

# Use the mask to make colonies more pronounced
image_res = cv2.bitwise_and(image_orig, image_orig, mask = image_mask)

# load the image, convert it to grayscale, and blur it slightly
image_gray = cv2.cvtColor(image_res, cv2.COLOR_BGR2GRAY)
image_gray = cv2.GaussianBlur(image_gray, (5, 5), 0)

# perform edge detection, then perform a dilation + erosion to close gaps in between object edges
image_edged = cv2.Canny(image_gray, 95, 100)
image_edged = cv2.dilate(image_edged, None, iterations=4)
image_edged = cv2.erode(image_edged, None, iterations=4)

# find contours in the edge map
contours = cv2.findContours(image_edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0]

# Filter out small contours
contours = [contour for contour in contours if cv2.contourArea(contour) > 1]

# Measure distance between contour centroids
centroids = []
for contour in contours:
    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    centroids.append((cX, cY))

# Define a distance threshold to group nearby contours
min_distance = 50

# Cluster contours based on distance
clusters = []
for i, (x, y) in enumerate(centroids):
    cluster = [i]
    for j, (x2, y2) in enumerate(centroids):
        if i != j and np.sqrt((x - x2) ** 2 + (y - y2) ** 2) < min_distance:
            cluster.append(j)
    if cluster not in clusters:
        clusters.append(cluster)
count = len(clusters)

# Process each cluster as a single colony
for cluster in clusters:
    # Find the convex hull of the combined contours in the cluster
    combined_contours = [contours[i] for i in cluster]
    combined_hull = cv2.convexHull(np.vstack(combined_contours))

    # Draw the colony
    cv2.drawContours(image_res, [combined_hull], 0, (0, 255, 0), 3)

#Write the number of colonies counted on the image
cv2.putText(image_res, str(count), (10, height_orig - 50), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10)   
    

# Display and save the result
cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Result', width_orig, height_orig)
cv2.imshow("Result", image_res)
cv2.imwrite("output.jpg", image_res)
cv2.waitKey(0)
cv2.destroyAllWindows()

