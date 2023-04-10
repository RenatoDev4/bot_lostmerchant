# Necessary libraries
import datetime
import os.path
import re
import time
from collections import defaultdict

import telebot
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


# Class to scrape the website
class WebsiteScraper:
    def __init__(self, website_url):
        self.website_url = website_url
        self.driver = None

    def configure_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.binary_location = "/usr/bin/google-chrome"
        return chrome_options

    def scrape_website(self):
        self.launch_driver()
        self.navigate_to_website()
        self.select_server_region()
        self.select_server()
        html_content = self.get_html_content()
        time.sleep(3)
        self.close_driver()
        return html_content

    def launch_driver(self):
        chrome_options = self.configure_chrome_options()
        self.driver = webdriver.Chrome(options=chrome_options)

    def navigate_to_website(self):
        self.driver.get(self.website_url)  # type:ignore

    def select_server_region(self):
        dropdown_server_region = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "severRegion")))
        select1 = Select(dropdown_server_region)
        select1.select_by_visible_text("South America")

    def select_server(self):
        dropdown2 = self.driver.find_element(By.ID, "server")  # type:ignore
        select2 = Select(dropdown2)
        select2.select_by_visible_text("Kazeros")

    def get_html_content(self):
        html_content = self.driver.page_source  # type:ignore
        return html_content

    def close_driver(self):
        self.driver.close()  # type:ignore


if __name__ == "__main__":
    WEBSITE_URL = "https://lostmerchants.com/"
    scraper = WebsiteScraper(WEBSITE_URL)
    html_content = scraper.scrape_website()

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

    # Begin the scraping process

    soup = BeautifulSoup(html_content, "html.parser")
    dic_merchant = defaultdict(list)

    # Get the time remaining for the merchants
    data_tempo = soup.find_all('div', class_='merchants__content')

    for time_ in data_tempo:
        tempo = time_.find('span', class_='merchants__timer')
        if tempo is not None:
            for final_tempo in tempo:
                final_t = final_tempo.text
                final_t = final_t.replace("Expires in ", "")
                dic_merchant['tempo'].append(final_t)

    # Get the itens and the local of the merchants
    data = soup.find_all('div', class_='merchant merchant-grid__item')

    for merchant in data:
        local = merchant.find_all('div', class_='card-frame__title')
        for title in local:
            final_local = title.text
            dic_merchant['local'].append(final_local)

        itens = merchant.find_all('div', class_='stock__item')
        for w_itens in itens:
            final_itens = w_itens.text
            dic_merchant['itens'].append(final_itens)

    local_str = ' '.join(
        [s for s in dic_merchant['local'] if isinstance(s, str)])
    itens_str = ' '.join(
        [s for s in dic_merchant['itens'] if isinstance(s, str)])

# Server
server = "Kazeros / SA"


# Function to send the message to the telegram group

def send_message(message):
    apiToken = '5805754523: AAFIthNp4MtRuN3bbzpyD2gYqFOCFHxQDWg'
    chatID = '-1001538174798'
    bot = telebot.TeleBot(apiToken)

    # Define the path to the file where the sent messages will be saved
    file_path = os.path.join(
        '/home', 'Projetos_Python', 'bot_lostmerchants', 'sent_messages_kazeros.txt')  # noqa

    try:
        # Verify if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                sent_messages = f.read().splitlines()
        else:
            sent_messages = []

        # Verify if the message was already sent
        if message not in sent_messages:
            # Envie a mensagem
            bot.send_message(chat_id=chatID, text=message, parse_mode='HTML')

            # If the message was sent, save it in the file
            with open(file_path, 'a') as f:
                f.write(message + '\n')
        else:
            print('Mensagem já enviada anteriormente:', message)

    except Exception as e:
        print('Erro ao enviar a mensagem:', e)


# All the maps where the merchants can be found
locals_loa = ["Loghill", "Ankumo Mountain", "Rethramis Border", "Rethramis",
              "Saland Hill", "Ozhorn Hill", 'Yudia',
              'Mount Zagoras', 'Lakebar', 'Medrick Monastery', 'Bilbrin Forest', 'Battlebound Plains', 'West Luterra',  # noqa
              'Dyorika Plain', 'Sunbright Hill', 'Flowering Orchard', 'East Luterra',  # noqa
              'Blackrose Chapel', 'Leyar Terrace', "Borea's Domain", 'Croconys Seashore',  # noqa
              'Seaswept Woods', 'Sweetwater Forest', 'Skyreach Steppe', 'Forest of Giants', 'Tortoyk',  # noqa
              'Delphi Township', 'Rattan Hill', 'Melody Forest', 'Twilight Mists', 'Prisma Valley', 'Anikka',  # noqa
              'Arid Path', 'Scraplands', 'Nebelhorn', 'Windbringer Hills', 'Totrich', 'Riza Falls', 'Arthetine',  # noqa
              'Port Krona', 'Parna Forest', 'Fesnar Highland', 'Vernese Forest', 'Balankar Mountains', 'North Vern',  # noqa
              'Frozen Sea', 'Bitterwind Hill', 'Iceblood Plateau', 'Lake Eternity', 'Icewing Heights', 'Shushire',  # noqa
              'Lake Shiverwave', 'Glass Lotus Lake', 'Breezesome Brae', 'Xeneela Ruins', "Elzowin's Shade", 'Rohendel',  # noqa
              "Yorn's Cradle", 'Unfinished Garden', 'Black Anvil Mine', 'Iron Hammer Mine', 'Hall of Promise', 'Yorn',  # noqa
              'Kalaja', 'Feiton',
              'Tideshelf Path', 'Starsand Beach', 'Tikatika Colony', 'Secret Forest', 'Punika',  # noqa
              'Candaria Territory', 'Bellion Ruins', 'South Vern',
              'Fang River', 'The Wolflands', 'Rowen']

