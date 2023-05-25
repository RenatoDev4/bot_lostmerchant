import datetime
import os
import re
import time

import telebot
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# URL

chrome_options = Options()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path=os.environ.get(
    "CHROMEDRIVER_PATH"), options=chrome_options)
driver.get("https://lostmerchants.com/")


# Localiza o menu usando seu ID
time.sleep(5)

dropdown_server_region = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "severRegion")))

select1 = Select(dropdown_server_region)
select1.select_by_visible_text("South America")

dropdown2 = driver.find_element(By.ID, "server")

select2 = Select(dropdown2)
select2.select_by_visible_text("Kazeros")

time.sleep(10)


# URL PROCURA PRODUTO
html_content = driver.page_source

# INFORMA QUE É UM NAVEGADOR
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}

# Servidor
servidor = "Kazeros / SA"

# Salva o item de Luterra para não enviar em duplicidade
processed_itens = set()


# Função enviar mensagem do BOT
def send_message(mensagem):

    apiToken = '5805754523:AAFIthNp4MtRuN3bbzpyD2gYqFOCFHxQDWg'
    chatID = '-1001538174798'
    bot = telebot.TeleBot(apiToken)
    # Read the list of messages already sent from a file
    with open('/home/renato/bot_lostmerchants/sent_messages_kazeros.txt', 'r') as f:
        sent_messages = f.read().splitlines()

    # Check if the new message is in the list of sent messages
    if message not in sent_messages:
        # Send the message
        bot.send_message(chat_id=chatID, text=message, parse_mode='HTML')

        # If the message is sent successfully, save it to the file
        with open('/home/renato/bot_lostmerchants/sent_messages_kazeros.txt', 'a') as f:
            f.write(message + '\n')
    else:
        pass

# COMEÇA O WEB SCRAPING


soup = BeautifulSoup(html_content, "html.parser")
dic_merchant = {'local': [], 'itens': [], 'tempo': []}

#  PEGA O TEMPO QUE FALTA PARA ACABAR
data_tempo = soup.find_all('div', class_='merchants__content')

for time_ in data_tempo:
    tempo = time_.find('span', class_='merchants__timer')
    if tempo is not None:
        for final_tempo in tempo:
            final_t = final_tempo.text
            final_t = final_t.replace("Expires in ", "")
            dic_merchant['tempo'].append(final_t)
            print(final_t)

# PEGA OS LOCAIS E ITENS DO SITE
data = soup.find_all('div', class_='merchant merchant-grid__item')
for quote in soup.find_all('span', class_="item__tooltip"):
    quote.decompose()

for merchant in data:
    local = merchant.find_all('div', class_='card-frame__title')
    for title in local:
        final_local = title.text
        dic_merchant['local'].append(final_local)
        print(final_local)

    itens = merchant.find_all('div', class_='stock__item')
    for w_itens in itens:
        final_itens = w_itens.text
        dic_merchant['itens'].append(final_itens)
        print(final_itens)


local_str = ' '.join([s for s in dic_merchant['local'] if isinstance(s, str)])
itens_str = ' '.join([s for s in dic_merchant['itens'] if isinstance(s, str)])


# TODOS OS MAPAS QUE OS MERCHANTS APARECEM
locals_loa = ["Loghill", "Ankumo Mountain", "Rethramis Border", "Rethramis",
              "Saland Hill", "Ozhorn Hill", 'Yudia',
              'Mount Zagoras', 'Lakebar', 'Medrick Monastery', 'Bilbrin Forest', 'Battlebound Plains', 'West Luterra',
              'Dyorika Plain', 'Sunbright Hill', 'Flowering Orchard', 'East Luterra',
              'Blackrose Chapel', 'Leyar Terrace', "Borea's Domain", 'Croconys Seashore',
              'Seaswept Woods', 'Sweetwater Forest', 'Skyreach Steppe', 'Forest of Giants', 'Tortoyk',
              'Delphi Township', 'Rattan Hill', 'Melody Forest', 'Twilight Mists', 'Prisma Valley', 'Anikka',
              'Arid Path', 'Scraplands', 'Nebelhorn', 'Windbringer Hills', 'Totrich', 'Riza Falls', 'Arthetine',
              'Port Krona', 'Parna Forest', 'Fesnar Highland', 'Vernese Forest', 'Balankar Mountains', 'North Vern',
              'Frozen Sea', 'Bitterwind Hill', 'Iceblood Plateau', 'Lake Eternity', 'Icewing Heights', 'Shushire',
              'Lake Shiverwave', 'Glass Lotus Lake', 'Breezesome Brae', 'Xeneela Ruins', "Elzowin's Shade", 'Rohendel',
              "Yorn's Cradle", 'Unfinished Garden', 'Black Anvil Mine', 'Iron Hammer Mine', 'Hall of Promise', 'Yorn',
              'Kalaja', 'Feiton',
              'Tideshelf Path', 'Starsand Beach', 'Tikatika Colony', 'Secret Forest', 'Punika',
              'Candaria Territory', 'Bellion Ruins', 'South Vern',
              'Fang River', 'The Wolflands', 'Rowen']

itens_loa = ["Surprise Chest", "Sky Reflection Oil", "Chain War Chronicles",
             "Shy Wind Flower Pollen", "Angler's Fishing Pole", "Wei",
             "Fine Gramophone", "Vern's Founding Coin", "Sirius's Holy Book",
             "Sylvain Queens' Blessing", "Fargar's Beer", "Red Moon Tears",
             "Oreha Viewing Stone", "Necromancer's Records", "Warm Earmuffs",
             "Seria", "Sian", "Madnick", "Mokamoka"]


