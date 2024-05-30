from datetime import datetime

def calculate_age(birthdate_str):
        birthdate = datetime.strptime(birthdate_str, "%d/%m/%Y")  # Chuyển đổi chuỗi thành datetime
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age