# All the itens that can be found in the merchants

itens_loa = ["Surprise Chest", "Sky Reflection Oil", "Chain War Chronicles",
             "Shy Wind Flower Pollen", "Angler's Fishing Pole", "Wei",
             "Fine Gramophone", "Vern's Founding Coin", "Sirius's Holy Book",
             "Sylvain Queens' Blessing", "Fargar's Beer", "Red Moon Tears",
             "Oreha Viewing Stone", "Necromancer's Records", "Warm Earmuffs",
             "Seria", "Sian", "Madnick", "Mokamoka"]


# Use regex to find the matches
local_matches = [re.search(word, local_str)  # type:ignore
                 for word in locals_loa if word in local_str]  # type:ignore
itens_matches = [re.search(word, itens_str)  # type:ignore
                 for word in itens_loa if word in itens_str]  # type:ignore


# Define a function to create the message string for a legendary report
def create_legendary_message(server, location, item_name, map_url, final_t):
    location_map = location.split()[1]
    message = "<b>RAPPORT LENDARIO ENCONTRADO!</b>\n\n"
    message += f"<b>Servidor</b> {server}\n"
    message += f"<b>Local:</b> {location}\n"
    message += f"<b>Item:</b> {item_name}\n"
    message += f"<b>Mapa: <a href='{map_url}'>{location_map}</a></b>\n\n"
    message += f"<b>O NPC irá embora em: {final_t}</b>"
    return message