# Usa expressões regulares para encontrar as palavras em cada string
local_matches = [re.search(word, local_str) for word in locals_loa]
itens_matches = [re.search(word, itens_str) for word in itens_loa]

# PROCURA SE O ITEM FOI ENCONTRADO NA BUSCA EM 'ITENS_MATCHES'

# ------ RETHRAMIS ------

if any(match is not None and match.group() == 'Surprise Chest' for match in itens_matches):

    # URLS DOS MAPAS DE RETHRAMIS
    log_hill_url = 'https://assets.maxroll.gg/wordpress/wandering_merchant_ben_log_hill_v2.jpg'
    ankumo_mountain_url = 'https://assets.maxroll.gg/wordpress/wandering_merchant_ben_ankumo_mountain_v2.jpg'
    rethramis_border = 'https://assets.maxroll.gg/wordpress/wandering_merchant_ben_rethramis_border_v2.jpg'


# Envia a mensagem dependendo de qual é o mapa // Rethramis
    if "Loghill" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local: </b> Rethramis / Log Hill\n"
        message += "<b>Item:</b> Surprise Chest\n"
        message += f"<b>Mapa: <a href='{log_hill_url}'>Log Hill</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif "Ankumo Mountain" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local: </b> Rethramis / Ankumo Mountain\n"
        message += "<b>Item:</b> Surprise Chest\n"
        message += f"<b>Mapa: <a href='{ankumo_mountain_url}'>Ankumo Mountain</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif "Rethramis Border" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Rethramis / Rethramis Border\n"
        message += "<b>Item:</b> Surprise Chest\n"
        message += f"<b>Mapa: <a href='{rethramis_border}'>Rethramis Border</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

# ------ YUDIA ------

if any(match is not None and match.group() == 'Sky Reflection Oil' for match in itens_matches):

    # URLS DOS MAPAS DE YUDIA
    saland_hill_url = 'https://assets.maxroll.gg/wordpress/yudia_wandering_merchant_lucas_saland_hill.jpg'
    ozhorn_hill_url = 'https://assets.maxroll.gg/wordpress/yudia_wandering_merchant_lucas_ozhorn_hill.jpg'

    if 'Saland Hill' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Yudia / Saland Hill\n"
        message += "<b>Item:</b> Sky Reflection Oil\n"
        message += f"<b>Mapa: <a href='{saland_hill_url}'>Saland Hill</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Ozhorn Hill' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Yudia / Ozhorn Hill\n"
        message += "<b>Item:</b> Sky Reflection Oil\n"
        message += f"<b>Mapa: <a href='{ozhorn_hill_url}'>Ozhorn Hill</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)


# ------ WEST LUTERRA ------


if any(match is not None and match.group() == 'Chain War Chronicles' for match in itens_matches):

    # URLS DOS MAPAS DE WEST LUTERRA
    mount_zagoras_url = 'https://assets.maxroll.gg/wordpress/malone_mount_zagoras.jpg'
    lakebar_url = 'https://assets.maxroll.gg/wordpress/malone_lakebar.jpg'
    medrick_monastery = 'https://assets.maxroll.gg/wordpress/malone_medrick_monastery.jpg'
    bilbrin_forest = 'https://assets.maxroll.gg/wordpress/malone_bilbrin_forest.jpg'
    battlebound_plains = 'https://assets.maxroll.gg/wordpress/malone_battlebound_plains.jpg'

    if 'Mount Zagoras' in local_str and 'Chain War Chronicles' not in processed_itens:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> West Luterra / Mount Zagoras\n"
        message += "<b>Item</b>: Chain War Chronicles\n"
        message += f"<b>Mapa: <a href='{mount_zagoras_url}'>Mount Zagoras</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Chain War Chronicles')

    elif 'Lakebar' in local_str and 'Chain War Chronicles' not in processed_itens:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> West Luterra / Lakebar\n"
        message += "<b>Item</b>: Chain War Chronicles\n"
        message += f"<b>Mapa: <a href='{lakebar_url}'>Lakebar</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Chain War Chronicles')

    elif 'Medrick Monastery' in local_str and 'Chain War Chronicles' not in processed_itens:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> West Luterra / Medrick Monastery\n"
        message += "<b>Item</b>: Chain War Chronicles\n"
        message += f"<b>Mapa: <a href='{medrick_monastery}'>Medrick Monastery</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Chain War Chronicles')

    elif 'Bilbrin Forest' in local_str and 'Chain War Chronicles' not in processed_itens:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> West Luterra / Bilbrin Forest\n"
        message += "<b>Item</b>: Chain War Chronicles\n"
        message += f"<b>Mapa: <a href='{bilbrin_forest}'>Bilbrin Forest</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Chain War Chronicles')

    elif 'Battlebound Plains' in local_str and 'Chain War Chronicles' not in processed_itens:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> West Luterra / Battlebound Plains\n"
        message += "<b>Item</b>: Chain War Chronicles\n"
        message += f"<b>Mapa: <a href='{battlebound_plains}'>Battlebound Plains</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Chain War Chronicles')

# ------ EAST LUTERRA (MORRIS) ------


