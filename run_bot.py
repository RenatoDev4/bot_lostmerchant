import time

from main_kazeros_heroku import run_bot

parameters = [
    ("South America", "Kazeros", '-1001538174798',
     '/bot_lostmerchants/sent_messages_kazeros.txt'),
    ("South America", "Arthetine", '-1001878906754',
     '/bot_lostmerchants/sent_messages_arthetine.txt'),
    ("South America", "Blackfang", '-1001868489245',
     '/bot_lostmerchants/sent_messages_blackfang.txt'),
]

for params in parameters:
    run_bot(*params)
    time.sleep(1)
