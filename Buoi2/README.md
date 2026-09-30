# 🛡️ Mật mã hiện đại và Triển khai PKI (Buổi 2)

Chào mừng đến với dự án **Mật mã hiện đại và Hệ thống khóa công khai (PKI)**! Dự án này bao gồm hai phần chính: một thư viện mã hóa đa năng (crypto-toolkit) và một hệ thống Certificate Authority thu nhỏ (mini-ca).

---

## 🚀 1. Crypto Toolkit (crypto-toolkit)

Đây là một thư viện Python mạnh mẽ hỗ trợ mã hóa, băm mật khẩu và chữ ký số. Bao gồm mã hóa AES-256-GCM, tạo/ký khóa RSA và băm mật khẩu Argon2.

**Hình ảnh minh họa kết quả (Lab 1):**

*(Ảnh 1: Kết quả chạy Unit Test thành công)*
![Minh họa Crypto Toolkit - Unit Test](./images/crypto_test.png)

*(Ảnh 2: Kết quả mã hóa file thành công qua CLI)*
![Minh họa Crypto Toolkit - CLI Encrypt](./images/crypto_cli_encrypt.png)

*(Ảnh 3: Kết quả giải mã file thành công qua CLI)*
![Minh họa Crypto Toolkit - CLI Decrypt](./images/crypto_cli_decrypt.png)

*(Ảnh 4: Giao diện đồ họa (GUI) mã hóa thành công)*
![Minh họa Crypto Toolkit - GUI](./images/crypto_gui.png)

*(Ảnh 5: Khởi chạy Flask API Server)*
![Minh họa Crypto Toolkit - Flask Server](./images/crypto_flask_run.png)

*(Ảnh 6: Test API /encrypt bằng Postman / Thunder Client thành công)*
![Minh họa Crypto Toolkit - API Test](./images/crypto_flask_postman.png)

---

## 🏛️ 2. Mini Certificate Authority (mini-ca)

Hệ thống mô phỏng cấu trúc hạ tầng khóa công khai (PKI) với chuẩn chứng chỉ X.509. Hỗ trợ tạo Root CA, Intermediate CA, phát hành và thu hồi chứng chỉ.

**Hình ảnh minh họa kết quả (Lab 2):**

*(Ảnh 1: Kết quả chạy demo toàn bộ quy trình PKI qua CLI)*
![Minh họa Mini CA - CLI](./images/minica_cli.png)

*(Ảnh 2: Các file chứng chỉ (.pem) được sinh ra thành công trong thư mục certs)*
![Minh họa Mini CA - Certs Folder](./images/minica_certs.png)

*(Ảnh 3: Khởi tạo Root CA và Intermediate CA qua GUI)*
![Minh họa Mini CA - GUI 1](./images/minica_gui_1.png)

*(Ảnh 4: Phát hành chứng chỉ cho End-Entity qua GUI)*
![Minh họa Mini CA - GUI 2](./images/minica_gui_2.png)

*(Ảnh 5: Xác thực chuỗi chứng chỉ (Chain of Trust) thành công)*
![Minh họa Mini CA - GUI 3](./images/minica_gui_3.png)

*(Ảnh 6: Thu hồi chứng chỉ)*
![Minh họa Mini CA - GUI 4](./images/minica_gui_4.png)

*(Ảnh 7: Kiểm tra trạng thái OCSP)*
![Minh họa Mini CA - GUI 5](./images/minica_gui_5.png)

---
*Dự án thực hành thuộc môn học An Toàn Thông Tin - Phát triển bởi Nguyễn Phi Phúc - 2387701131*