if any(match is not None and match.group() == 'Chain War Chronicles' for match in itens_matches):

    # URLS DOS MAPAS DE EAST LUTERRA (NPC MORRIS)
    dyorika_plains = 'https://assets.maxroll.gg/wordpress/morris_dyorika_plains_10.jpg'
    sunbright_hill = 'https://assets.maxroll.gg/wordpress/morris_sunbright_hill_10.jpg'
    flowering_orchard = 'https://assets.maxroll.gg/wordpress/morris_flowering_orchard_10.jpg'

    if 'Dyorika Plain' in local_str and 'Chain War Chronicles' not in processed_itens:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> East Luterra / Dyorika Plain\n"
        message += "<b>Item</b>: Chain War Chronicles\n"
        message += f"<b>Mapa: <a href='{dyorika_plains}'>Dyorika Plain</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Chain War Chronicles')

    elif 'Sunbright Hill' in local_str and 'Chain War Chronicles' not in processed_itens:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> East Luterra / Sunbright Hill\n"
        message += "<b>Item</b>: Chain War Chronicles\n"
        message += f"<b>Mapa: <a href='{sunbright_hill}'>Sunbright Hill</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Chain War Chronicles')

    elif 'Flowering Orchard' in local_str and 'Chain War Chronicles' not in processed_itens:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> East Luterra / Flowering Orchard\n"
        message += "<b>Item</b>: Chain War Chronicles\n"
        message += f"<b>Mapa: <a href='{flowering_orchard}'>Flowering Orchard</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Chain War Chronicles')


# ------ EAST LUTERRA (BURT) ------


if any(match is not None and match.group() == 'Chain War Chronicles' for match in itens_matches):

    # URLS DOS MAPAS DE EAST LUTERRA (NPC BURT)
    blackrose_chapel = 'https://assets.maxroll.gg/wordpress/burt_blackrose_chapel_v4.jpg'
    leyar_terrace = 'https://assets.maxroll.gg/wordpress/burt_layer_terrace_v4.jpg'
    boreas_domain = 'https://assets.maxroll.gg/wordpress/burt_boreas_domain_v4.jpg'
    croconys_seashore = 'https://assets.maxroll.gg/wordpress/burt_croconys_seashore_v4.jpg'

    if 'Blackrose Chapel' in local_str and 'Chain War Chronicles' not in processed_itens:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> East Luterra / Blackrose Chapel\n"
        message += "<b>Item</b>: Chain War Chronicles\n"
        message += f"<b>Mapa: <a href='{blackrose_chapel}'>Blackrose Chapel</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Chain War Chronicles')

    elif 'Leyar Terrace' in local_str and 'Chain War Chronicles' not in processed_itens:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> East Luterra / Leyar Terrace\n"
        message += "<b>Item</b>: Chain War Chronicles\n"
        message += f"<b>Mapa: <a href='{leyar_terrace}'>Leyar Terrace</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Chain War Chronicles')

    elif "Borea's Domain" in local_str and 'Chain War Chronicles' not in processed_itens:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> East Luterra / Borea's Domain\n"
        message += "<b>Item</b>: Chain War Chronicles\n"
        message += f"<b>Mapa: <a href='{boreas_domain}'>Borea's Domain</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Chain War Chronicles')

    elif "Croconys Seashore" in local_str and 'Chain War Chronicles' not in processed_itens:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> East Luterra / Croconys Seashore\n"
        message += "<b>Item</b>: Chain War Chronicles\n"
        message += f"<b>Mapa: <a href='{croconys_seashore}'>Croconys Seashore</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Chain War Chronicles')


# ------ TORTOYK ------


if any(match is not None and match.group() == 'Shy Wind Flower Pollen' for match in itens_matches):

    # URLS DOS MAPAS DE TORTOYK
    seaswept_woods = 'https://assets.maxroll.gg/wordpress/wandering_merchant_oliver_seaswept_woods.jpg'
    sweetwater_forest = 'https://assets.maxroll.gg/wordpress/wandering_merchant_oliver_sweetwater_forest.jpg'
    skyreach_steppe = 'https://assets.maxroll.gg/wordpress/wandering_merchant_oliver_skyreach_steppe.jpg'
    forest_of_giants = 'https://assets.maxroll.gg/wordpress/wandering_merchant_oliver_forest_of_giants.jpg'

    if 'Seaswept Woods' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Tortoyk / Seaswept Woods\n"
        message += "<b>Item</b>: Shy Wind Flower Pollen\n"
        message += f"<b>Mapa: <a href='{seaswept_woods}'>Seaswept Woods</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Sweetwater Forest' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Tortoyk / Sweetwater Forest\n"
        message += "<b>Item</b>: Shy Wind Flower Pollen\n"
        message += f"<b>Mapa: <a href='{sweetwater_forest}'>Sweetwater Forest</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Skyreach Steppe' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Tortoyk / Skyreach Steppe\n"
        message += "<b>Item</b>: Shy Wind Flower Pollen\n"
        message += f"<b>Mapa: <a href='{skyreach_steppe}'>Skyreach Steppe</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Forest of Giants' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Tortoyk / Forest of Giants\n"
        message += "<b>Item</b>: Shy Wind Flower Pollen\n"
        message += f"<b>Mapa: <a href='{forest_of_giants}'>Forest of Giants</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)


# ------ ANIKKA ------

