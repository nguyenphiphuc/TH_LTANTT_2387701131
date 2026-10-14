# Bài 4: Bảo mật Web App và API

**Môn học:** Lập trình An ninh Thông tin  
**Sinh viên:** Nguyễn Phi Phúc - 2387701131  

---

## 1. Tổng quan
Thư mục `Buoi4` bao gồm hai phần thực hành chính theo tài liệu học tập:
- **Phần 4.2: Web Vulnerability Scanner (`web-vuln-scanner`)**: Xây dựng công cụ quét và phát hiện các lỗ hổng ứng dụng web phổ biến (Reflected XSS, SQL Injection, CSRF, SSRF), xuất báo cáo phân loại rủi ro và giao diện Web UI bằng Flask.
- **Phần 4.4: JWT Secure Tools (`jwt-security-tools`)**: Triển khai giải pháp bảo mật với JSON Web Token (JWT) và OAuth 2.0 bao gồm API Gateway xác thực Bearer token, công cụ Brute-force mật khẩu yếu (Dictionary attack), bộ kiểm định tính hợp lệ token (Validator), OAuth 2.0 Client và trình quản trị vòng đời token (TokenManager).

---

## 2. Phần 1: Web Vulnerability Scanner (`web-vuln-scanner`)

### Cấu trúc dự án
```text
Buoi4/web-vuln-scanner/
├── report/
│   ├── __init__.py
│   └── report_generator.py      # Bộ tạo báo cáo lỗ hổng
├── scanners/
│   ├── __init__.py
│   ├── csrf_detector.py         # Phát hiện thiếu CSRF token
│   ├── sql_injection_tester.py  # Kiểm tra các biến thể SQL Injection
│   ├── ssrf_tester.py           # Phát hiện truy cập IP/Domain nội bộ (SSRF)
│   └── xss_scanner.py           # Quét Reflected XSS
├── tests/
│   ├── __init__.py
│   ├── test_csrf.py
│   ├── test_sql_injection.py
│   ├── test_ssrf.py
│   ├── test_xss.py
│   └── test_report.py
├── ui/
│   ├── templates/
│   │   ├── index.html           # Trang nhập URL và chọn scanner
│   │   └── result.html          # Trang hiển thị kết quả phân loại rủi ro
│   └── app.py                   # Ứng dụng Flask Web UI
├── main.py                      # Chương trình CLI chạy thử nghiệm
└── requirements.txt
```

### Hướng dẫn chạy và kiểm thử
1. **Chạy toàn bộ Unittest (9 tests):**
   ```powershell
   cd Buoi4/web-vuln-scanner
   python -m unittest discover tests
   ```
   *Kết quả:* `Ran 9 tests in 0.002s - OK`

2. **Chạy kịch bản quét qua dòng lệnh (CLI):**
   ```powershell
   python .\main.py
   ```

3. **Chạy giao diện Web UI:**
   ```powershell
   python .\ui\app.py
   ```
   Truy cập `http://127.0.0.1:5000` trên trình duyệt để sử dụng giao diện quét trực quan.

---

## 3. Phần 2: JWT Security Tools (`jwt-security-tools`)

### Cấu trúc dự án
```text
Buoi4/jwt-security-tools/
├── api_gateway/
│   ├── __init__.py
│   └── gateway.py            # API Gateway bảo vệ endpoint bằng JWT Bearer
├── jwt_cracker/
│   ├── __init__.py
│   └── cracker.py            # Brute-force secret key yếu bằng ThreadPoolExecutor
├── jwt_validator/
│   ├── __init__.py
│   └── validator.py          # Kiểm định chữ ký và hạn dùng token
├── oauth_client/
│   ├── __init__.py
│   └── client.py             # Client Authorization Code flow OAuth 2.0
├── token_manager/
│   ├── __init__.py
│   └── manager.py            # Cấp phát & refresh Access/Refresh Token
├── tests/
│   ├── __init__.py
│   ├── test_api_gateway.py
│   ├── test_cracker.py
│   ├── test_oauth_client.py
│   ├── test_token_manager.py
│   └── test_validator.py
├── main.py                   # Sinh token mẫu và khởi chạy API Gateway
├── pytest.ini
└── requirements.txt
```

### Hướng dẫn chạy và kiểm thử
1. **Chạy bộ kiểm thử tự động với Pytest (7 tests):**
   ```powershell
   cd Buoi4/jwt-security-tools
   $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"; pytest tests/
   ```
   *Kết quả:* `7 passed`

2. **Khởi chạy API Gateway & phát hành Token:**
   ```powershell
   python .\main.py
   ```
   Chương trình sẽ in ra `Access Token`, `Refresh Token` và phục vụ API tại `http://127.0.0.1:5000`.

3. **Kiểm tra chứng thực bằng `curl`:**
   ```bash
   curl -H "Authorization: Bearer <access_token>" http://127.0.0.1:5000/protected
   ```
   *Phản hồi khi token hợp lệ:*
   ```json
   {"message": "Access granted", "user": "phuoc"}
   ```
   *Phản hồi khi token sai hoặc không có header:*
   ```json
   {"message": "Access denied"}
   ```
