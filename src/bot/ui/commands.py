from maxapi.types import BotCommand

def create_commands():
    return (
        BotCommand(name='/start', description='Старт'),
        BotCommand(name='/menu', description='Меню'),
        BotCommand(name='/choose_region', description='Выбрать/изменить регион')
    )
