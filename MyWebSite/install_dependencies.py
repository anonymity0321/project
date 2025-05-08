# install_dependencies.py
import subprocess
import sys

def install_packages():
    try:
        # 执行pip install命令安装requirements.txt中的所有库
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("所有依赖库安装成功！")
    except subprocess.CalledProcessError as e:
        print(f"安装依赖库时出错: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == "__main__":
    install_packages()