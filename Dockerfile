# Sử dụng Python rút gọn để build cho nhẹ
FROM python:3.10-slim

WORKDIR /app

# Sao chép và cài đặt thư viện trước để tối ưu hóa cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cấp quyền cho toàn bộ thư mục (Hugging Face yêu cầu quyền truy cập non-root)
RUN chmod -R 777 /app

# Lệnh chạy ứng dụng
CMD ["python", "app.py"]
