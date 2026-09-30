<div align="center">
  <h1>🛡️ MẬT MÃ HIỆN ĐẠI & TRIỂN KHAI PKI 🛡️</h1>
  <p><i>Báo cáo thực hành Buổi 2 - Môn học An Toàn Thông Tin</i></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python">
    <img src="https://img.shields.io/badge/Framework-Flask%20%7C%20Tkinter-brightgreen.svg" alt="Frameworks">
    <img src="https://img.shields.io/badge/Security-Cryptography%20%7C%20Argon2-red.svg" alt="Security">
  </p>
</div>

---

## 📖 1. Tổng quan dự án

Dự án này được xây dựng nhằm hiện thực hóa các kiến thức chuyên sâu về **Mật mã học hiện đại** và **Hạ tầng khóa công khai (PKI)**. Thay vì chỉ dừng lại ở lý thuyết, dự án mang đến trải nghiệm thực tế với hai phân hệ lõi:

- 🧰 **Crypto Toolkit (Phân hệ Mã hóa):** Một thư viện toàn diện cung cấp các giải pháp bảo mật dữ liệu, từ mã hóa file (AES), chữ ký số (RSA) cho đến băm mật khẩu chống tấn công phần cứng (Argon2).
- 🏛️ **Mini CA (Phân hệ Chứng chỉ số):** Trình mô phỏng hoàn chỉnh vòng đời của một chứng chỉ điện tử chuẩn X.509, tái hiện lại mô hình Chain of Trust từ Root CA đến End-Entity.

---

## 🚀 2. Phân hệ Crypto Toolkit (crypto-toolkit)

### ✨ Tính năng cốt lõi
* 🔒 **Mã hóa đối xứng (AES-256-GCM):** Đảm bảo tính bảo mật và toàn vẹn tuyệt đối cho tệp tin.
* 🔑 **Mã hóa bất đối xứng (RSA-2048):** Tạo cặp khóa, hỗ trợ quy trình ký số và xác thực chữ ký (PKCS#1 v1.5).
* 🛡️ **Băm mật khẩu an toàn (Argon2):** Vận dụng thuật toán hiện đại nhất chống lại Brute-force & phần cứng chuyên dụng (GPU/ASIC).
* 💻 **Đa nền tảng giao tiếp:** Hỗ trợ tương tác qua **Giao diện dòng lệnh (CLI)**, **Giao diện đồ họa (GUI)** và **RESTful API (Flask)**.

### 📸 Demo thực tế & Đánh giá (Lab 1)

> **[Unit Test]** Xác thực tính đúng đắn của thuật toán mã hóa và băm mật khẩu.
<div align="center"><img src="./images/crypto_test.png" alt="Unit Test"></div>

> **[Command Line Interface]** Vận hành mã hóa và giải mã file với tốc độ cao trực tiếp từ Terminal.
<div align="center">
  <img src="./images/crypto_cli_encrypt.png" alt="CLI Encrypt"><br><br>
  <img src="./images/crypto_cli_decrypt.png" alt="CLI Decrypt">
</div>

> **[Graphical User Interface]** Trải nghiệm người dùng thân thiện, trực quan với Tkinter.
<div align="center"><img src="./images/crypto_gui.png" alt="GUI"></div>

> **[Flask REST API]** Tích hợp dịch vụ mã hóa vào nền tảng Web, kiểm thử qua Thunder Client / Postman.
<div align="center">
  <img src="./images/crypto_flask_run.png" alt="Flask Server"><br><br>
  <img src="./images/crypto_flask_postman.png" alt="API Test">
</div>

---

## 🏛️ 3. Phân hệ Mini Certificate Authority (mini-ca)

### ✨ Tính năng cốt lõi
* 🥇 **Thiết lập Cấu trúc CA (Hierarchy):** Khởi tạo thành công **Root CA** (tự ký) và phân quyền cấp phát cho **Intermediate CA**.
* 📜 **Quản lý Vòng đời Chứng chỉ:** Phát hành chứng chỉ số chuẩn X.509 cho End-Entity (người dùng, máy chủ).
* 🔗 **Xác thực Chuỗi niềm tin (Chain of Trust):** Kiểm tra tính hợp pháp của chứng chỉ từ cấp thấp nhất lên đến Root CA.
* 🚫 **Quản lý Thu hồi (Revocation & OCSP):** Lập danh sách thu hồi chứng chỉ và kiểm tra trạng thái hiệu lực theo thời gian thực.

### 📸 Demo thực tế & Đánh giá (Lab 2)

> **[Quy trình PKI qua CLI]** Kịch bản tự động hóa từ việc tạo CA, cấp chứng chỉ đến thu hồi.
<div align="center"><img src="./images/minica_cli.png" alt="CLI Process"></div>

> **[Lưu trữ Chứng chỉ]** Các file .pem chứa khóa và chứng chỉ số X.509 được trích xuất an toàn.
<div align="center"><img src="./images/minica_certs.png" alt="Certificates"></div>

> **[Trải nghiệm Mini CA qua GUI]** Thao tác phát hành và quản lý chứng chỉ điện tử chỉ với vài cú click chuột.
<div align="center">
  <img src="./images/minica_gui_1.png" alt="Create CA">
  <br>
  <img src="./images/minica_gui_2.png" alt="Issue Cert">
  <br>
  <img src="./images/minica_gui_3.png" alt="Verify Chain">
  <br>
  <img src="./images/minica_gui_4.png" alt="Revoke Cert">
  <br>
  <img src="./images/minica_gui_5.png" alt="Check OCSP">
</div>

---

<div align="center">
  <b><i>👨‍💻 Dự án thực hành thuộc môn học An Toàn Thông Tin - Phát triển bởi Nguyễn Phi Phúc - 2387701131 👨‍💻</i></b>
</div>
