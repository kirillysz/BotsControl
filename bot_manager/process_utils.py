import os
import psutil
import time
import subprocess

class ProcessUtils:

    @staticmethod
    def _get_pid(bot_name: str, bot_path: str) -> int | None:
        pid_file = os.path.join(bot_path, f"{bot_name}.pid")

        if not os.path.exists(pid_file):
            return None
        try:
            with open(pid_file, "r") as f:
                return int(f.read().strip())
        except ValueError:
            return None
        
    @staticmethod
    def _remove_pid_file(bot_name: str, bot_path: str):
        pid_file = os.path.join(bot_path, f"{bot_name}.pid")

        if not os.path.exists(pid_file):
            return None
        try:
            os.remove(pid_file)
            print(f"[~] PID-файл {pid_file} удалён.")
        except Exception as e:
            print(f"[!] Не удалось удалить PID-файл {pid_file}: {e}")


    @staticmethod
    def start_bot(bot_name: str, bot_path: str) -> bool:
        venv_path = os.path.join(bot_path, "venv")
        python_bin = os.path.join(venv_path, "bin", "python")

        for entry in ["bot.py", "main.py"]:
            bot_file = os.path.join(bot_path, entry)
            if os.path.isfile(bot_file):
                break
        else:
            print(f"[!] Не найдена точка входа (main.py или bot.py) в {bot_path}")
            return False

        log_dir = "log"
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, f"{bot_name}.log")

        try:
            with open(log_path, "a") as log_file:
                process = subprocess.Popen(
                    [python_bin, bot_file],
                    stdout=log_file,
                    stderr=log_file,
                    stdin=subprocess.DEVNULL
                )

                pid_file = os.path.join(bot_path, f"{bot_name}.pid")
                with open(pid_file, "w") as f:
                    f.write(str(process.pid))

            print(f"[+] Бот {bot_name} запущен с PID {process.pid}")
            return True
        
        except Exception as e:
            print(f"[!] Ошибка при запуске бота {bot_name}: {e}")
            return False

    @staticmethod
    def stop_bot(bot_name: str, bot_path: str, timeout: float = 5.0):
        pid = ProcessUtils._get_pid(bot_name, bot_path)
        if pid is None:
            print(f"[-] PID не найден для {bot_name}")
            return
        
        if not psutil.pid_exists(pid):
            print(f"[!] Процесс {pid} уже удален")
            ProcessUtils._remove_pid_file(bot_name, bot_path)
            return
        
        try:
            proc = psutil.Process(pid)
            print(f"[~] Завершаем процесс {pid} ({bot_name})...")
            proc.terminate()

            try:
                proc.wait(timeout=timeout)
                print(f"[x] Бот {bot_name} завершён.")

            except psutil.TimeoutExpired:
                print(f"[!] Не ответил — убиваем...")

                proc.kill()
                proc.wait()

                print(f"[x] Бот {bot_name} принудительно завершён.")

            except psutil.NoSuchProcess:
                print(f"[!] Процесс {pid} не найден.")

            except psutil.AccessDenied:
                print(f"[!] Нет прав на завершение процесса {pid}.")

        finally:
            ProcessUtils._remove_pid_file(bot_name, bot_path)

    @staticmethod
    def status_bot(bot_name: str, bot_path: str) -> bool:
        pid = ProcessUtils._get_pid(bot_name, bot_path)
        if pid is None:
            print(f"[•] Бот {bot_name}: не запущен (PID-файл не найден).")
            return
        
        if psutil.pid_exists(pid):
            proc = psutil.Process(pid)
            print(f"[✓] Бот {bot_name} работает (PID {pid}, {proc.name()})")
        
        else:
            print(f"[•] Бот {bot_name}: не запущен.")
            ProcessUtils._remove_pid_file(bot_name, bot_path)

    @staticmethod
    def restart_bot(bot_name: str, bot_path: str):
        print(f"[↻] Перезапуск бота {bot_name}...")

        ProcessUtils.stop_bot(bot_name, bot_path)
        time.sleep(1)
        ProcessUtils.start_bot(bot_name, bot_path)

