from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
import time
from HelperFunctions import calculate_age

class ClassifierModel:
    def __init__(self, algorithm, connector):
        self.connector = connector
        if algorithm == "logistic_regression":
            self.model = LogisticRegression()
        elif algorithm == "naive_bayes":
            self.model = GaussianNB()
        elif algorithm == "decision_tree":
            self.model = DecisionTreeClassifier()
        self.label_encoder = LabelEncoder()   


    
    def train(self, X_train, y_train, user_data):
            start_time = time.time()  # Bắt đầu đo thời gian huấn luyện
            X_train_encoded = self.encode_features(X_train)
            self.model.fit(X_train_encoded, y_train)
            end_time = time.time()  # Kết thúc đo thời gian huấn luyện
            self.training_time = end_time - start_time  # Tính thời gian huấn luyện
        

    def encode_features(self, X):
        label_encoders = {}
        X_encoded = []

        for row in X:
            encoded_row = []
            for i, value in enumerate(row):
                if isinstance(value, str):
                    if i not in label_encoders:
                        label_encoders[i] = LabelEncoder()
                        label_encoders[i].fit([value for row in X for value in [row[i]] if isinstance(value, str)])
                    encoded_row.append(label_encoders[i].transform([value])[0])
                else:
                    encoded_row.append(value)
            X_encoded.append(encoded_row)
        
        return X_encoded



    def predict(self, X_test, user_data):
        start_time = time.time()  # Bắt đầu đo thời gian dự đoán
        user_location_id = user_data.get("location_id")
        user_hometown_id = user_data.get("hometown_id")
        user_age = calculate_age(user_data.get("age"))  # Chuyển đổi ngày sinh thành tuổi
        user_gender = 1 if user_data.get("gender") == "MALE" else 0  # 0 cho FEMALE, 1 cho MALE
        recommendations = []
        distances = []
        X_test_encoded = self.encode_features(X_test)
        predictions = self.model.predict(X_test_encoded)
        for i, data_point in enumerate(X_test):
            if predictions[i] == 1:
                
                test_location_id = data_point[5]
                test_hometown_id = data_point[4]
                test_age = data_point[1]
                test_gender = data_point[2]
                #   
                user_vector = [user_hometown_id, user_location_id, user_age, user_gender]
                test_vector = [test_hometown_id, test_location_id, test_age, test_gender]
                
                # Tính khoảng cách Euclidean giữa hai vector
                distance = euclidean_distances([user_vector], [test_vector])[0][0]
                distances.append(distance)
            
                # Tính giá trị trung bình và độ lệch chuẩn của khoảng cách
                mean_distance = np.mean(distances)
                std_distance = np.std(distances)
                
                # Chọn ngưỡng liên kết là giá trị trung bình + độ lệch chuẩn = Trung bình cộng độ lệch chuẩn
                linking_threshold = mean_distance + std_distance
                if distance <= linking_threshold:   
                    if len(data_point) > 5 and data_point[4] == user_data["hometown_id"] and data_point[5] == user_data["location_id"]:
                        friend_id = data_point[0]  # Lấy friend's ID
                        friend_data = self.connector.get_user_data_by_id(friend_id)  # Lấy dữ liệu người dùng từ friend_id
                        if friend_data:  # CKiểm tra dữ liệu có tồn tại hay không
                            friend_data_dict = dict(friend_data)  # Chuyển bản ghi sang từ điển
                            friend_name = friend_data_dict.get("u.friend_name") 
                            friend_birthday = friend_data_dict.get("age")
                            friend_gender = friend_data_dict.get("gender")
                            hometown_name = friend_data_dict.get("u.hometown_name")
                            location_name = friend_data_dict.get("u.location_name")
                            if friend_name:
                                recommendations.append((friend_name, friend_birthday, friend_gender, hometown_name, location_name, "Cùng quê quán và nơi sinh sống", distance, "Gợi ý kết bạn"))
                            else:
                                print(f"Không tìm thấy người dùng có Id: {friend_id}")
                        else:
                            print(f"Không tìm thấy người dùng có Id: {friend_id}")
                    elif len(data_point) > 4 and data_point[4] == user_data["hometown_id"]:
                        friend_id = data_point[0]  
                        friend_data = self.connector.get_user_data_by_id(friend_id) 
                        if friend_data:  
                            friend_data_dict = dict(friend_data) 
                            friend_name = friend_data_dict.get("u.friend_name")  
                            friend_birthday = friend_data_dict.get("age")
                            friend_gender = friend_data_dict.get("gender")
                            hometown_name = friend_data_dict.get("u.hometown_name")
                            location_name = friend_data_dict.get("u.location_name")
                            if friend_name:
                                recommendations.append((friend_name, friend_birthday, friend_gender, hometown_name, location_name, "Cùng quê quán", distance, "Gợi ý kết bạn"))
                            else:
                                print(f"Không tìm thấy người dùng có Id: {friend_id}")
                        else:
                            print(f"Không tìm thấy người dùng có Id: {friend_id}")
                    elif len(data_point) > 5 and data_point[5] == user_data["location_id"]:
                        friend_id = data_point[0] 
                        friend_data = self.connector.get_user_data_by_id(friend_id) 
                        if friend_data:  
                            friend_data_dict = dict(friend_data) 
                            friend_name = friend_data_dict.get("u.friend_name") 
                            friend_birthday = friend_data_dict.get("age")
                            friend_gender = friend_data_dict.get("gender")
                            hometown_name = friend_data_dict.get("u.hometown_name")
                            location_name = friend_data_dict.get("u.location_name")
                            if friend_name:
                                recommendations.append((friend_name, friend_birthday, friend_gender, hometown_name, location_name, "Cùng nơi sinh sống", distance, "Gợi ý kết bạn"))
                            else:
                                print(f"Không tìm thấy người dùng có Id: {friend_id}")
                    else:
                        friend_id = data_point[0] 
                        friend_data = self.connector.get_user_data_by_id(friend_id)  
                        if friend_data:  
                            friend_data_dict = dict(friend_data)  
                            friend_name = friend_data_dict.get("u.friend_name")  
                            friend_birthday = friend_data_dict.get("age")
                            friend_gender = friend_data_dict.get("gender")
                            hometown_name = friend_data_dict.get("u.hometown_name")
                            location_name = friend_data_dict.get("u.location_name")
                            if friend_name:
                                recommendations.append((friend_name, friend_birthday, friend_gender, hometown_name, location_name, "Ngẫu nhiên", distance, "Gợi ý kết bạn"))
                            else:
                                print(f"Không tìm thấy người dùng có Id: {friend_id}")
                        else:
                            print(f"Không tìm thấy người dùng có Id: {friend_id}")
        
        end_time = time.time()  # Kết thúc đo thời gian dự đoán
        self.prediction_time = end_time - start_time  # Tính thời gian dự đoán
        return recommendations
        


    def evaluate(self, X_test, y_test):
        X_test_encoded = self.encode_features(X_test)
        predictions = self.model.predict(X_test_encoded)
        # Sử dụng confusion_matrix để tính các giá trị TP, TN, FP, FN
        confusion_mat = confusion_matrix(y_test, predictions, labels=[1, 2])

        # Tính lại các giá trị TP, TN, FP, FN theo vị trí đúng trong confusion matrix
        TP = confusion_mat[0, 0] 
        FN = confusion_mat[0, 1]
        FP = confusion_mat[1, 0]
        TN = confusion_mat[1, 1]
        # In ra các giá trị
        print("Matrix:", confusion_mat)
        print("True Positives (TP):", TP)
        print("True Negatives (TN):", TN)
        print("False Positives (FP):", FP)
        print("False Negatives (FN):", FN)
        precision = precision_score(y_test, predictions)
        recall = recall_score(y_test, predictions)
        f1 = f1_score(y_test, predictions)
        return precision, recall, f1