if any(match is not None and match.group() == "Angler's Fishing Pole" for match in itens_matches):

    # URLS DOS MAPAS DE ANIKKA
    delphi_township = 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_delphi_township.jpg'
    rattan_hill = 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_rattan_hill.jpg'
    melody_forest = 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_melody_forest.jpg'
    twilight_mists = 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_twilight_mists.jpg'
    prisma_valley = 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_mirror_valley.jpg'

    if 'Delphi Township' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Anikka / Delphi Township\n"
        message += "<b>Item</b>: Angler's Fishing Pole\n"
        message += f"<b>Mapa: <a href='{delphi_township}'>Delphi Township</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Rattan Hill' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Anikka / Rattan Hill\n"
        message += "<b>Item</b>: Angler's Fishing Pole\n"
        message += f"<b>Mapa: <a href='{rattan_hill}'>Rattan Hill</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Melody Forest' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Anikka / Melody Forest\n"
        message += "<b>Item</b>: Angler's Fishing Pole\n"
        message += f"<b>Mapa: <a href='{melody_forest}'>Melody Forest</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Twilight Mists' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Anikka / Twilight Mists\n"
        message += "<b>Item</b>: Angler's Fishing Pole\n"
        message += f"<b>Mapa: <a href='{twilight_mists}'>Twilight Mists</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Prisma Valley' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Anikka / Prisma Valley\n"
        message += "<b>Item</b>: Angler's Fishing Pole\n"
        message += f"<b>Mapa: <a href='{prisma_valley}'>Prisma Valley</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)


# ------ ANIKKA WEI ------

if any(match is not None and match.group() == "Wei" for match in itens_matches):

    # URLS DOS MAPAS DE ANIKKA
    delphi_township = 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_delphi_township.jpg'
    rattan_hill = 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_rattan_hill.jpg'
    melody_forest = 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_melody_forest.jpg'
    twilight_mists = 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_twilight_mists.jpg'
    prisma_valley = 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_mirror_valley.jpg'

    if 'Delphi Township' in local_str:
        message = "<b>WEI LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Anikka / Delphi Township\n"
        message += "<b>Item</b>: Wei\n"
        message += f"<b>Mapa: <a href='{delphi_township}'>Delphi Township</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Rattan Hill' in local_str:
        message = "<b>WEI LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Anikka / Rattan Hill\n"
        message += "<b>Item</b>: Wei\n"
        message += f"<b>Mapa: <a href='{rattan_hill}'>Rattan Hill</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Melody Forest' in local_str:
        message = "<b>WEI LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Anikka / Melody Forest\n"
        message += "<b>Item</b>: Wei\n"
        message += f"<b>Mapa: <a href='{melody_forest}'>Melody Forest</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Twilight Mists' in local_str:
        message = "<b>WEI LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Anikka / Twilight Mists\n"
        message += "<b>Item</b>: Wei\n"
        message += f"<b>Mapa: <a href='{twilight_mists}'>Twilight Mists</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Prisma Valley' in local_str:
        message = "<b>WEI LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Anikka / Prisma Valley\n"
        message += "<b>Item</b>: Wei\n"
        message += f"<b>Mapa: <a href='{prisma_valley}'>Prisma Valley</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

# ------ ARTHETINE ------

if any(match is not None and match.group() == "Fine Gramophone" for match in itens_matches):

    # URLS DOS MAPAS DE ANIKKA
    arid_path = 'https://assets.maxroll.gg/wordpress/wandering_merchant_nox_arid_path.jpg'
    scraplands = 'https://assets.maxroll.gg/wordpress/wandering_merchant_nox_scraplands.jpg'
    nebelhorn = 'https://assets.maxroll.gg/wordpress/wandering_merchant_nox_nebel_horn.jpg'
    windbringer_hills = 'https://assets.maxroll.gg/wordpress/wandering_merchant_nox_windbringer_hill.jpg'
    totrich = 'https://assets.maxroll.gg/wordpress/wandering_merchant_nox_tottrich.jpg'
    riza_falls = 'https://assets.maxroll.gg/wordpress/wandering_merchant_nox_riza_falls.jpg'

    if 'Arid Path' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Arthetine / Arid Path\n"
        message += "<b>Item</b>: Fine Gramophone\n"
        message += f"<b>Mapa: <a href='{arid_path}'>Arid Path</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Scraplands' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Arthetine / Scraplands\n"
        message += "<b>Item</b>: Fine Gramophone\n"
        message += f"<b>Mapa: <a href='{scraplands}'>Scraplands</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Nebelhorn' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Arthetine / Nebelhorn\n"
        message += "<b>Item</b>: Fine Gramophone\n"
        message += f"<b>Mapa: <a href='{nebelhorn}'>Nebelhorn</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Windbringer Hills' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Arthetine / Windbringer Hills\n"
        message += "<b>Item</b>: Fine Gramophone\n"
        message += f"<b>Mapa: <a href='{windbringer_hills}'>Windbringer Hills</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Totrich' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Arthetine / Totrich\n"
        message += "<b>Item</b>: Fine Gramophone\n"
        message += f"<b>Mapa: <a href='{totrich}'>Totrich</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Riza Falls' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Arthetine / Riza Falls\n"
        message += "<b>Item</b>: Fine Gramophone\n"
        message += f"<b>Mapa: <a href='{riza_falls}'>Riza Falls</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)


# ------ NORTH VERN ------

