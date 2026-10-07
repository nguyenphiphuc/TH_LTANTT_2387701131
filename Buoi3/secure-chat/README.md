# Bài 3: Bảo mật Mạng Máy tính - SecureChat

## 1. Giới thiệu
**SecureChat** là ứng dụng trò chuyện (chat) an toàn dựa trên mô hình Client-Server. Ứng dụng tích hợp lập trình Socket kết hợp với các cơ chế bảo mật mạnh mẽ nhằm đảm bảo tính bí mật, toàn vẹn và xác thực của dữ liệu truyền qua mạng, chống lại các nguy cơ đánh chặn và giả mạo.

## 2. Các tính năng bảo mật nổi bật
- **Mã hóa kênh truyền (SSL/TLS):** Sử dụng giao thức TLS 1.2+ để mã hóa đường truyền giữa Client và Server, chống lại các cuộc tấn công nghe lén (eavesdropping) và tấn công xen giữa (Man-In-The-Middle).
- **Xác thực chứng chỉ số (Mutual Authentication):** Server yêu cầu Client xuất trình chứng chỉ hợp lệ (được ký bởi CA tin cậy do chính hệ thống tạo ra) trước khi kết nối, đồng thời Client cũng xác minh danh tính và chứng chỉ của Server.
- **Mã hóa đầu cuối (End-to-End Encryption - E2EE):** Dữ liệu tin nhắn được mã hóa thêm một lớp thứ hai bằng thuật toán đối xứng **AES-256 (chế độ CBC)** với khóa sinh ngẫu nhiên (Session Key) cho từng Client. Lớp mã hóa này đảm bảo dù bản thân Server có bị xâm nhập cũng không thể đọc được nội dung tin nhắn dạng rõ (plaintext).
- **Quản lý đa luồng (Multithreading) & Phân chia phòng (Room):** Xử lý đồng thời nhiều kết nối client cùng lúc không gây block và hỗ trợ tính năng gom nhóm/phòng để phát (broadcast) tin nhắn một cách an toàn.

## 3. Cấu trúc thư mục mã nguồn
```text
secure-chat/
├── certs/                      # Thư mục lưu trữ hệ thống chứng chỉ số (CA, Server, Client)
├── client.py                   # Mã nguồn Client (giao diện CLI, xử lý socket TLS và mã hóa AES)
├── connection_manager.py       # Module quản lý danh sách các client đang kết nối và chia sẻ khóa
├── make-certs.bat              # Script tự động tạo cấu trúc thư mục và sinh chứng chỉ qua OpenSSL
├── message_encryption.py       # Module xử lý cốt lõi việc mã hóa/giải mã thuật toán AES-256
├── openssl.cnf                 # File cấu hình chứa thông số để sinh chứng chỉ X.509
├── room_manager.py             # Module quản lý phân chia phòng chat và luân chuyển gói tin
└── server.py                   # Mã nguồn Server (Thiết lập socket an toàn, load chứng chỉ TLS)
```

## 4. Hướng dẫn cài đặt và cấu hình

### Yêu cầu hệ thống:
1. **Python 3.x**
2. Thư viện mật mã **cryptography**:
   ```bash
   pip install cryptography
   ```
3. Công cụ **OpenSSL**: Yêu cầu cài đặt Win32/Win64 OpenSSL và thêm đường dẫn của thư mục `bin` (VD: `C:\Program Files\OpenSSL-Win64\bin`) vào biến môi trường `PATH` của hệ điều hành.

## 5. Các bước triển khai và khởi chạy

1. **Khởi tạo chứng chỉ số:**
   Mở Terminal tại thư mục `secure-chat`, chạy file batch để khởi tạo CA Root, sau đó ký chứng chỉ cho Server và Client:
   ```bash
   .\make-certs.bat
   ```

2. **Khởi chạy Server:**
   Khởi động tiến trình máy chủ để bắt đầu lắng nghe ở cổng `8443` thông qua socket đã được bọc chứng chỉ TLS:
   ```bash
   python server.py
   ```

3. **Khởi chạy Client (Đóng vai trò người dùng):**
   Mở một terminal mới và khởi động ứng dụng người dùng. Cung cấp tên hiển thị (Username) khi được yêu cầu. Client sẽ tự tạo một Session Key (AES-256) và thiết lập kênh TLS bảo mật tới Server:
   ```bash
   python client.py
   ```
   *(Mở nhiều terminal để giả lập nhiều người dùng khác nhau tham gia phòng trò chuyện).*

## 6. Kết quả thực nghiệm và Kiểm thử
Dưới đây là kết quả kiểm thử thực tế ứng dụng trò chuyện mã hóa **SecureChat**:

1. **Khởi chạy Máy chủ (Server):**
   - Server kích hoạt lắng nghe tại địa chỉ `127.0.0.1:8443` với chứng chỉ số SSL/TLS hợp lệ.
   ```text
   Server listening on 127.0.0.1:8443
   ```

2. **Khởi chạy Máy khách 1 (Alice):**
   - Alice kết nối tới Server thông qua kênh mã hóa TLS, truyền khóa đối xứng AES-256 ngẫu nhiên và bắt đầu gửi tin nhắn.
   ```text
   Username: Alice
   Type messages (type 'exit' to quit):
   dsada
   ádas
   ```

3. **Khởi chạy Máy khách 2 (Bob):**
   - Bob kết nối vào cùng phòng `general`. Server nhận tin nhắn mã hóa AES từ Alice, giải mã và mã hóa lại bằng khóa AES riêng của Bob để truyền đến Bob theo thời gian thực:
   ```text
   Username: Bob
   Type messages (type 'exit' to quit):
   [Alice]: dsada
   [Alice]: ádas
   ```

=> **Kết luận:** Ứng dụng đã hoàn thành đầy đủ các yêu cầu về mã hóa kênh truyền (TLS), xác thực chứng chỉ số (Mutual Auth) và mã hóa nội dung tin nhắn đầu cuối (E2EE AES-256).

---
*Báo cáo bài tập môn Lập trình An toàn Mạng.*
