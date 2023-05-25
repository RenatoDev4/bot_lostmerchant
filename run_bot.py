import time

from main_kazeros_heroku import run_bot

parameters = [
    ("South America", "Kazeros", "Kazeros / SA", '-1001538174798',
     '/bot_lostmerchants/sent_messages_kazeros.txt'),
    ("South America", "Arthetine", "Arthetine / SA", '-1001878906754',
     '/bot_lostmerchants/sent_messages_arthetine.txt'),
    ("South America", "Blackfang", "Blackfang / SA", '-1001868489245',
     '/bot_lostmerchants/sent_messages_blackfang.txt'),
]

for params in parameters:
    run_bot(*params)
    time.sleep(1)