if any(match is not None and match.group() == "Vern's Founding Coin" for match in itens_matches):

    # URLS DOS MAPAS DE ANIKKA
    port_krona = 'https://assets.maxroll.gg/wordpress/wandering_merchant_peter_port_krona.jpg'
    parna_forest = 'https://assets.maxroll.gg/wordpress/wandering_merchant_peter_parna_forest.jpg'
    fesnar_highland = 'https://assets.maxroll.gg/wordpress/wandering_merchant_peter_fesnar_highland.jpg'
    vernese_forest = 'https://assets.maxroll.gg/wordpress/wandering_merchant_peter_vernese_forest.jpg'
    balankar_mountains = 'https://assets.maxroll.gg/wordpress/wandering_merchant_peter_balankar_mountains.jpg'

    if 'Port Krona' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> North Vern / Port Krona\n"
        message += "<b>Item</b>: Vern's Founding Coin\n"
        message += f"<b>Mapa: <a href='{port_krona}'>Port Krona</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Parna Forest' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> North Vern / Parna Forest\n"
        message += "<b>Item</b>: Vern's Founding Coin\n"
        message += f"<b>Mapa: <a href='{parna_forest}'>Parna Forest</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Fesnar Highland' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> North Vern / Fesnar Highland\n"
        message += "<b>Item</b>: Vern's Founding Coin\n"
        message += f"<b>Mapa: <a href='{fesnar_highland}'>Fesnar Highland</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Vernese Forest' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> North Vern / Vernese Forest\n"
        message += "<b>Item</b>: Vern's Founding Coin\n"
        message += f"<b>Mapa: <a href='{vernese_forest}'>Vernese Forest</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Balankar Mountains' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> North Vern / Balankar Mountains\n"
        message += "<b>Item</b>: Vern's Founding Coin\n"
        message += f"<b>Mapa: <a href='{balankar_mountains}'>Balankar Mountains</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)


# ------ SHUSHIRE ------

if any(match is not None and match.group() == "Sirius's Holy Book" for match in itens_matches):

    # URLS DOS MAPAS DE ANIKKA
    frozen_sea = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_frozen_sea_v2.jpg'
    bitterwind_hill = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_bitterwind_hill_v2.jpg'
    iceblood_plateau = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_ice_blood_plateau_v2.jpg'
    lake_eternity = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_lake_eternity_v2.jpg'
    icewing_heights = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_icewing_heights_v2.jpg'

    if 'Frozen Sea' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Shushire / Frozen Sea\n"
        message += "<b>Item</b>: Sirius's Holy Book\n"
        message += f"<b>Mapa: <a href='{frozen_sea}'>Frozen Sea</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Bitterwind Hill' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Shushire / Bitterwind Hill\n"
        message += "<b>Item</b>: Sirius's Holy Book\n"
        message += f"<b>Mapa: <a href='{bitterwind_hill}'>Bitterwind Hill</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Iceblood Plateau' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Shushire / Iceblood Plateau\n"
        message += "<b>Item</b>: Sirius's Holy Book\n"
        message += f"<b>Mapa: <a href='{iceblood_plateau}'>Iceblood Plateau</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Lake Eternity' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Shushire / Lake Eternity\n"
        message += "<b>Item</b>: Sirius's Holy Book\n"
        message += f"<b>Mapa: <a href='{lake_eternity}'>Lake Eternity</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Icewing Heights' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Shushire / Icewing Heights\n"
        message += "<b>Item</b>: Sirius's Holy Book\n"
        message += f"<b>Mapa: <a href='{icewing_heights}'>Icewing Heights</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)


# ------ ROHENDEL ------

if any(match is not None and match.group() == "Sylvain Queens' Blessing" for match in itens_matches):

    # URLS DOS MAPAS DE ANIKKA
    lake_shiverwave = 'https://assets.maxroll.gg/wordpress/aricer_lake_shiverwave_v4.jpg'
    glass_lotus_lake = 'https://assets.maxroll.gg/wordpress/aricer_glass_lotus_lake_v4.jpg'
    breezesome_brae = 'https://assets.maxroll.gg/wordpress/aricer_breezesome_brae_v4.jpg'
    xeneela_ruins = 'https://assets.maxroll.gg/wordpress/aricer_xeneela_ruins_v4.jpg'
    elzowins_shade = 'https://assets.maxroll.gg/wordpress/aricer_elzowins_shade_v4.jpg'

    if 'Lake Shiverwave' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Rohendel / Lake Shiverwave\n"
        message += "<b>Item</b>: Sylvain Queens' Blessing\n"
        message += f"<b>Mapa: <a href='{lake_shiverwave}'>Lake Shiverwave</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Glass Lotus Lake' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Rohendel / Glass Lotus Lake\n"
        message += "<b>Item</b>: Sylvain Queens' Blessing\n"
        message += f"<b>Mapa: <a href='{glass_lotus_lake}'>Glass Lotus Lake</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Breezesome Brae' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Rohendel / Breezesome Brae\n"
        message += "<b>Item</b>: Sylvain Queens' Blessing\n"
        message += f"<b>Mapa: <a href='{breezesome_brae}'>Breezesome Brae</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif 'Xeneela Ruins' in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Rohendel / Xeneela Ruins\n"
        message += "<b>Item</b>: Sylvain Queens' Blessing\n"
        message += f"<b>Mapa: <a href='{xeneela_ruins}'>Xeneela Ruins</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif "Elzowin's Shade" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Rohendel / Elzowin's Shade\n"
        message += "<b>Item</b>: Sylvain Queens' Blessing\n"
        message += f"<b>Mapa: <a href='{elzowins_shade}'>Elzowin's Shade</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

# ------ YORN ------

