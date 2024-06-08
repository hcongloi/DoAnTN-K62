from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QGridLayout, QMessageBox
from PyQt5.QtCore import pyqtSlot
from Neo4jConnector import Neo4jConnector
from ClassifierModel import ClassifierModel
import xlsxwriter
from sklearn.model_selection import train_test_split

class Starter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống khuyến nghị kết bạn")
        self.initUI()
        self.friends_found = False

    def initUI(self):
        self.setMinimumSize(1200, 800) 
        self.setMaximumSize(1200, 800)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Data
        data_layout = QVBoxLayout()
        data_group = QWidget()
        data_group.setLayout(data_layout)
        main_layout.addWidget(data_group)
        
        data_layout.addWidget(QLabel("Người dùng:"))
        self.cbUsers = QComboBox()  
        data_layout.addWidget(self.cbUsers)
        
        self.btnPrintResults = QPushButton("In kết quả vào Excel")
        self.btnPrintResults.clicked.connect(self.print_results_to_excel)
        data_layout.addWidget(self.btnPrintResults)
        

        self.cbAl = QComboBox()
        self.cbAl.addItems(["Logistic Regression", "Naive Bayes", "Decision Tree"])
        data_layout.addWidget(QLabel("Mô hình phân lớp:"))
        data_layout.addWidget(self.cbAl)

        self.btnConfirm = QPushButton("TÌM BẠN")
        self.btnConfirm.clicked.connect(self.find_friends)
        data_layout.addWidget(self.btnConfirm)
        
        self.tblUserInfo = QTableWidget()  
        data_layout.addWidget(QLabel("Thông tin người dùng:"))
        self.tblUserInfo.setColumnCount(7)
        self.tblUserInfo.setRowCount(2)  
        header = self.tblUserInfo.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tblUserInfo.setHorizontalHeaderLabels(["Mã người dùng", "Tên người dùng", "Ngày sinh", "Giới tính", "Quê quán", "Nơi sinh sống hiện tại", "Tình trạng mối quan hệ"])
        self.tblUserInfo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tblUserInfo.setFixedHeight(2 * self.tblUserInfo.rowHeight(0)) 
        data_layout.addWidget(self.tblUserInfo)
        
        self.tbl = QTableWidget()
        data_layout.addWidget(QLabel("Kết quả:"))
        self.tbl.setColumnCount(8)
        header = self.tbl.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tbl.setHorizontalHeaderLabels(["Người dùng","Ngày sinh","Giới tính","Quê quán", "Nơi sinh sống hiện tại", "Mối quan hệ", "Khoảng cách phù hợp", "Khuyến nghị kết bạn"])
        self.tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        data_layout.addWidget(self.tbl)

        # Additional labels with scroll area
        self.panel2_scroll = QScrollArea()
        self.panel2 = QWidget()  
        self.panel2_layout = QGridLayout()  
        data_layout.addWidget(QLabel("Mô tả:"))
        self.panel2.setLayout(self.panel2_layout)
        self.panel2_scroll.setWidgetResizable(True)
        self.panel2_scroll.setFixedHeight(4 * 30)
        self.panel2_scroll.setWidget(self.panel2)
        main_layout.addWidget(self.panel2_scroll)

        labels = [
            "Tổng số lượng", "Số người dự đoán phù hợp", "Số người dự đoán không phù hợp",
            "Độ chính xác (Precision)","Độ bao phủ (Recall)", "Hệ số F1 (F1-score)", "Thời gian huấn luyện (s)", "Thời gian dự đoán (s)"
        ]


        col_count = 2  
        for index, label_text in enumerate(labels):
            row = index // col_count  
            col = index % col_count   
            label = QLabel(label_text)
            self.panel2_layout.addWidget(label, row, col)

        # Kết nối với cơ sở dữ liệu Neo4J
        self.connector = Neo4jConnector("bolt://localhost:7687", "neo4j", "Congloi2002")
        users = self.connector.get_users()
        self.cbUsers.addItems(users)
        

    @pyqtSlot()
    def find_friends(self):
        

        selected_user = self.cbUsers.currentText()
        algorithm = self.cbAl.currentText()
        
        if not selected_user:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một người dùng.")
            return
        
        
        # Lấy dữ liệu từ Neo4J
        user_data = self.connector.get_user_data(selected_user)
        
        # Kiểm tra xem user_data có tồn tại không
        if user_data:
            # Hiển thị thông tin người dùng
            self.display_user_info(user_data)

            # Tiếp tục với các bước khác (train, predict, display_results, display_comparison)
            X, y = self.connector.get_features_labels(selected_user)  

            if not X:  # Handle the case where X is empty
                QMessageBox.warning(self, "Cảnh báo", "Không có dữ liệu hợp lệ cho người dùng được chọn.")
                return

            # Chia tập dữ liệu thành tập huấn luyện và tập kiểm tra
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            # Huấn luyện mô hình
            model = ClassifierModel(algorithm.lower().replace(" ", "_"), self.connector)
            model.train(X_train, y_train, user_data)
            # Dự đoán liên kết
            predictions = model.predict(X_test, user_data)
            precision, recall, f1 = model.evaluate(X_test, y_test)
            # Hiển thị kết quả
            training_time = model.training_time
            prediction_time = model.prediction_time
            self.display_results(predictions)
            self.display_comparison(len(X_test), len(predictions), len(y_test) - len(predictions), precision, recall, f1, training_time, prediction_time)
            self.friends_found = True
            QMessageBox.information(self, "Thông báo", f"Đã tìm thấy {len(predictions)} người dùng phù hợp để kết bạn.")
        else:
            QMessageBox.warning(self, "Cảnh báo", f"Không tìm thấy thông tin cho người dùng {selected_user}.")

    def display_user_info(self, user_data):
        # Xóa nội dung hiện tại của bảng thông tin người dùng
        self.tblUserInfo.clearContents()
        self.tblUserInfo.setRowCount(1)  # Chỉ cần 1 hàng để hiển thị thông tin của người dùng

        # Điền thông tin người dùng vào bảng
        
        self.tblUserInfo.setItem(0, 0, QTableWidgetItem(user_data.get("u.friend_id")))
        self.tblUserInfo.setItem(0, 1, QTableWidgetItem(user_data.get("u.friend_name")))
        self.tblUserInfo.setItem(0, 2, QTableWidgetItem(user_data.get("age")))
        self.tblUserInfo.setItem(0, 3, QTableWidgetItem(user_data.get("gender")))
        self.tblUserInfo.setItem(0, 4, QTableWidgetItem(user_data.get("u.hometown_name")))
        self.tblUserInfo.setItem(0, 5, QTableWidgetItem(user_data.get("u.location_name")))
        self.tblUserInfo.setItem(0, 6, QTableWidgetItem(user_data.get("relationship_status")))


    def display_results(self, predictions):
        predictions_sorted = sorted(predictions, key=lambda x: x[6])
        
        self.tbl.clearContents()
        self.tbl.setRowCount(len(predictions_sorted))
        
        for row, (user, birthday, gender, hometown, location, relation, confidence, recommendations) in enumerate(predictions_sorted):
            self.tbl.setItem(row, 0, QTableWidgetItem(user))
            self.tbl.setItem(row, 1, QTableWidgetItem(birthday))
            self.tbl.setItem(row, 2, QTableWidgetItem(gender))
            self.tbl.setItem(row, 3, QTableWidgetItem(hometown))
            self.tbl.setItem(row, 4, QTableWidgetItem(location))
            self.tbl.setItem(row, 5, QTableWidgetItem(relation))
            self.tbl.setItem(row, 6, QTableWidgetItem(str("{:.2f}".format(confidence))))
            self.tbl.setItem(row, 7, QTableWidgetItem(recommendations))

    def display_comparison(self, total_users, correct_predictions, incorrect_predictions, precision, recall, f1, training_time, prediction_time):
        for i in reversed(range(self.panel2_layout.count())):
            self.panel2_layout.itemAt(i).widget().deleteLater()

        labels = [
            ("Tổng số lượng", total_users),
            ("Số người dự đoán phù hợp", correct_predictions),
            ("Số người dự đoán không phù hợp", incorrect_predictions),
            ("Độ chính xác (Precision)", f"{precision:.4f}"),
            ("Độ bao phủ (Recall)", f"{recall:.4f}"),
            ("Hệ số F1 F1-score)", f"{f1:.4f}"),
            ("Thời gian huấn luyện (s)", f"{training_time:.4f}"),
            ("Thời gian dự đoán (s)", f"{prediction_time:.4f}")
        ]
        for index, (label_text, value) in enumerate(labels):
            row = index // 2  
            col = index % 2   
            label = QLabel(f"{label_text}: {value}")
            self.panel2_layout.addWidget(label, row, col)
            
    def print_results_to_excel(self):
        
        if not self.friends_found:
            # Nếu người dùng chưa nhấn nút tìm bạn bè, thông báo vui lòng tìm bạn bè phù hợp
            QMessageBox.warning(self, "Cảnh báo", f"Vui lòng tìm bạn bè phù hợp trước khi in kết quả ra Excel.")
            return
        # Lấy tên người dùng và mô hình phân lớp được chọn
        selected_user = self.cbUsers.currentText()
        algorithm = self.cbAl.currentText()
        
        # Tạo tên tệp tin dựa trên tên người dùng
        file_name = f'ket_qua_du_doan_cua_{selected_user}_{algorithm}.xlsx'
        
        # Lấy dữ liệu bảng thông tin người dùng
        user_info = []
        for row in range(self.tblUserInfo.rowCount()):
            for col in range(self.tblUserInfo.columnCount()):
                item = self.tblUserInfo.item(row, col)
                if item:
                    user_info.append(item.text())

        # Lấy kết quả danh sách dự đoán
        predictions = []
        for row in range(self.tbl.rowCount()):
            prediction_row = []
            for col in range(self.tbl.columnCount()):
                item = self.tbl.item(row, col)
                if item:
                    prediction_row.append(item.text())
            predictions.append(prediction_row)
        
        # Lấy kết quả hiệu suất của mô hình
        comparison_data = []
        for i in range(self.panel2_layout.count()):
            widget = self.panel2_layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                comparison_data.append(widget.text())

        # Tạo file Excel
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()
        
        # Dòng minh họa cho thông tin người dùng
        worksheet.write_row(0, 0, ["Thông tin người dùng:"])

        # Ghi các nhãn thông tin người dùng và dữ liệu người dùng
        user_info_labels = ["Mã người dùng", "Tên người dùng", "Ngày sinh", "Giới tính", "Quê quán", "Nơi sinh sống hiện tại", "Tình trạng mối quan hệ"]
        for i, label in enumerate(user_info_labels):
            worksheet.write(1, i, label)
        for i, value in enumerate(user_info):
            worksheet.write(2, i, value)

        # Dòng minh họa cho dự đoán
        worksheet.write_row(3, 0, ["Dự đoán:"])

        # Ghi các nhãn dự đoán và dữ liệu dự đoán
        prediction_labels = ["Người dùng", "Ngày sinh", "Giới tính", "Quê quán", "Nơi sinh sống hiện tại", "Mối quan hệ", "Khoảng cách phù hợp", "Khuyến nghị kết bạn"]
        for j, label in enumerate(prediction_labels):
            worksheet.write(4, j, label)
        for row, prediction in enumerate(predictions):
            for col, value in enumerate(prediction):
                worksheet.write(row + 5, col, value)

        # Dòng minh họa cho dữ liệu so sánh
        worksheet.write_row(5 + len(predictions), 0, ["So sánh:"])

        # Ghi các nhãn so sánh và dữ liệu so sánh
        for l, value in enumerate(comparison_data):
            worksheet.write(6 + len(predictions), l, value)

        workbook.close()
        QMessageBox.information(self, "Thông báo", "Đã in kết quả thành công vào tệp Excel.")