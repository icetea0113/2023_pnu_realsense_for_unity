import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

# 데이터를 불러옵니다.
data = pd.read_csv("skeleton_data.txt", header=None, names=["timestamp", "joint", "landmark_x", "landmark_y", "depth_data", "landmark_z"])

# depth data가 0이나 -1이 아닌 값들과 해당 시점의 landmark z 값을 저장합니다.
filtered_data = data[data['depth_data'] > 0]
X_train = filtered_data[['landmark_z']]
y_train = filtered_data['depth_data']

# KNN 모델을 학습시킵니다.
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train, y_train)

# depth data가 0이나 -1인 값을 찾아서 KNN 모델로 예측한 depth data로 업데이트합니다.
missing_depth_index = data[data['depth_data'] <= 0].index
X_test = data.loc[missing_depth_index, ['landmark_z']]
predicted_depth_data = knn.predict(X_test)
data.loc[missing_depth_index, 'depth_data'] = predicted_depth_data

# 업데이트된 데이터를 저장합니다.
data.to_csv("updated_skeleton_data.txt", header=False, index=False)
print("End Update by KNN")