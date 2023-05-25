import time

from main_kazeros_heroku import run_bot

parameters = [
    ("South America", "Kazeros", "Kazeros / SA", '-1001538174798'),
    ("South America", "Arthetine", "Arthetine / SA", '-943556783'),
    ("South America", "Blackfang", "Blackfang / SA", '-861248244'),
    ("NA East", "Adrinne", "Adrinne / NA East", '-825012817'),
    ("NA East", "Aldebaran", "Aldebaran / NA East", '-946782213'),
    ("NA East", "Avesta", "Avesta / NA East", '-987673841'),
    ("NA East", "Azena", "Azena / NA East", '-959219503'),
    ("NA East", "Danube", "Danube / NA East", '-996260314'),
    ("NA East", "Elzowin", "Elzowin / NA East", '-942225425'),
    ("NA East", "Galatur", "Galatur / NA East", '-836742275'),
    ("NA East", "Karta", "Karta / NA East", '-933240393'),
    ("NA East", "Kharmine", "Kharmine / NA East", '-810193440'),
    ("NA East", "Ladon", "Ladon / NA East", '-808925138'),
    ("NA East", "Regulus", "Regulus / NA East", '-851396099'),
    ("NA East", "Sasha", "Sasha / NA East", '-906136865'),
    ("NA East", "Una", "Una / NA East", '-943045643'),
    ("NA East", "Vykas", "Vykas / NA East", '-953577345'),
    ("NA East", "Zosma", "Zosma / NA East", '-999646858'),
    ("NA West", "Akkan", "Akkan / NA West", '-706325026'),
    ("NA West", "Bergstrom", "Bergstrom / NA West", '-977095778'),
    ("NA West", "Enviska", "Enviska / NA West", '-930233732'),
    ("NA West", "Mari", "Mari / NA West", '-927539127'),
    ("NA West", "Rohendel", "Rohendel / NA West", '-966685928'),
    ("NA West", "Shandi", "Shandi / NA West", '-928806223'),
    ("NA West", "Valtan", "Valtan / NA West", '-870455951'),
    ("EU Central", "Antares", "Antares / EU Central", '-949864095'),
    ("EU Central", "Armen", "Armen / EU Central", '-998381556'),
    ("EU Central", "Asta", "Asta / EU Central", '-938419838'),
    ("EU Central", "Calvasus", "Calvasus / EU Central", '-920031025'),
    ("EU Central", "Evergrace", "Evergrace / EU Central", '-602541064'),
    ("EU Central", "Ezrebet", "Ezrebet / EU Central", '-993399201'),
    ("EU Central", "Kadan", "Kadan / EU Central", '-921287726'),
    ("EU Central", "Lazenith", "Lazenith / EU Central", '-805937304'),
    ("EU Central", "Mokoko", "Mokoko / EU Central", '-831250041'),
    ("EU Central", "Neria", "Neria / EU Central", '-931235917'),
    ("EU Central", "Slen", "Slen / EU Central", '-926516808'),
    ("EU Central", "Thirain", "Thirain / EU Central", '-961278841'),
    ("EU Central", "Trixion", "Trixion / EU Central", '-640849733'),
    ("EU Central", "Wei", "Wei / EU Central", '-940298065'),
    ("EU Central", "Zinnervale", "Zinnervale / EU Central", '-923781616'),
    ("EU West", "Ealyn", "Ealyn / EU West", '-809988789'),
    ("EU West", "Nia", "Nia / EU West", '-892872088'),
]

for params in parameters:
    run_bot(*params)
    time.sleep(1)
