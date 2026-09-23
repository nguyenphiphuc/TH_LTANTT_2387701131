# Buổi 1 - Lab 3: Ghi nhật ký ưu tiên bảo mật (SecureLogger)

## Thông tin sinh viên
- Họ và tên: Nguyễn Phi Phúc
- MSSV: 2387701131

## Kết quả đạt được
- Xây dựng hệ thống SecureLogger theo cấu trúc JSON.
- Tự động phát hiện và che giấu (mask) thông tin định danh cá nhân (PII như Email, Token).
- Quản lý luân phiên và nén log file (gzip rotation).
- Tính toán và lưu mã băm SHA-256 vào file `secure.log.sig` nhằm phát hiện thay đổi trái phép (tamper detection).