if any(match is not None and match.group() == "Fargar's Beer" for match in itens_matches):

    # URLS DOS MAPAS DE ANIKKA
    yorns_cradle = 'https://assets.maxroll.gg/wordpress/laitir_yorns_cradle_v1.jpg'
    unfinished_garden = 'https://assets.maxroll.gg/wordpress/laitir_unfinished_garden_v1.jpg'
    black_anvil_mine = 'https://assets.maxroll.gg/wordpress/laitir_black_anvil_mine_v1.jpg'
    iron_hammer_mine = 'https://assets.maxroll.gg/wordpress/laitir_iron_hammer_mine_v1.jpg'
    hall_of_promise = 'https://assets.maxroll.gg/wordpress/laitir_hall_of_promise.jpg'

    if "Yorn's Cradle" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Yorn / Yorn's Cradle\n"
        message += "<b>Item</b>: Fargar's Beer\n"
        message += f"<b>Mapa: <a href='{yorns_cradle}'>Yorn's Cradle</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif "Unfinished Garden" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Yorn / Unfinished Garden\n"
        message += "<b>Item</b>: Fargar's Beer\n"
        message += f"<b>Mapa: <a href='{unfinished_garden}'>Unfinished Garden</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif "Black Anvil Mine" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Yorn / Black Anvil Mine\n"
        message += "<b>Item</b>: Fargar's Beer\n"
        message += f"<b>Mapa: <a href='{black_anvil_mine}'>Black Anvil Mine</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif "Iron Hammer Mine" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Yorn / Iron Hammer Mine\n"
        message += "<b>Item</b>: Fargar's Beer\n"
        message += f"<b>Mapa: <a href='{iron_hammer_mine}'>Iron Hammer Mine</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif "Hall of Promise" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Yorn / Hall of Promise\n"
        message += "<b>Item</b>: Fargar's Beer\n"
        message += f"<b>Mapa: <a href='{hall_of_promise}'>Hall of Promise</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

# ------ FEITON ------

if any(match is not None and match.group() == "Red Moon Tears" for match in itens_matches):

    # URLS DOS MAPAS DE ANIKKA
    kalaja = 'https://assets.maxroll.gg/wordpress/feiton_wandering_merchant_v1.jpg'

    if "Kalaja" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Feiton / Kalaja\n"
        message += "<b>Item</b>: Red Moon Tears\n"
        message += f"<b>Mapa: <a href='{kalaja}'>Kalaja</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)


# ------ PUNIKA ------

if any(match is not None and match.group() == "Oreha Viewing Stone" for match in itens_matches):

    # URLS DOS MAPAS DE ANIKKA
    tideshelf_path = 'https://assets.maxroll.gg/wordpress/punika_wandering_merchant_1_v1.jpg'
    starsand_beach = 'https://assets.maxroll.gg/wordpress/punika_wandering_merchant_2_v1.jpg'
    tikatika_colony = 'https://assets.maxroll.gg/wordpress/punika_wandering_merchant_3_v1.jpg'
    secret_forest = 'https://assets.maxroll.gg/wordpress/punika_wandering_merchant_4_v1.jpg'

    if "Tideshelf Path" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Punika / Tideshelf Path\n"
        message += "<b>Item</b>: Oreha Viewing Stone\n"
        message += f"<b>Mapa: <a href='{tideshelf_path}'>Tideshelf Path</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif "Starsand Beach" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Punika / Starsand Beach\n"
        message += "<b>Item</b>: Oreha Viewing Stone\n"
        message += f"<b>Mapa: <a href='{starsand_beach}'>Starsand Beach</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif "Tikatika Colony" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Punika / Tikatika Colony\n"
        message += "<b>Item</b>: Oreha Viewing Stone\n"
        message += f"<b>Mapa: <a href='{tikatika_colony}'>Tikatika Colony</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif "Secret Forest" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Punika / Secret Forest\n"
        message += "<b>Item</b>: Oreha Viewing Stone\n"
        message += f"<b>Mapa: <a href='{secret_forest}'>Secret Forest</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

# ------ SOUTH VERN ------

if any(match is not None and match.group() == "Necromancer's Records" for match in itens_matches):

    # URLS DOS MAPAS DE ANIKKA
    candaria_territory = 'https://assets.maxroll.gg/wordpress/wandering_merchant_evan_candaria_estate.jpg'
    bellion_ruins = 'https://assets.maxroll.gg/wordpress/wandering_merchant_evan_bellion_ruins.jpg'

    if "Candaria Territory" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> South Vern / Candaria Territory\n"
        message += "<b>Item</b>: Necromancer's Records\n"
        message += f"<b>Mapa: <a href='{candaria_territory}'>Candaria Territory</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif "Bellion Ruins" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> South Vern / Bellion Ruins\n"
        message += "<b>Item</b>: Necromancer's Records\n"
        message += f"<b>Mapa: <a href='{bellion_ruins}'>Bellion Ruins</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

# ------ ROWEN ------

if any(match is not None and match.group() == "Warm Earmuffs" for match in itens_matches):

    # URLS DOS MAPAS DE ANIKKA
    fang_river = 'https://lostmerchants.com/images/zones/Fang%20River.jpg'
    the_wolflands = 'https://lostmerchants.com/images/zones/The%20Wolflands.jpg'

    if "Fang River" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Rowen / Fang River\n"
        message += "<b>Item</b>: Warm Earmuffs\n"
        message += f"<b>Mapa: <a href='{fang_river}'>Fang River</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

    elif "The Wolflands" in local_str:
        message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Rowen / The Wolflands\n"
        message += "<b>Item</b>: Warm Earmuffs\n"
        message += f"<b>Mapa: <a href='{the_wolflands}'>The Wolflands</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)

# ------ EAST LUTERRA (BURT) (SERIA) ------


# if any(match is not None and match.group() == 'Seria' for match in itens_matches):

#     # URLS DOS MAPAS DE EAST LUTERRA (NPC BURT)
#     blackrose_chapel = 'https://assets.maxroll.gg/wordpress/burt_blackrose_chapel_v4.jpg'
#     leyar_terrace = 'https://assets.maxroll.gg/wordpress/burt_layer_terrace_v4.jpg'
#     boreas_domain = 'https://assets.maxroll.gg/wordpress/burt_boreas_domain_v4.jpg'
#     croconys_seashore = 'https://assets.maxroll.gg/wordpress/burt_croconys_seashore_v4.jpg'

