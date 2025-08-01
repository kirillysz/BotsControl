import os
import subprocess

class VenvUtils:
    
    @staticmethod
    def create_venv(bot_path: str):
        venv_path = os.path.join(bot_path, "venv")

        result = subprocess.run(
            ["python", "-m", "venv", venv_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"VENV создано в  {venv_path}")
        else:
            print(f"Ошибка при создании VENV:\n{result.stderr}")

    @staticmethod
    def install_requeirements_to_venv(bot_path: str, requirements_path: str):
        venv_path = os.path.join(bot_path, "venv")
        pip_executable = os.path.join(venv_path, "bin", "pip")

        install_requirements = subprocess.run(
            [pip_executable, "install", "-r", requirements_path],
            capture_output=True,
            text=True
        )

        if install_requirements.returncode == 0:
            print("Успешная установка зависимостей!")
        else:
            print(f"Ошибка при установке зависимостей:\n{install_requirements.stderr}")
        