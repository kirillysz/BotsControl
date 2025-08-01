from bot_manager.instance import BotInstance
from bot_manager.core import BotManager
from bot_manager.process_utils import ProcessUtils

# Цвета для терминала (ANSI)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'  # Сброс цвета
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_menu():
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== Менеджер ботов ==={Colors.ENDC}\n")
    print(f"{Colors.OKGREEN}1.{Colors.ENDC} Добавить бота")
    print(f"{Colors.OKGREEN}2.{Colors.ENDC} Запустить бота")
    print(f"{Colors.OKGREEN}3.{Colors.ENDC} Остановить бота")
    print(f"{Colors.OKGREEN}4.{Colors.ENDC} Перезапустить бота")
    print(f"{Colors.OKGREEN}5.{Colors.ENDC} Статус бота")
    print(f"{Colors.OKGREEN}0.{Colors.ENDC} Выход")
    print("-" * 30)

def main():
    bot_manager = BotManager(bots=[])

    while True:
        print_menu()
        choice = input(f"{Colors.OKCYAN}Выберите действие:{Colors.ENDC} ").strip()

        if choice == "1":
            print(f"{Colors.BOLD}Добавление нового бота:{Colors.ENDC}")
            name = input("  Имя бота: ").strip()
            bot_path = input("  Путь к боту: ").strip()
            requirements_path = input("  Путь к requirements.txt: ").strip()

            bot = BotInstance(name=name, bot_path=bot_path, requirements_path=requirements_path)
            bot_manager.add_bot(bot)

        elif choice == "2":
            name = input("Введите имя бота для запуска: ").strip()
            bot_manager.start_bot(name)

        elif choice == "3":
            name = input("Введите имя бота для остановки: ").strip()
            bot_manager.stop_bot(name)

        elif choice == "4":
            name = input("Введите имя бота для перезапуска: ").strip()
            bot_manager.restart_bot(name)

        elif choice == "5":
            name = input("Введите имя бота для проверки статуса: ").strip()
            bot = bot_manager.bots.get(name)
            if not bot:
                print(f"{Colors.FAIL}Бот {name} не найден{Colors.ENDC}")
            else:
                ProcessUtils.status_bot(bot.name, bot.bot_path)

        elif choice == "0":
            print(f"{Colors.OKGREEN}Выход...{Colors.ENDC}")
            break

        else:
            print(f"{Colors.WARNING}Некорректный выбор, попробуйте ещё раз.{Colors.ENDC}")

if __name__ == "__main__":
    main()