#     if 'Blackrose Chapel' in local_str and 'Seria' not in processed_itens:
#         message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
#         message += "<b>Set de cartas:</b> Lost Wind Clif\n\n"
#         message += f"<b>Servidor:</b> {servidor}\n"
#         message += "<b>Local:</b> East Luterra / Blackrose Chapel\n"
#         message += "<b>Item</b>: Seria\n"
#         message += f"<b>Mapa: <a href='{blackrose_chapel}'>Blackrose Chapel</a></b>\n\n"
#         message += f"<b>O NPC irá embora em: {final_t}</b>"
#         # Envia a mensagem
#         send_message(message)
#         processed_itens.add('Seria')

#     elif 'Leyar Terrace' in local_str and 'Seria' not in processed_itens:
#         message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
#         message += "<b>Set de cartas:</b> Lost Wind Clif\n\n"
#         message += f"<b>Servidor:</b> {servidor}\n"
#         message += "<b>Local:</b> East Luterra / Leyar Terrace\n"
#         message += "<b>Item</b>: Seria\n"
#         message += f"<b>Mapa: <a href='{leyar_terrace}'>Leyar Terrace</a></b>\n\n"
#         message += f"<b>O NPC irá embora em: {final_t}</b>"
#         # Envia a mensagem
#         send_message(message)
#         processed_itens.add('Seria')

#     elif "Borea's Domain" in local_str and 'Seria' not in processed_itens:
#         message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
#         message += "<b>Set de cartas:</b> Lost Wind Clif\n\n"
#         message += f"<b>Servidor:</b> {servidor}\n"
#         message += "<b>Local:</b> East Luterra / Borea's Domain\n"
#         message += "<b>Item</b>: Seria\n"
#         message += f"<b>Mapa: <a href='{boreas_domain}'>Borea's Domain</a></b>\n\n"
#         message += f"<b>O NPC irá embora em: {final_t}</b>"
#         # Envia a mensagem
#         send_message(message)
#         processed_itens.add('Seria')

#     elif "Croconys Seashore" in local_str and 'Seria' not in processed_itens:
#         message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
#         message += "<b>Set de cartas:</b> Lost Wind Clif\n\n"
#         message += f"<b>Servidor:</b> {servidor}\n"
#         message += "<b>Local:</b> East Luterra / Croconys Seashore\n"
#         message += "<b>Item</b>: Seria\n"
#         message += f"<b>Mapa: <a href='{croconys_seashore}'>Croconys Seashore</a></b>\n\n"
#         message += f"<b>O NPC irá embora em: {final_t}</b>"
#         # Envia a mensagem
#         send_message(message)
#         processed_itens.add('Seria')

# # ------ SHUSHIRE (SIAN)  ------

# if any(match is not None and match.group() == "Sian" for match in itens_matches):

#     # URLS DOS MAPAS DE ANIKKA
#     frozen_sea = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_frozen_sea_v2.jpg'
#     bitterwind_hill = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_bitterwind_hill_v2.jpg'
#     iceblood_plateau = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_ice_blood_plateau_v2.jpg'
#     lake_eternity = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_lake_eternity_v2.jpg'
#     icewing_heights = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_icewing_heights_v2.jpg'

#     if 'Frozen Sea' in local_str:
#         message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
#         message += "<b>Set de cartas:</b> We'll meet again\n\n"
#         message += "<b>Local:</b> Shushire / Frozen Sea\n"
#         message += f"<b>Servidor:</b> {servidor}\n"
#         message += "<b>Item</b>: Sian\n"
#         message += f"<b>Mapa: <a href='{frozen_sea}'>Frozen Sea</a></b>\n\n"
#         message += f"<b>O NPC irá embora em: {final_t}</b>"
#         # Envia a mensagem
#         send_message(message)
#         processed_itens.add('Sian')

#     elif 'Bitterwind Hill' in local_str:
#         message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
#         message += "<b>Set de cartas:</b> We'll meet again\n\n"
#         message += f"<b>Servidor:</b> {servidor}\n"
#         message += "<b>Local:</b> Shushire / Bitterwind Hill\n"
#         message += "<b>Item</b>: Sian\n"
#         message += f"<b>Mapa: <a href='{bitterwind_hill}'>Bitterwind Hill</a></b>\n\n"
#         message += f"<b>O NPC irá embora em: {final_t}</b>"
#         # Envia a mensagem
#         send_message(message)
#         processed_itens.add('Sian')

#     elif 'Iceblood Plateau' in local_str:
#         message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
#         message += "<b>Set de cartas:</b> We'll meet again\n\n"
#         message += f"<b>Servidor:</b> {servidor}\n"
#         message += "<b>Local:</b> Shushire / Iceblood Plateau\n"
#         message += "<b>Item</b>: Sian\n"
#         message += f"<b>Mapa: <a href='{iceblood_plateau}'>Iceblood Plateau</a></b>\n\n"
#         message += f"<b>O NPC irá embora em: {final_t}</b>"
#         # Envia a mensagem
#         send_message(message)
#         processed_itens.add('Sian')

#     elif 'Lake Eternity' in local_str:
#         message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
#         message += "<b>Set de cartas:</b> We'll meet again\n\n"
#         message += f"<b>Servidor:</b> {servidor}\n"
#         message += "<b>Local:</b> Shushire / Lake Eternity\n"
#         message += "<b>Item</b>: Sian\n"
#         message += f"<b>Mapa: <a href='{lake_eternity}'>Lake Eternity</a></b>\n\n"
#         message += f"<b>O NPC irá embora em: {final_t}</b>"
#         # Envia a mensagem
#         send_message(message)
#         processed_itens.add('Sian')

