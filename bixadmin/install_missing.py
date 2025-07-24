import pkgutil, subprocess, sys, os, re

project_dir = os.getcwd()
found_imports = set()

# Scan all .py files in your project
for root, dirs, files in os.walk(project_dir):
    for file in files:
        if file.endswith(".py"):
            with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    match = re.match(r'^\s*(?:from|import)\s+([a-zA-Z0-9_\.]+)', line)
                    if match:
                        package = match.group(1).split('.')[0]
                        found_imports.add(package)

# Check which are missing and install them
for package in sorted(found_imports):
    if pkgutil.find_loader(package) is None:
        print(f"Installing missing package: {package}")
        subprocess.run([sys.executable, "-m", "pip", "install", package])

print("All missing packages have been installed.")