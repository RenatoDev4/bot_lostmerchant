import time

from main_kazeros_heroku import run_bot

parameters = [
    ("South America", "Kazeros", "Kazeros / SA", '-1001538174798'),
    ("South America", "Arthetine", "Arthetine / SA", '-1001838502266'),
    ("South America", "Blackfang", "Blackfang / SA", '-1001935567045'),
    ("NA East", "Adrinne", "Adrinne / NA East", '-1001700906483'),
    ("NA East", "Aldebaran", "Aldebaran / NA East", '-1001938544531'),
    ("NA East", "Avesta", "Avesta / NA East", '-1001884097381'),
    ("NA East", "Azena", "Azena / NA East", '-1001926236597'),
    ("NA East", "Danube", "Danube / NA East", '-1001965513544'),
    ("NA East", "Elzowin", "Elzowin / NA East", '-1001622485963'),
    ("NA East", "Galatur", "Galatur / NA East", '-1001479924286'),
    ("NA East", "Karta", "Karta / NA East", '-1001862074492'),
    ("NA East", "Kharmine", "Kharmine / NA East", '-1001655865395'),
    ("NA East", "Ladon", "Ladon / NA East", '-1001957078420'),
    ("NA East", "Regulus", "Regulus / NA East", '-1001848077098'),
    ("NA East", "Sasha", "Sasha / NA East", '-1001849698068'),
    ("NA East", "Una", "Una / NA East", '-1001988962483'),
    ("NA East", "Vykas", "Vykas / NA East", '-1001980716838'),
    ("NA East", "Zosma", "Zosma / NA East", '-1001839269436'),
    ("NA West", "Akkan", "Akkan / NA West", '-1001841978218'),
    ("NA West", "Bergstrom", "Bergstrom / NA West", '-1001931174300'),
    ("NA West", "Enviska", "Enviska / NA West", '-1001893806093'),
    ("NA West", "Mari", "Mari / NA West", '-1001539261477'),
    ("NA West", "Rohendel", "Rohendel / NA West", '-1001843237445'),
    ("NA West", "Shandi", "Shandi / NA West", '-1001671428822'),
    ("NA West", "Valtan", "Valtan / NA West", '-1001975828606'),
    ("EU Central", "Antares", "Antares / EU Central", '-1001812602653'),
    ("EU Central", "Armen", "Armen / EU Central", '-1001900639552'),
    ("EU Central", "Asta", "Asta / EU Central", '-1001551334555'),
    ("EU Central", "Calvasus", "Calvasus / EU Central", '-1001888719445'),
    ("EU Central", "Evergrace", "Evergrace / EU Central", '-602541064'),
    ("EU Central", "Ezrebet", "Ezrebet / EU Central", '-1001811918030'),
    ("EU Central", "Kadan", "Kadan / EU Central", '-1001809249498'),
    ("EU Central", "Lazenith", "Lazenith / EU Central", '-1001976411910'),
    ("EU Central", "Mokoko", "Mokoko / EU Central", '-1001665315135'),
    ("EU Central", "Neria", "Neria / EU Central", '-1001936577030'),
    ("EU Central", "Slen", "Slen / EU Central", '-1001934646335'),
    ("EU Central", "Thirain", "Thirain / EU Central", '-1001903621622'),
    ("EU Central", "Trixion", "Trixion / EU Central", '-1001943158851'),
    ("EU Central", "Wei", "Wei / EU Central", '-1001606684003'),
    ("EU Central", "Zinnervale", "Zinnervale / EU Central", '-1001871403341'),
    ("EU West", "Ealyn", "Ealyn / EU West", '-1001907577566'),
    ("EU West", "Nia", "Nia / EU West", '-1001903621622'),  # OK
]

for params in parameters:
    run_bot(*params)
    time.sleep(1)
