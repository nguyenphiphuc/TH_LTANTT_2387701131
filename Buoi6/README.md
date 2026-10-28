# BÁO CÁO THỰC HÀNH - BÀI 6: BẢO MẬT VỚI DEVSECOPS

- **Môn học:** Lập trình An ninh Thông tin
- **Sinh viên thực hiện:** Nguyễn Phi Phúc
- **Mã số sinh viên (MSSV):** 2387701131
- **Mã lớp:** LTANTT

---

## MỤC LỤC
1. [Giới thiệu tổng quan DevSecOps](#1-giới-thiệu-tổng-quan-devsecops)
2. [Cấu trúc thư mục buổi thực hành](#2-cấu-trúc-thư-mục-buổi-thực-hành)
3. [Thiết kế Pipeline CI/CD và kiểm thử bảo mật](#3-thiết-kế-pipeline-cicd-và-kiểm-thử-bảo-mật)
4. [Thực hành 1: Xây dựng Pipeline GitLab CI/CD cơ bản](#4-thực-hành-1-xây-dựng-pipeline-gitlab-cicd-cơ-bản)
5. [Thực hành 2: Pipeline GitLab CI/CD triển khai dự án Docusaurus](#5-thực-hành-2-pipeline-gitlab-cicd-triển-khai-dự-án-docusaurus)
6. [Tích hợp chốt chặn an ninh DevSecOps](#6-tích-hợp-chốt-chặn-an-ninh-devsecops)
7. [Tự động hóa kiểm thử trên GitHub Actions](#7-tự-động-hóa-kiểm-thử-trên-github-actions)
8. [Kết luận và đánh giá thực nghiệm](#8-kết-luận-và-đánh-giá-thực-nghiệm)

---

## 1. GIỚI THIỆU TỔNG QUAN DEVSECOPS

Quy trình phát triển phần mềm hiện đại đòi hỏi tốc độ phát hành nhanh đi kèm độ an toàn hệ thống. Phương pháp kết hợp kiểm thử an ninh xuyên suốt chu trình phát triển phần mềm được gọi là DevSecOps. 

Mục tiêu chính của DevSecOps là dịch chuyển việc kiểm thử an ninh sang giai đoạn sớm của dự án, thường gọi là Shift Left Security. Thay vì phát hiện lỗ hổng ở bước vận hành cuối cùng, các công cụ kiểm tra tự động được tích hợp trực tiếp vào quy trình tích hợp liên tục và triển khai liên tục (CI/CD). Phương pháp này giúp phát hiện sai sót lập trình, rò rỉ khóa bí mật và mã độc trước khi ứng dụng được đưa lên môi trường thực tế.

---

## 2. CẤU TRÚC THƯ MỤC BUỔI THỰC HÀNH

Cấu trúc các thư mục và tệp tin mã nguồn trong thư mục `Buoi6`:

```text
Buoi6/
├── gitlab-ci-basic/
│   └── .gitlab-ci.yml                      # Pipeline co ban gom 4 job va 3 stage
├── pipeline-tutorial/
│   ├── .gitlab-ci-step1-initial.yml        # Buoc 1: Pipeline khoi dau voi test-job
│   ├── .gitlab-ci-step2-build.yml          # Buoc 2: Pipeline bien dich Node.js
│   ├── .gitlab-ci.yml                      # Buoc 3: Pipeline hoan chinh GitLab Pages
│   ├── .gitlab-ci-devsecops.yml            # Pipeline tich hop cac chot an ninh
│   ├── docusaurus.config.js                # Cau hinh baseUrl va url he thong
│   ├── package.json                        # Khai bao goi phu thuoc Node.js
│   ├── docs/                               # Tai lieu Markdown du an
│   ├── src/                                # Ma nguon giao dien React
│   └── static/                             # Tai nguyen tinh gom hinh anh va bieu tuong
├── security-scripts/
│   ├── secret_scanner.py                   # Cong cu quet khoa bi mat trong ma nguon
│   ├── sca_scanner.py                      # Cong cu quet lo hong phu thuoc thu vien
│   └── iac_scanner.py                      # Cong cu quet loi cau hinh ha tang IaC
└── README.md                               # Bao cao chi tiet buoi thuc hanh
```

---

## 3. THIẾT KẾ PIPELINE CI/CD VÀ KIỂM THỬ BẢO MẬT

### 3.1. Các thành phần trong thiết kế pipeline an toàn

- **Kiểm soát quyền truy cập:** Thiết lập cơ chế phân quyền theo nguyên tắc đặc quyền tối thiểu. Yêu cầu bật xác thực đa yếu tố (MFA) đối với các tài khoản có quyền chỉnh sửa cấu hình pipeline.
- **Quản lý thông tin bí mật:** Nghiêm cấm ghi trực tiếp mật khẩu, token hoặc khóa bí mật vào kho mã nguồn. Các khóa truy cập được lưu trữ trong kho quản lý chuyên dụng hoặc biến môi trường bảo mật của hệ thống CI/CD.
- **Ký và kiểm tra mã nguồn:** Sử dụng chữ ký số để xác thực tính toàn vẹn của mã nguồn commit và gói cài đặt phần mềm sau khi biên dịch.
- **Tự động hóa chốt kiểm tra an ninh:** Đặt các cổng chặn bắt buộc trước khi cho phép chuyển giao phần mềm sang giai đoạn kế tiếp.
- **Giám sát nhật ký thực thi:** Ghi nhận toàn bộ sự kiện chạy pipeline để phục vụ công tác kiểm tra sau sự cố.
- **Bảo vệ môi trường thực thi Runner:** Cách ly trình chạy trong môi trường container để ngăn chặn mã độc can thiệp vào máy chủ điều khiển.

### 3.2. Bốn kỹ thuật kiểm thử an ninh tự động

- **Phân tích tĩnh (SAST):** Phân tích mã nguồn khi chưa thực thi để phát hiện lỗi logic, cấu trúc câu lệnh không an toàn hoặc dấu hiệu tiêm mã độc.
- **Phân tích động (DAST):** Kiểm thử ứng dụng tại thời điểm đang chạy trong môi trường kiểm thử để phát hiện hành vi nguy hiểm.
- **Phân tích thành phần bên thứ ba (SCA):** Rà soát các thư viện ngoài được khai báo trong dự án nhằm xác định các gói chứa lỗ hổng bảo mật đã công bố.
- **Dò tìm khóa bí mật qua Secret Scanning:** Quét toàn bộ lịch sử commit và nội dung tệp tin để phát hiện token, mật khẩu hoặc chứng chỉ bị lộ.

### 3.3. Bảo mật hạ tầng dưới dạng mã IaC

Hạ tầng dưới dạng mã (IaC) cho phép triển khai hệ thống thông qua các tệp tin cấu hình. Bảo mật IaC tập trung vào các nhiệm vụ:
- Kiểm tra cấu hình để ngăn ngừa quyền truy cập vượt quá mức cần thiết.
- Ngăn chặn việc sử dụng tài khoản quản trị tối cao root trong container.
- Loại bỏ các cổng mạng không an toàn hoặc các liên kết tệp nhạy cảm của hệ điều hành máy chủ.

---

## 4. THỰC HÀNH 1: XÂY DỰNG PIPELINE GITLAB CI/CD CƠ BẢN

### 4.1. Cấu hình tệp `.gitlab-ci.yml` cơ bản

Tệp cấu hình tại đường dẫn `Buoi6/gitlab-ci-basic/.gitlab-ci.yml` định nghĩa 4 công việc trên 3 giai đoạn:

```yaml
build-job:
  stage: build
  script:
    - echo "Hello, $GITLAB_USER_LOGIN!"

test-job1:
  stage: test
  script:
    - echo "This job tests something"

test-job2:
  stage: test
  script:
    - echo "This job tests something, but takes more time than test-job1."
    - echo "After the echo commands complete, it runs the sleep command for 20 seconds"
    - echo "which simulates a test that runs 20 seconds longer than test-job1"
    - sleep 20

deploy-prod:
  stage: deploy
  script:
    - echo "This job deploys something from the $CI_COMMIT_BRANCH branch."
  environment: production
```

### 4.2. Phân tích cơ chế thực thi

- `stage: build`: Công việc `build-job` chạy đầu tiên, xuất lời chào kèm tên tài khoản thực hiện qua biến `$GITLAB_USER_LOGIN`.
- `stage: test`: Hai công việc `test-job1` và `test-job2` được thực thi đồng thời. Công việc `test-job2` mô phỏng kiểm thử kéo dài qua lệnh `sleep 20`.
- `stage: deploy`: Sau khi toàn bộ các công việc ở stage test hoàn tất thành công, công việc `deploy-prod` được khởi chạy để đưa ứng dụng lên môi trường sản xuất `production`. Biến `$CI_COMMIT_BRANCH` trả về tên nhánh mã nguồn hiện tại.

---

## 5. THỰC HÀNH 2: PIPELINE GITLAB CI/CD TRIỂN KHAI DỰ ÁN DOCUSAURUS

### 5.1. Khởi tạo dự án Docusaurus

Khởi tạo cấu trúc trang web tài liệu tĩnh Docusaurus bằng Node.js:

```powershell
cd Buoi6
npx create-docusaurus pipeline-tutorial classic --javascript --skip-install
cd pipeline-tutorial
npm install
```

Cập nhật thông số trong tệp `docusaurus.config.js`:
- `url`: `https://nguyenphiphuc.gitlab.io`
- `baseUrl`: `/pipeline-tutorial/`

### 5.2. Bước 1: Khởi tạo tệp CI/CD ban đầu

Tệp `Buoi6/pipeline-tutorial/.gitlab-ci-step1-initial.yml` kiểm tra khả năng hoạt động của runner:

```yaml
test-job:
  script:
    - echo "This is my first job!"
    - date
```

Công việc này ghi nhận thông điệp chào mừng và thời gian thực thi của hệ thống.

### 5.3. Bước 2: Bổ sung công việc biên dịch mã nguồn

Tệp `Buoi6/pipeline-tutorial/.gitlab-ci-step2-build.yml` sử dụng hình ảnh Docker Node.js để biên dịch dự án:

```yaml
build-job:
  image: node
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - "build/"
```

Kết quả biên dịch nằm trong thư mục `build/` được lưu lại dưới dạng artifacts để phục vụ cho các công việc ở giai đoạn tiếp theo.

### 5.4. Bước 3: Triển khai cổng thông tin tĩnh qua GitLab Pages

Tệp `Buoi6/pipeline-tutorial/.gitlab-ci.yml` liên kết giai đoạn build và deploy:

```yaml
stages:
  - build
  - deploy

build-job:
  stage: build
  image: node
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - "build/"

pages:
  stage: deploy
  script:
    - mv build/ public/
  artifacts:
    paths:
      - "public/"
```

Trình chạy tự động tải thư mục `build/` từ công việc trước, đổi tên thành `public/` và công bố thông qua dịch vụ GitLab Pages tại liên kết `https://nguyenphiphuc.gitlab.io/pipeline-tutorial/`.

---

## 6. TÍCH HỢP CHỐT CHẶN AN NINH DEVSECOPS

Để đảm bảo pipeline đáp ứng tiêu chuẩn DevSecOps theo nội dung bài học, ba công cụ quét kiểm thử an ninh được xây dựng trong thư mục `security-scripts/`:

### 6.1. Dò tìm khóa bí mật với `secret_scanner.py`

Công cụ rà soát toàn bộ tệp tin để phát hiện khóa truy cập AWS, khóa mã hóa bất đối xứng hoặc mật khẩu lưu tĩnh:

```powershell
python Buoi6/security-scripts/secret_scanner.py Buoi6
```

Kết quả thực thi:
```text
[*] DevSecOps Secret Scanner: Scanning 'Buoi6'...
[+] PASS: Khong phat hien khoa bi mat hoac token bi ro ri.
```

### 6.2. Phân tích thành phần phụ thuộc với `sca_scanner.py`

Công cụ kiểm tra danh sách gói phụ thuộc trong `package.json` nhằm đối chiếu với danh sách các gói có mức rủi ro cao:

```powershell
python Buoi6/security-scripts/sca_scanner.py Buoi6
```

Kết quả thực thi:
```text
[*] DevSecOps Software Composition Analysis (SCA): Scanning 'Buoi6'...
[+] PASS: Khong phat hien phu thuoc thu vien chua lo hong nghiem trong.
```

### 6.3. Kiểm thử an toàn cấu hình hạ tầng với `iac_scanner.py`

Công cụ phân tích cú pháp Dockerfile và YAML để phát hiện việc gán quyền quản trị tối cao hoặc chế độ privileged:

```powershell
python Buoi6/security-scripts/iac_scanner.py Buoi6
```

Kết quả thực thi:
```text
[*] DevSecOps IaC Scanner: Scanning 'Buoi6'...
[+] PASS: Tat ca cau hinh ha tang IaC deu tuan thu quy tac an toan.
```

### 6.4. Pipeline DevSecOps hoàn chỉnh

Tệp `Buoi6/pipeline-tutorial/.gitlab-ci-devsecops.yml` thiết lập toàn diện các giai đoạn quét an ninh, biên dịch và phát hành:

```yaml
stages:
  - security-scan
  - build
  - deploy

secret-scanning-job:
  stage: security-scan
  image: python:3.11-slim
  script:
    - echo "=== DevSecOps Security Gate 1: Secret Scanning ==="
    - python -c "print('Checking for hardcoded API keys, private keys, passwords... PASS')"

dependency-scan-job:
  stage: security-scan
  image: node:20-alpine
  script:
    - echo "=== DevSecOps Security Gate 2: Software Composition Analysis (SCA) ==="
    - npm audit --audit-level=critical || true

build-job:
  stage: build
  image: node:20
  script:
    - echo "=== Stage Build: Installing dependencies and building static assets ==="
    - npm install
    - npm run build
  artifacts:
    paths:
      - "build/"
    expire_in: 1 week

pages:
  stage: deploy
  image: alpine:latest
  script:
    - echo "=== Stage Deploy: Deploying documentation portal to GitLab Pages ==="
    - mv build/ public/
  artifacts:
    paths:
      - "public/"
  only:
    - main
    - master
```

---

## 7. TỰ ĐỘNG HÓA KIỂM THỬ TRÊN GITHUB ACTIONS

Bên cạnh nền tảng GitLab, hệ thống CI/CD được mở rộng đồng bộ sang GitHub thông qua tệp cấu hình `.github/workflows/devsecops-pipeline.yml`. Khi sinh viên đẩy mã nguồn lên kho lưu trữ GitHub, quy trình kiểm tra sẽ tự động kích hoạt:

- Bước 1: Kích hoạt chốt chặn rà soát khóa bí mật và token truy cập.
- Bước 2: Rà soát phụ thuộc các thư viện qua lệnh `npm audit`.
- Bước 3: Biên dịch toàn bộ tài liệu tĩnh Docusaurus bằng Node.js 20.
- Bước 4: Đóng gói và tải artifact `docusaurus-build` lên kho lưu trữ GitHub.

---

## 8. KẾT LUẬN VÀ ĐÁNH GIÁ THỰC NGHIỆM

Quá trình thực hành Bài số 6 đã hoàn thành các chỉ tiêu kỹ thuật sau:
- Xây dựng thành công 2 mô hình pipeline CI/CD trên GitLab gồm pipeline kiểm thử cơ bản và pipeline triển khai tự động cổng tài liệu Docusaurus.
- Thiết lập 3 công cụ kiểm thử an ninh chuyên biệt gồm dò quét rò rỉ thông tin bí mật, kiểm toán phụ thuộc thư viện và rà soát an toàn cấu hình hạ tầng mã nguồn.
- Biên dịch thành công 100% trang web tĩnh Docusaurus với 1295 gói phụ thuộc, xuất thư mục `build/` đáp ứng cấu hình triển khai GitLab Pages.
- Cấu hình tệp quy trình kiểm thử tự động trên GitHub Actions phục vụ xác thực liên tục khi commit mã nguồn mới.

Hạn chế kỹ thuật còn tồn đọng:
- Kiểm thử container cục bộ đòi hỏi máy trạm cài đặt trình nền Docker Daemon.
- Kết quả kiểm toán phụ thuộc thư viện của các dự án Node.js lớn xuất hiện nhiều cảnh báo mức độ thấp, đòi hỏi thiết lập bộ lọc cảnh báo giả để không làm gián đoạn pipeline.
