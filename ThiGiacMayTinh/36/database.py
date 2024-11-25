import sqlite3
from datetime import datetime  # Sửa lỗi sai chính tả thư viện

class AttendanceDB:
    def __init__(self):  # Đúng tên hàm khởi tạo
        # Kết nối đến cơ sở dữ liệu SQLite
        self.conn = sqlite3.connect('my_database.db')
        self.create_tables()  # Gọi hàm tạo bảng

    def create_tables(self):
        cursor = self.conn.cursor()  # Tạo con trỏ để thực hiện lệnh SQL
        # Tạo bảng "students"
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT(50) PRIMARY KEY,
                name TEXT(250),
                class_id TEXT(25)
            )
            '''
        )
        # Tạo bảng "attendance"
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                class_id TEXT,
                date TEXT,
                time TEXT,
                confidence REAL,
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            )
            '''
        )
        self.conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu

    def mark_attendance(self, student_id, class_id, confidence):
        cursor = self.conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")  # Sửa lỗi `datatime` thành `datetime`

        # Kiểm tra nếu đã ghi nhận điểm danh hôm nay
        cursor.execute(
            '''
            SELECT COUNT(*) FROM attendance
            WHERE student_id = ? AND class_id = ? AND date = ?
            ''', (student_id, class_id, today)
        )
        if cursor.fetchone()[0] == 0:  # Nếu chưa ghi nhận
            now = datetime.now()
            cursor.execute(
                '''
                INSERT INTO attendance (student_id, class_id, date, time, confidence)
                VALUES (?, ?, ?, ?, ?)
                ''', (student_id, class_id, today, now.strftime("%H:%M:%S"), confidence)
            )
            self.conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
            return True
        return False  # Nếu đã ghi nhận thì trả về False

    def get_student_name(self, student_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT name FROM students WHERE student_id = ?', (student_id,))
        result = cursor.fetchone()
        return result[0] if result else "Unknown"

# Khởi tạo lớp
a = AttendanceDB()

# Kiểm tra điểm danh
print(a.mark_attendance("123456", "21DTH", 0.8))  # True nếu chưa điểm danh
print(a.mark_attendance("123456", "21DTH", 0.8))  # False nếu đã điểm danh

# Kiểm tra tên sinh viên
print(a.get_student_name("123456"))  # Trả về "Unknown" nếu sinh viên không tồn tại
