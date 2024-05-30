from neo4j import GraphDatabase
from HelperFunctions import calculate_age

class Neo4jConnector:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def get_users(self):
        with self._driver.session() as session:
            result = session.run("MATCH (u:Person) RETURN u.friend_name AS name")
            return [record["name"] for record in result]

    def get_user_data(self, selected_user):
        with self._driver.session() as session:
            result = session.run("MATCH (u:Person {friend_name: $name}) RETURN u.friend_id, u.friend_name, u.friend_birthday AS age, u.friend_gender AS gender, u.relationship_status AS relationship_status, u.hometown_id AS hometown_id, u.location_id AS location_id, u.hometown_name, u.location_name", name=selected_user)
            user_data = result.single()
            return user_data
    
    def get_features_labels(self, selected_user):
        with self._driver.session() as session:
            # Truy vấn để lấy danh sách các friend_id của các người dùng không phải là bạn bè của người dùng được chọn
            query = """
            MATCH (kei:Person {friend_name: $name})
            WITH kei
            MATCH (potentialFriend:Person)
            WHERE NOT (kei)-[:FRIEND]->(potentialFriend) AND kei <> potentialFriend
            WITH kei, potentialFriend
            OPTIONAL MATCH (kei)-[:FRIEND]->(commonFriend)-[:FRIEND]->(potentialFriend)
            WHERE kei <> commonFriend AND kei <> potentialFriend
            WITH kei, potentialFriend, COUNT(DISTINCT commonFriend) AS common_friends_count
            RETURN potentialFriend.friend_id AS friend_id, 
                potentialFriend.friend_name AS friend_name,
                potentialFriend.friend_birthday AS age, 
                potentialFriend.friend_gender AS gender, 
                CASE WHEN common_friends_count > 0 THEN 1 ELSE 2 END AS friend, 
                potentialFriend.relationship_status AS relationship_status, 
                potentialFriend.hometown_id AS hometown_id, 
                potentialFriend.location_id AS location_id

            """
            non_friends_result = session.run(query, name=selected_user)
            data = [record for record in non_friends_result]
            
            if data:
                # Trích xuất friend_id và thông tin khác từ kết quả
                non_friend_ids = [record["friend_id"] for record in data]
                selector_user = self.get_user_data(selected_user)
                selector_user_hometown_id = selector_user["hometown_id"]
                selector_user_location_id = selector_user["location_id"]
                # Xử lý trường hợp có người dùng không phải là bạn bè
                X = []
                y = []
                for record in data:
                    if all([record["friend_id"], record["age"], record["gender"], record["friend"], record["relationship_status"], record["hometown_id"], record["location_id"]]):  # Kiểm tra liệu tất cả trường thông tin có không
                        age = calculate_age(record["age"])  # Chuyển đổi ngày sinh thành tuổi
                        # Chuyển đổi relationship_status thành số
                        if record["relationship_status"] == "Độc thân":
                            relationship_status = 1
                        elif record["relationship_status"] == "Đang hẹn hò":
                            relationship_status = 2
                        elif record["relationship_status"] == "Đã kết hôn":
                            relationship_status = 3
                        else:
                            relationship_status = 0  # Giá trị mặc định nếu không phù hợp
                        # Chuyển đổi friend_gender thành số
                        gender = 1 if record["gender"] == "MALE" else 0  # 0 cho FEMALE, 1 cho MALE
                        # Kiểm tra hometown và location của người dùng so với selector_user
                        if ((record["hometown_id"] == selector_user_hometown_id or record["location_id"] == selector_user_location_id) and record["friend"] == 0):
                            record["friend"] = 1
                        X.append((record["friend_id"], age, gender, relationship_status, record["hometown_id"], record["location_id"]))
                        y.append(record["friend"])  
                return X, y
            else:
                return [], []
            
    def get_user_data_by_id(self, friend_id):
        with self._driver.session() as session:
            result = session.run("MATCH (u:Person {friend_id: $id}) RETURN u.friend_name, u.friend_birthday AS age, u.friend_gender AS gender, u.relationship_status AS relationship_status, u.hometown_id AS hometown_id, u.location_id AS location_id, u.hometown_name, u.location_name", id=friend_id)
            user_data_id = result.single()
            return user_data_id