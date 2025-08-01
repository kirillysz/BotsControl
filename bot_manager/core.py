from bot_manager.process_utils import ProcessUtils
from bot_manager.venv_utils import VenvUtils
from bot_manager.instance import BotInstance

class BotManager:
    def __init__(self, bots: list[BotInstance]):
        self.bots = {bot.name: bot for bot in bots}

    def add_bot(self, bot: BotInstance):
        if bot.name in self.bots:
            print(f"[!] Бот с именем {bot.name} уже существует")
            return
        
        self.bots[bot.name] = bot
        VenvUtils.create_venv(bot_path=bot.bot_path)
        VenvUtils.install_requeirements_to_venv(bot_path=bot.bot_path, requirements_path=bot.requirements_path)

    def start_bot(self, bot_name: str):
        bot = self.bots.get(bot_name)
        if not bot:
            print(f"Бот {bot_name} не найден")
            return
        
        ProcessUtils.status_bot(bot_name=bot.name, bot_path=bot.bot_path)
        
        started = ProcessUtils.start_bot(bot_name=bot.name, bot_path=bot.bot_path)
        if started:
            print(f"[+] Бот {bot_name} успешно запущен")
        else:
            print(f"Не удалось запустить бота {bot.name}")

    def stop_bot(self, bot_name: str):
        bot = self.bots.get(bot_name)
        if not bot:
            print(f"Бот {bot_name} не найден")
            return
        
        ProcessUtils.stop_bot(bot.name, bot.bot_path)
        ProcessUtils.status_bot(bot.name, bot.bot_path)

    def restart_bot(self, bot_name: str):
        bot = self.bots.get(bot_name)
        if not bot:
            print(f"Бот {bot_name} не найден")
            return
        
        restarted = ProcessUtils.restart_bot(bot_name=bot.name, bot_path=bot.bot_path)
        if restarted:
            print(f"[+] Бот {bot_name} успешно перезапущен")
        else:
            print(f"Не удалось перезапустить бота {bot.name}")

    