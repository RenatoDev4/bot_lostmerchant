import time

from main_kazeros_heroku import run_bot

parameters = [
    ("South America", "Kazeros", "Kazeros / SA", '-1001538174798'),
    ("South America", "Arthetine", "Arthetine / SA", '-1001538174798'),
    ("South America", "Blackfang", "Blackfang / SA", '-1001538174798'),
]

for params in parameters:
    run_bot(*params)
    time.sleep(1)