#     elif 'Icewing Heights' in local_str:
#         message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
#         message += "<b>Set de cartas:</b> We'll meet again\n\n"
#         message += f"<b>Servidor:</b> {servidor}\n"
#         message += "<b>Local:</b> Shushire / Icewing Heights\n"
#         message += "<b>Item</b>: Sian\n"
#         message += f"<b>Mapa: <a href='{icewing_heights}'>Icewing Heights</a></b>\n\n"
#         message += f"<b>O NPC irá embora em: {final_t}</b>"
#         # Envia a mensagem
#         send_message(message)
#         processed_itens.add('Sian')

# ------ SHUSHIRE (MADNICK)  ------

if any(match is not None and match.group() == "Madnick" for match in itens_matches):

    # URLS DOS MAPAS DE ANIKKA
    frozen_sea = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_frozen_sea_v2.jpg'
    bitterwind_hill = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_bitterwind_hill_v2.jpg'
    iceblood_plateau = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_ice_blood_plateau_v2.jpg'
    lake_eternity = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_lake_eternity_v2.jpg'
    icewing_heights = 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_icewing_heights_v2.jpg'

    if 'Frozen Sea' in local_str:
        message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
        message += "<b>Set de cartas:</b> We'll meet again\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Shushire / Frozen Sea\n"
        message += "<b>Item</b>: Madnick\n"
        message += f"<b>Mapa: <a href='{frozen_sea}'>Frozen Sea</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Madnick')

    elif 'Bitterwind Hill' in local_str:
        message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
        message += "<b>Set de cartas:</b> We'll meet again\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Shushire / Bitterwind Hill\n"
        message += "<b>Item</b>: Madnick\n"
        message += f"<b>Mapa: <a href='{bitterwind_hill}'>Bitterwind Hill</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Madnick')

    elif 'Iceblood Plateau' in local_str:
        message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
        message += "<b>Set de cartas:</b> We'll meet again\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Shushire / Iceblood Plateau\n"
        message += "<b>Item</b>: Madnick\n"
        message += f"<b>Mapa: <a href='{iceblood_plateau}'>Iceblood Plateau</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Madnick')

    elif 'Lake Eternity' in local_str:
        message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
        message += "<b>Set de cartas:</b> We'll meet again\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Shushire / Lake Eternity\n"
        message += "<b>Item</b>: Madnick\n"
        message += f"<b>Mapa: <a href='{lake_eternity}'>Lake Eternity</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Madnick')

    elif 'Icewing Heights' in local_str:
        message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
        message += "<b>Set de cartas:</b> We'll meet again\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Shushire / Icewing Heights\n"
        message += "<b>Item</b>: Madnick\n"
        message += f"<b>Mapa: <a href='{icewing_heights}'>Icewing Heights</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Madnick')

# ------ TORTOYK (MOKAMOKA) ------


if any(match is not None and match.group() == 'Mokamoka' for match in itens_matches):

    # URLS DOS MAPAS DE TORTOYK
    seaswept_woods = 'https://assets.maxroll.gg/wordpress/wandering_merchant_oliver_seaswept_woods.jpg'
    sweetwater_forest = 'https://assets.maxroll.gg/wordpress/wandering_merchant_oliver_sweetwater_forest.jpg'
    skyreach_steppe = 'https://assets.maxroll.gg/wordpress/wandering_merchant_oliver_skyreach_steppe.jpg'
    forest_of_giants = 'https://assets.maxroll.gg/wordpress/wandering_merchant_oliver_forest_of_giants.jpg'

    if 'Seaswept Woods' in local_str:
        message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
        message += "<b>Set de cartas:</b> Forest of giants\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Tortoyk / Seaswept Woods\n"
        message += "<b>Item</b>: Mokamoka\n"
        message += f"<b>Mapa: <a href='{seaswept_woods}'>Seaswept Woods</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Mokamoka')

    elif 'Sweetwater Forest' in local_str:
        message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
        message += "<b>Set de cartas:</b> Forest of giants\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Tortoyk / Sweetwater Forest\n"
        message += "<b>Item</b>: Mokamoka\n"
        message += f"<b>Mapa: <a href='{sweetwater_forest}'>Sweetwater Forest</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Mokamoka')

    elif 'Skyreach Steppe' in local_str:
        message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
        message += "<b>Set de cartas:</b> Forest of giants\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Tortoyk / Skyreach Steppe\n"
        message += "<b>Item</b>: Mokamoka\n"
        message += f"<b>Mapa: <a href='{skyreach_steppe}'>Skyreach Steppe</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Mokamoka')

    elif 'Forest of Giants' in local_str:
        message = "<b>ITEM IMPORTANTE ENCONTRADO!</b>\n\n"
        message += "<b>Set de cartas:</b> Forest of giants\n\n"
        message += f"<b>Servidor:</b> {servidor}\n"
        message += "<b>Local:</b> Tortoyk / Forest of Giants\n"
        message += "<b>Item</b>: Mokamoka\n"
        message += f"<b>Mapa: <a href='{forest_of_giants}'>Forest of Giants</a></b>\n\n"
        message += f"<b>O NPC irá embora em: {final_t}</b>"
        # Envia a mensagem
        send_message(message)
        processed_itens.add('Mokamoka')


now = datetime.datetime.now()
dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

print(
    f'Busca concluida com sucesso / {servidor} / {dt_string}')
driver.quit()
