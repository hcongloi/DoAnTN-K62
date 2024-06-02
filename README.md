# Đồ án tốt nghiệp - CNTT - K62 - Huỳnh Công Lợi

## ⚠️ Yêu cầu.

1. Cài đặt Neo4J Desktop
2. Cài đặt VSCode

## Cấu trúc thư mục

```shell
.
├── README.md                                                     # File hướng dẫn cài đặt README 
├── BAO-CAO-DATN-HUYNHCONGLOI-62133105-FINAL                      # File Word báo cáo đồ án tốt nghiệp
├── BÁO CÁO ĐỒ ÁN TỐT NGHIỆP                     		  # File Power Point báo cáo đồ án tốt nghiệp
├── fb_friends_data                                               # File dữ liệu người dùng của mạng xã hội Facebook
├── Kết quả của các mô hình phân lớp                              # File Excel kết quả của các mô hình phân 
└── main 
   ├── __pycache__                  
   │   │── ClassifierModel.cpython-312		
   │   │── HelperFunctions.cpython-312                 	 
   │   │── Neo4jConnector.cpython-312                  		
   │   └── Starter.cpython-312               		
   ├── ClassifierModel						  # Mô hình phân lớp
   ├── HelperFunctions						  # Các hàm hỗ trợ
   ├── main							  # Hàm chính
   ├── Neo4jConnector						  # Kết nối tới Neo4j 
   └── Starter                      				  # Giao diện hiển thị của chương trình

```

## 🛠 Phát triển.

Đầu tiên, khởi động Neo4J Desktop 
- Tạo mới Project, chọn New -> Creat project  
- Tạo mới cơ sở dữ liệu đồ thị, chọn Add -> Local DBMS 
- Điền thông tin của cơ sở dữ liệu, Name(Tên của cơ sở dữ liệu) và Password(Mật khẩu để kết nối với cơ sở dữ liệu)
- Tìm thư mục của cơ sở dữ liệu đồ thị vừa tạo để đưa file dữ liệu vào, tới tên đường dẫn: Neo4j Desktop\relate-data\dbmss\cơ sở dữ liệu vừa tạo\import
- Sao chép file dữ liệu "fb_friends_data.csv" vào thư mục trên.
- Vào trong Neo4J và nhấn nút "Start" để khởi chạy cơ sở dữ liệu đồ thị
- Sau khi khởi chạy thành công nhấn nút "Open" để mở cửa sổ truy vấn "neo4j@bolt://localhost:7687/neo4j - Neo4j Browser"
> Tiến hành nạp dữ liệu vào trong cơ sở dữ liệu đồ thị Neo4j
```bash
  LOAD CSV WITH HEADERS FROM "file:///fb_friends_data.csv" AS nodes

  CREATE (p:Person {friend_id: nodes.friend_id,friend_name: nodes.friend_name, friend_gender:nodes.friend_gender,url:nodes.url,friend_birthday:nodes.friend_birthday,relationship_status:nodes.relationship_status,location_id:nodes.location_id, location_name:nodes.location_name,hometown_id:nodes.hometown_id, hometown_name:nodes.hometown_name})
```
- Sau đó nhấn nút "Run" hoặc tổ hợp phím "Ctrl + Enter" để chạy chương trình
- Tiếp đến tạo các mối quan hệ cho dữ liệu vừa được thêm trên
> Mối quan hệ bạn bè
```bash
  MATCH (p1:Person), (p2:Person)
	WHERE p1.friend_id < p2.friend_id AND rand() > 0.95
	WITH p1, p2
	LIMIT 3500
	MERGE (p1)-[:FRIEND]->(p2)
	MERGE (p2)-[:FRIEND]->(p1)
```
> Mối quan hệ cùng quê quán 
```bash
  LOAD CSV WITH HEADERS FROM "file:///fb_friends_data.csv" AS nodes
  WITH nodes 
  merge (a:Person{friend_id: nodes.friend_id,friend_name: nodes.friend_name}) 
  merge (h:Hometown {hometown_id:nodes.hometown_id, hometown_name:nodes.hometown_name})
  merge (a)-[:from]->(h)
  return a, h
```
> Mối quan hệ cùng nơi thường trú
```bash
	LOAD CSV WITH HEADERS FROM "file:///fb_friends_data.csv" AS nodes
	WITH nodes 
	merge (a:Person{friend_id: nodes.friend_id,friend_name: nodes.friend_name}) 
	merge(l:Location{location_id:nodes.location_id,location_name:nodes.location_name})
	merge (a)-[:LIVE]->(l)
	return a, l
```
> Mối quan hệ cùng độ tuổi
```bash
  LOAD CSV WITH HEADERS FROM "file:///fb_friends_data.csv" AS nodes
	WITH nodes, toInteger(split(nodes.friend_birthday, '/')[0]) AS birth_year
	MERGE (age:Age {birth_year: birth_year})
	ON CREATE SET age.age_range = toString(birth_year) + "-" + toString(birth_year + 10)
	merge (a:Person{friend_id: nodes.friend_id,friend_name: nodes.friend_name}) 
	MERGE (a)-[:FROM_AGE]->(age)
	RETURN a, age
```

Sau khi đã triển khai dữ liệu cho cơ sở dữ liệu đồ thị mạng xã hội Facebook thì tiếp đến ta sẽ tiến hành chạy chương trình "Hệ thống khuyến nghị kết bạn" trên VSCode
- Mở Terminal và tải các thư viện cần thiết cho chương trình
```bash
pip install numpy pandas scikit-learn networkx matplotlib seaborn tensorflow neo4j pyqt5 xlsxwriter
```
- Thay đổi mật khẩu trong file Starter dòng 95 thành mật khẩu của cơ sở dữ liệu đồ thị mà bạn đang chạy
```bash
self.connector = Neo4jConnector("bolt://localhost:7687", "neo4j", "Mật khẩu")
```
- Chạy chương trình "Run Python File" của VSCode 

##.Kết thúc.
