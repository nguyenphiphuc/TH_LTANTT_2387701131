import json
import os
import sys

KNOWN_VULNERABLE_PACKAGES = {
    "lodash": "< 4.17.21",
    "axios": "< 1.7.4",
    "semver": "< 7.5.2",
    "minimist": "< 1.2.6",
    "json5": "< 2.2.2"
}

def scan_package_json(filepath):
    warnings = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        deps = {}
        if "dependencies" in data:
            deps.update(data["dependencies"])
        if "devDependencies" in data:
            deps.update(data["devDependencies"])
        
        for pkg, ver in deps.items():
            if pkg in KNOWN_VULNERABLE_PACKAGES:
                warnings.append(f"Thu vien '{pkg}' (phien ban {ver}) can kiem tra: yeu cau an toan la {KNOWN_VULNERABLE_PACKAGES[pkg]}")
    except Exception as e:
        warnings.append(f"Loi doc file {filepath}: {str(e)}")
    return warnings

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"[*] DevSecOps Software Composition Analysis (SCA): Scanning '{target}'...")
    total_warnings = 0
    for root, dirs, files in os.walk(target):
        if "node_modules" in root or ".git" in root:
            continue
        for file in files:
            if file == "package.json":
                path = os.path.join(root, file)
                warns = scan_package_json(path)
                if warns:
                    print(f"[-] Canh bao SCA trong {path}:")
                    for w in warns:
                        print(f"    - {w}")
                    total_warnings += len(warns)
    if total_warnings == 0:
        print("[+] PASS: Khong phat hien phu thuoc thu vien chua lo hong nghiem trong.")
        sys.exit(0)
    else:
        print(f"[*] Tong so luot ra soat phu thuoc: {total_warnings}")
        sys.exit(0)

if __name__ == "__main__":
    main()
