# DoAnTN-K62

⚠️ Yêu cầu trước.
Cài đặt Python 3.8
Cài đặt Neo4j Desktop
Kiến thức cơ bản về Python và Neo4j.
🛠 Phát triển
Đầu tiên, tạo một môi trường ảo và kích hoạt nó:

bash
Sao chép mã
python -m venv venv
source venv/bin/activate   # Trên Windows sử dụng `venv\Scripts\activate`
Thứ hai, cài đặt các gói Python cần thiết:

bash
Sao chép mã
pip install numpy pandas scikit-learn networkx matplotlib seaborn tensorflow neo4j pyqt5 xlsxwriter
Thứ ba, chạy script Python của bạn:

bash
Sao chép mã
python main.py
Đảm bảo Neo4j Desktop đang chạy và cơ sở dữ liệu Neo4j của bạn có thể truy cập được.

Cấu trúc thư mục
shell
Sao chép mã
.
├── README.md                       # Tệp README
├── .vscode                         # Cấu hình VSCode
├── data                            # Thư mục chứa dữ liệu
├── notebooks                       # Jupyter notebooks cho việc khám phá dữ liệu
├── scripts                         # Các script Python
├── src
│   ├── __init__.py                 # Khởi tạo module src
│   ├── data                        # Các hàm xử lý dữ liệu
│   │   └── load_data.py            # Script để tải dữ liệu
│   ├── models                      # Các mô hình học máy
│   │   ├── train.py                # Script để huấn luyện mô hình
│   │   ├── evaluate.py             # Script để đánh giá mô hình
│   │   └── predict.py              # Script để dự đoán
│   ├── visualization               # Các hàm vẽ đồ thị
│   │   ├── plot_data.py            # Script để vẽ đồ thị dữ liệu
│   ├── database                    # Tương tác với cơ sở dữ liệu
│   │   └── neo4j_handler.py        # Script để xử lý tương tác với Neo4j
│   ├── gui                         # Các thành phần giao diện đồ họa
│   │   └── main_window.py          # Cửa sổ GUI chính sử dụng PyQt5
│   └── utils                       # Các hàm tiện ích
│       └── helpers.py              # Các hàm trợ giúp
├── tests                           # Các bài kiểm tra đơn vị
│   └── test_models.py              # Các kiểm tra cho mô hình
├── Dockerfile                      # Dockerfile để đóng gói
└── docker-compose.yml              # Cấu hình Docker Compose
Tính năng mới
Nếu cần phát triển một tính năng mới, chúng ta sẽ tạo nhánh từ main. Khi tính năng hoàn thành, chúng ta sẽ rebase main trước khi tạo PR chống lại main.

Các bước làm việc với git:

Tạo một nhánh mới từ main
bash
Sao chép mã
git checkout -b feature/XYZ-123-mo-ta
Thực hiện nhiệm vụ của bạn và commit với
bash
Sao chép mã
git add -A && git commit -m "Thêm tính năng XYZ-123-mo-ta"
Pull phiên bản mới nhất của main và rebase
bash
Sao chép mã
git checkout main && git pull && git checkout - && git rebase main
Giải quyết xung đột nếu cần và đẩy mã lên origin
bash
Sao chép mã
git push origin feature/XYZ-123-mo-ta
Các Thư Viện và Công Cụ Cần Thiết
Thư Viện Python
NumPy: Thư viện hỗ trợ tính toán số học và xử lý mảng.
Pandas: Thư viện cung cấp các cấu trúc dữ liệu và công cụ phân tích dữ liệu.
Scikit-learn: Thư viện cung cấp các công cụ học máy đơn giản và hiệu quả.
NetworkX: Thư viện để tạo, thao tác và nghiên cứu cấu trúc, động lực và chức năng của các mạng phức tạp.
Matplotlib: Thư viện vẽ đồ thị 2D.
Seaborn: Thư viện vẽ biểu đồ thống kê, xây dựng trên Matplotlib.
TensorFlow hoặc PyTorch: Một trong hai thư viện này sẽ được sử dụng để xây dựng và huấn luyện mô hình học sâu.
Neo4j: Thư viện giao tiếp với cơ sở dữ liệu đồ thị Neo4j.
PyQt5: Thư viện để phát triển giao diện người dùng đồ họa (GUI).
XlsxWriter: Thư viện để tạo và chỉnh sửa các tệp Excel.
datetime: Thư viện cung cấp các lớp để xử lý ngày và thời gian.
time: Thư viện hỗ trợ đo thời gian thực thi và các chức năng liên quan đến thời gian.
Các Module Cụ Thể từ Scikit-learn
train_test_split: Chức năng chia dữ liệu thành tập huấn luyện và tập kiểm tra.
GaussianNB: Thuật toán Naive Bayes phân phối chuẩn.
LogisticRegression: Thuật toán hồi quy logistic.
DecisionTreeClassifier: Thuật toán cây quyết định.
precision_score, recall_score, f1_score, confusion_matrix: Các công cụ đánh giá hiệu suất của mô hình.
LabelEncoder: Công cụ mã hóa nhãn dữ liệu.
euclidean_distances: Chức năng tính toán khoảng cách Euclidean giữa các điểm.
Cơ Sở Dữ Liệu
Neo4j: Một hệ quản trị cơ sở dữ liệu đồ thị, phù hợp với việc lưu trữ và xử lý dữ liệu mạng xã hội.
Công Cụ Phát Triển
VS Code: Một trình soạn thảo mã nguồn mở, mạnh mẽ và dễ sử dụng, hỗ trợ nhiều ngôn ngữ lập trình và tích hợp nhiều công cụ.
Đảm bảo rằng bạn đã cài đặt tất cả các yêu cầu cần thiết và tuân theo cấu trúc thư mục để duy trì một dự án sạch sẽ và tổ chức. Chúc bạn mã hóa vui vẻ!

```bash
git push origin feature/AONJ-73-xxx
```

##.END.
