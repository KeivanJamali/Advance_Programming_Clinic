import subprocess

REQUIRED_PACKAGES = [
    "datetime",
    "mysql-connector-python",
    "tabulate"
]


def check_and_install_libraries():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
            print(f"{package} is already installed.")
        except ImportError:
            print(f"{package} is not installed. Installing...")
            subprocess.check_call(["pip", "install", package])
            print(f"{package} is successfully installed.")


def main():
    check_and_install_libraries()
