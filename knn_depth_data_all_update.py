import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

# Load the data from the text file
data = pd.read_csv("skeleton_data.txt", delimiter=',', header=None)
data.columns = ['timestamp', 'joint', 'landmark_x', 'landmark_y', 'depth', 'landmark_z']

# Select only valid depth data (depth != 0 and depth != -1)
valid_data = data[(data['depth'] != 0) & (data['depth'] != -1)]

# Train the KNN model using valid depth data and landmark.z
k = 7 # Change this value to set the number of neighbors
knn = KNeighborsRegressor(n_neighbors=k)
knn.fit(valid_data[['landmark_z']], valid_data['depth'])

# Predict the depth data for all landmarks using the trained KNN model
data['predicted_depth'] = knn.predict(data[['landmark_z']])

# Calculate the correction factor for each depth data
correction_factor = 1.0 # Change this value to adjust the correction degree (0 <= correction_factor <= 1)
data['corrected_depth'] = data['depth'] * (1 - correction_factor) + data['predicted_depth'] * correction_factor

# Save the corrected data to a new text file
data[['timestamp', 'joint', 'landmark_x', 'landmark_y', 'corrected_depth', 'landmark_z']].to_csv("updated_skeleton_data.txt", index=False, header=False)

print("End update KNN !!")