# Define a data structure to store information about each legendary item and its associated map(s) # noqa
rapport_and_locations = [
    {'item_name': 'Surprise Chest',
     'locations': [
         {'location': 'Rethramis / Log Hill',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_ben_log_hill_v2.jpg'},  # noqa
         {'location': 'Rethramis / Ankumo Mountain',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_ben_ankumo_mountain_v2.jpg'},  # noqa
         {'location': 'Rethramis / Rethramis Border',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_ben_rethramis_border_v2.jpg'}  # noqa
     ]},

    {'item_name': 'Sky Reflection Oil',
     'locations': [
         {'location': 'Yudia / Saland Hill',
          'map_url': 'https://assets.maxroll.gg/wordpress/yudia_wandering_merchant_lucas_saland_hill.jpg'},  # noqa
         {'location': 'Yudia / Ozhorn Hill',
          'map_url': 'https://assets.maxroll.gg/wordpress/yudia_wandering_merchant_lucas_ozhorn_hill.jpg'}  # noqa
     ]},

    {'item_name': 'Chain War Chronicles',
     'locations': [
         {'location': 'West Luterra / Mount Zagoras',
          'map_url': 'https://assets.maxroll.gg/wordpress/yudia_wandering_merchant_lucas_saland_hill.jpg'},  # noqa
         {'location': 'West Luterra / Lakebar',
          'map_url': 'https://assets.maxroll.gg/wordpress/yudia_wandering_merchant_lucas_ozhorn_hill.jpg'},  # noqa
         {'location': 'West Luterra / Medrick Monastery',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_ben_medrick_monastery_v2.jpg'},  # noqa
         {'location': 'West Luterra / Bilbrin Forest',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_ben_bilbrin_forest_v2.jpg'},  # noqa
         {'location': 'West Luterra / Battlebound Plains',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_ben_battlebound_plains_v2.jpg'},  # noqa
         {'location': 'East Luterra / Dyorika Plain',
          'map_url': 'https://assets.maxroll.gg/wordpress/morris_dyorika_plains_10.jpg'},  # noqa
         {'location': 'East Luterra / Sunbright Hill',
          'map_url': 'https://assets.maxroll.gg/wordpress/morris_sunbright_hill_10.jpg'},  # noqa
         {'location': 'East Luterra / Flowering Orchard',
          'map_url': 'https://assets.maxroll.gg/wordpress/morris_flowering_orchard_10.jpg'},  # noqa
         {'location': 'East Luterra / Blackrose Chapel',
          'map_url': 'https://assets.maxroll.gg/wordpress/burt_blackrose_chapel_v4.jpg'},  # noqa
         {'location': 'East Luterra / Leyar Terrace',
          'map_url': 'https://assets.maxroll.gg/wordpress/burt_layer_terrace_v4.jpg'},  # noqa
         {'location': "East Luterra / Borea's Domain",
          'map_url': 'https://assets.maxroll.gg/wordpress/burt_boreas_domain_v4.jpg'},  # noqa
         {'location': "East Luterra / Croconys Seashore",
          'map_url': 'https://assets.maxroll.gg/wordpress/burt_croconys_seashore_v4.jpg'}  # noqa
     ]},

    {'item_name': 'Shy Wind Flower Pollen' or 'Mokamoka',
     'locations': [
         {'location': 'Tortoyk / Seaswept Woods',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_oliver_seaswept_woods.jpg'},  # noqa
         {'location': 'Tortoyk / Sweetwater Forest',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_oliver_sweetwater_forest.jpg'},  # noqa
         {'location': 'Tortoyk / Skyreach Steppe',
          'map_url': 'https: // assets.maxroll.gg/wordpress/wandering_merchant_oliver_skyreach_steppe.jpg'},  # noqa
         {'location': 'Tortoyk / Forest of Giants',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_oliver_forest_of_giants.jpg'}  # noqa
     ]},

    {'item_name': "Angler's Fishing Pole",
     'locations': [
         {'location': 'Anikka / Delphi Township',
          'map_url': 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_delphi_township.jpg'},  # noqa
         {'location': 'Anikka / Rattan Hill',
          'map_url': 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_rattan_hill.jpg'},  # noqa
         {'location': 'Anikka / Melody Forest',
          'map_url': 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_melody_forest.jpg'},  # noqa
         {'location': 'Anikka / Twilight Mists',
          'map_url': 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_twilight_mists.jpg'},  # noqa
         {'location': 'Anikka / Prisma Valley',
          'map_url': 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_mirror_valley.jpg'}  # noqa
     ]},

    {'item_name': "Wei",
     'locations': [
         {'location': 'Anikka / Delphi Township',
          'map_url': 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_delphi_township.jpg'},  # noqa
         {'location': 'Anikka / Rattan Hill',
          'map_url': 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_rattan_hill.jpg'},  # noqa
         {'location': 'Anikka / Melody Forest',
          'map_url': 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_melody_forest.jpg'},  # noqa
         {'location': 'Anikka / Twilight Mists',
          'map_url': 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_twilight_mists.jpg'},  # noqa
         {'location': 'Anikka / Prisma Valley',
          'map_url': 'https://assets.maxroll.gg/wordpress/traveling_merchant_mac_mirror_valley.jpg'}  # noqa
     ]},

    {'item_name': "Fine Gramophone",
     'locations': [
         {'location': 'Arthetine / Arid Path',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_nox_arid_path.jpg'},  # noqa
         {'location': 'Arthetine / Scraplands',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_nox_scraplands.jpg'},  # noqa
         {'location': 'Arthetine / Nebelhorn',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_nox_nebel_horn.jpg'},  # noqa
         {'location': 'Arthetine / Windbringer Hills',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_nox_windbringer_hill.jpg'},  # noqa
         {'location': 'Arthetine / Totrich',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_nox_tottrich.jpg'},  # noqa
         {'location': 'Arthetine / Riza Falls',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_nox_riza_falls.jpg'}  # noqa
     ]},

    {'item_name': "Vern's Founding Coin",
     'locations': [
         {'location': 'North Vern / Port Krona',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_peter_port_krona.jpg'},  # noqa
         {'location': 'North Vern / Parna Forest',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_peter_parna_forest.jpg'},  # noqa
         {'location': 'North Vern / Fesnar Highland',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_peter_fesnar_highland.jpg'},  # noqa
         {'location': 'North Vern / Vernese Forest',
          'map_url': 'https: // assets.maxroll.gg/wordpress/wandering_merchant_peter_vernese_forest.jpg'},  # noqa
         {'location': 'North Vern / Balankar Mountains',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_peter_balankar_mountains.jpg'}  # noqa
     ]},

    {'item_name': "Sirius's Holy Book" or 'Madnick',
     'locations': [
         {'location': 'Shushire / Frozen Sea',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_frozen_sea_v2.jpg'},  # noqa
         {'location': 'Shushire / Bitterwind Hill',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_bitterwind_hill_v2.jpg'},  # noqa
         {'location': 'Shushire / Iceblood Plateau',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_ice_blood_plateau_v2.jpg'},  # noqa
         {'location': 'Shushire / Lake Eternity',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_lake_eternity_v2.jpg'},  # noqa
         {'location': 'Shushire / Icewing Heights',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_jeffrey_icewing_heights_v2.jpg'}  # noqa
     ]},

    {'item_name': "Sylvain Queens' Blessing",
     'locations': [
         {'location': 'Rohendel / Lake Shiverwave',
          'map_url': 'https://assets.maxroll.gg/wordpress/aricer_lake_shiverwave_v4.jpg'},  # noqa
         {'location': 'Rohendel / Glass Lotus Lake',
          'map_url': 'https://assets.maxroll.gg/wordpress/aricer_glass_lotus_lake_v4.jpg'},  # noqa
         {'location': 'Rohendel / Breezesome Brae',
          'map_url': 'https://assets.maxroll.gg/wordpress/aricer_breezesome_brae_v4.jpg'},  # noqa
         {'location': 'Rohendel / Xeneela Ruins',
          'map_url': 'https://assets.maxroll.gg/wordpress/aricer_xeneela_ruins_v4.jpg'},  # noqa
         {'location': "Rohendel / Elzowin's Shade",
          'map_url': 'https://assets.maxroll.gg/wordpress/aricer_elzowins_shade_v4.jpg'}  # noqa
     ]},

    {'item_name': "Fargar's Beer",
     'locations': [
         {'location': "Yorn / Yorn's Cradle",
          'map_url': 'https://assets.maxroll.gg/wordpress/aricer_lake_shiverwave_v4.jpg'},  # noqa
         {'location': 'Yorn / Unfinished Garden',
          'map_url': 'https://assets.maxroll.gg/wordpress/aricer_glass_lotus_lake_v4.jpg'},  # noqa
         {'location': 'Yorn / Black Anvil Mine',
          'map_url': 'https://assets.maxroll.gg/wordpress/aricer_breezesome_brae_v4.jpg'},  # noqa
         {'location': 'Yorn / Iron Hammer Mine',
          'map_url': 'https://assets.maxroll.gg/wordpress/aricer_xeneela_ruins_v4.jpg'},  # noqa
         {'location': "Yorn / Hall of Promise",
          'map_url': 'https://assets.maxroll.gg/wordpress/aricer_elzowins_shade_v4.jpg'}  # noqa
     ]},


    {'item_name': "Red Moon Tears",
     'locations': [
         {'location': "Feiton / Kalaja",
          'map_url': 'https://assets.maxroll.gg/wordpress/feiton_wandering_merchant_v1.jpg'}  # noqa
     ]},

    {'item_name': "Oreha Viewing Stone",
     'locations': [
         {'location': "Punika / Tideshelf Path",
          'map_url': 'https://assets.maxroll.gg/wordpress/punika_wandering_merchant_1_v1.jpg'},  # noqa
         {'location': 'Punika / Starsand Beach',
          'map_url': 'https://assets.maxroll.gg/wordpress/punika_wandering_merchant_2_v1.jpg'},  # noqa
         {'location': 'Punika / Tikatika Colony',
          'map_url': 'https://assets.maxroll.gg/wordpress/punika_wandering_merchant_3_v1.jpg'},  # noqa
         {'location': 'Punika / Secret Forest',
          'map_url': 'https://assets.maxroll.gg/wordpress/punika_wandering_merchant_4_v1.jpg'}  # noqa
     ]},

    {'item_name': "Necromancer's Records",
     'locations': [
         {'location': "South Vern / Candaria Territory",
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_evan_candaria_estate.jpg'},  # noqa
         {'location': 'South Vern / Bellion Ruins',
          'map_url': 'https://assets.maxroll.gg/wordpress/wandering_merchant_evan_bellion_ruins.jpg'}  # noqa
     ]},

    {'item_name': "Warm Earmuffs",
     'locations': [
         {'location': "Rowen / Fang River",
          'map_url': 'https://lostmerchants.com/images/zones/Fang%20River.jpg'},  # noqa
         {'location': 'Rowen / The Wolflands',
          'map_url': 'https://lostmerchants.com/images/zones/The%20Wolflands.jpg'}  # noqa
     ]},


]

# Find rapport item and location, if find both, send message to telegram group # noqa
for item_dict in rapport_and_locations:
    item = item_dict['item_name']  # type:ignore
    locations = item_dict['locations']  # type:ignore
    if any(match is not None and match.group() == item for match in itens_matches):  # type:ignore # noqa
        for loc in locations:
            if loc['location'] in local_str:  # type:ignore
                message = create_legendary_message(
                    server, loc['location'], item, loc['map_url'], final_t)  # type:ignore # noqa
                send_message(message)
                break  # Stop searching for this item if it was already found and reported # noqa


# Print message to console to check if everything is working
now = datetime.datetime.now()
dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
print(f'Busca concluida com sucesso / {server} / {dt_string}')
