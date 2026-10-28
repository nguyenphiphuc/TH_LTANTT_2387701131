import os
import sys

def scan_dockerfile(filepath):
    issues = []
    has_user_directive = False
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f, start=1):
            clean = line.strip()
            if clean.startswith("FROM") and (":latest" in clean or ":" not in clean):
                issues.append(f"Line {idx}: Base image su dung tag 'latest' hoac khong khoa phien ban cu the.")
            if clean.startswith("USER") and not clean.endswith("root"):
                has_user_directive = True
            if "ADD " in clean and ("http://" in clean or "https://" in clean):
                issues.append(f"Line {idx}: Dung lenh ADD de tai file tu xa thay vi curl/wget kem checksum.")
    if not has_user_directive:
        issues.append("Thieu lenh USER phi root: Tien trinh trong container se chay voi quyen root mac dinh.")
    return issues

def scan_yaml_config(filepath):
    issues = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f, start=1):
            clean = line.strip()
            if "privileged: true" in clean:
                issues.append(f"Line {idx}: Container chay o che do dac quyen (privileged: true).")
            if "/var/run/docker.sock" in clean:
                issues.append(f"Line {idx}: Mount truc tiep docker socket vao container gay nguy co thoat khoi sandbox.")
            if "allow_failure: true" in clean:
                issues.append(f"Line {idx}: Canh bao bo qua loi trong pipeline (allow_failure: true).")
    return issues

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"[*] DevSecOps IaC Scanner: Scanning '{target_dir}'...")
    total_issues = 0
    for root, _, files in os.walk(target_dir):
        if "node_modules" in root or ".git" in root:
            continue
        for file in files:
            path = os.path.join(root, file)
            if file.lower() in ["dockerfile", "containerfile"] or file.lower().endswith(".dockerfile"):
                issues = scan_dockerfile(path)
                if issues:
                    print(f"[-] Phat hien van de IaC trong Dockerfile {path}:")
                    for iss in issues:
                        print(f"    - {iss}")
                    total_issues += len(issues)
            elif file.lower().endswith((".yml", ".yaml")):
                issues = scan_yaml_config(path)
                if issues:
                    print(f"[-] Phat hien van de IaC trong YAML {path}:")
                    for iss in issues:
                        print(f"    - {iss}")
                    total_issues += len(issues)
    if total_issues == 0:
        print("[+] PASS: Tat ca cau hinh ha tang IaC deu tuan thu quy tac an toan.")
        sys.exit(0)
    else:
        print(f"[-] Tong so canh bao IaC: {total_issues}")
        sys.exit(0)

if __name__ == "__main__":
    main()
