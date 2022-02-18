'''A Python web scaper that collects data from past Battlefied 4 games played
   By - Ethan Timothy'''

from asyncio.windows_events import NULL
from xml.dom import DOMException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle

#Import Classes
from player_class import Player_class
from game_class import Game_class

PATH = "C:\Program Files\chromedriver.exe" #Path to where you have chromedriver installed
URL = "https://battlelog.battlefield.com/bf4/soldier/Herpnurp/battlereports/1404882581/pc/"
URL2 = "https://battlelog.battlefield.com/bf4/battlereport/show/1/1487336408436195008/1404882581/"

driver = webdriver.Chrome(PATH)
driver.get(URL)
player_id = 1404882581

class Crawler:
    def __init__(self, player_id, game_count):
        self.player_id = player_id
        self.game_count = game_count
        self.game_list = []
        self.game_links = []
        self.scores = []
        self.game_objs = []

    def run_crawler(self):
        self.load_games()
        self.mk_link_list()
        self.get_scores()

    #Function to load the desired amount of games to the web page and build list of games (WebElements)
    def load_games(self):

        #Waits until page is loaded
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "load-more-reports")))

        try:

            try:

                #Loads the desired amount of games passed in at Crawler instantiation
                while len(self.game_list) < self.game_count:
                    time.sleep(1)
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "load-more-reports")))
                    element.click()
                    self.game_list = driver.find_elements_by_tag_name('tr')
            
            #If the website bugs out and won't load more the page will refresh and try again
            except:
                driver.refresh()
                self.load_games()

        except:

            #Once all games have been loaded all games are loaded into self.game_list and printed to console
            self.game_list = driver.find_elements_by_tag_name('tr')
            print("Game list count: " + str(len(self.game_list)))
    
    #Transforms previously gathered elements into a URL for each gathered match 
    def mk_link_list(self):

        for i in range(len(self.game_list)):
            ID = (self.game_list[i].get_attribute('data-reportid'))
            self.game_links.append((("https://battlelog.battlefield.com/bf4/battlereport/show/1/" + str(ID) + "/" +str(player_id) + "/"), ID))
            print('[' + str(i+1) + '] ' + self.game_links[i][0])

    #Visits each match URL and extracts scoreboard data
    def get_scores(self):
        count = 0

        for i in self.game_links:
            
            #Instantiate a new Class for Game_class to store each unique game in
            current_game = Game_class()
            current_game.game_id = i[1]

            try:
                driver.get(i[0])
                count += 1

                #Give a hefty 30sec wait for the page to load since the website is often very slow
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
                test = driver.find_element_by_tag_name('h2')
                print('[' + str(count) + '] ' + test.text)

                #Test to weed out false matches (the website sometimes displays games that I did not play in)
                if test.text != None and "HERPNURP" in test.text:
                    
                    if "WON" in test.text:
                        current_game.win_loss = "WON"

                        team_data = driver.find_element_by_class_name("span6") #Finds div with my team data
                        team_data2 = driver.find_elements_by_class_name("span6")[1]
                
                        player_data = team_data.find_elements_by_tag_name("tr") #Seperates each teammate and their score
                        player_data2 = team_data2.find_elements_by_tag_name("tr")

                        p_count = 0
                        p_count2 = 0

                        #Winning Team Data Handling
                        for e in player_data:
                            current_player = Player_class()
                            string = e.text.splitlines()
                            
                            #Make sure line isnt blank and is valid player data
                            if e.text != '' and p_count != 0 and len(string) == 3:
                                kd_score = string[2].split(' ')
                                current_player.game_ID = i[1]
                                current_player.player_ID = e.get_attribute("data-personaid")
                                current_player.position = string[0]
                                current_player.name = string[1]
                                current_player.kills = kd_score[0]
                                current_player.deaths = kd_score[1]
                                current_player.score = kd_score[2]

                                current_game.winners.append(current_player)

                            p_count += 1

                        #Losing Team Data Handling
                        for e in player_data2:
                            current_player = Player_class()
                            string = e.text.splitlines()
                            
                            #Make sure line isnt blank and is valid player data
                            if e.text != '' and p_count != 0 and len(string) == 3:
                                kd_score = string[2].split(' ')
                                current_player.game_ID = i[1]
                                current_player.player_ID = e.get_attribute("data-personaid")
                                current_player.position = string[0]
                                current_player.name = string[1]
                                current_player.kills = kd_score[0]
                                current_player.deaths = kd_score[1]
                                current_player.score = kd_score[2]

                                current_game.losers.append(current_player)

                            p_count2 += 1

                    if "LOST" in test.text:
                        current_game.win_loss = "LOST"

                        team_data = driver.find_element_by_class_name("span6") #Finds div with my team data
                        team_data2 = driver.find_elements_by_class_name("span6")[1]
                
                        player_data = team_data.find_elements_by_tag_name("tr") #Seperates each teammate and their score
                        player_data2 = team_data2.find_elements_by_tag_name("tr")

                        p_count = 0
                        p_count2 = 0

                        #Losing Team Data Handling
                        for e in player_data:
                            current_player = Player_class()
                            string = e.text.splitlines()
                            
                            #Make sure line isnt blank and is valid player data
                            if e.text != '' and p_count != 0 and len(string) == 3:
                                kd_score = string[2].split(' ')
                                current_player.game_ID = i[1]
                                current_player.player_ID = e.get_attribute("data-personaid")
                                current_player.position = string[0]
                                current_player.name = string[1]
                                current_player.kills = kd_score[0]
                                current_player.deaths = kd_score[1]
                                current_player.score = kd_score[2]

                                current_game.losers.append(current_player)

                            p_count += 1

                        #Winning Team Data Handling
                        for e in player_data2:
                            current_player = Player_class()
                            string = e.text.splitlines()

                            #Make sure line isnt blank and is valid player data
                            if e.text != '' and p_count != 0 and len(string) == 3:
                                kd_score = string[2].split(' ')
                                current_player.game_ID = i[1]
                                current_player.player_ID = e.get_attribute("data-personaid")
                                current_player.position = string[0]
                                current_player.name = string[1]
                                current_player.kills = kd_score[0]
                                current_player.deaths = kd_score[1]
                                current_player.score = kd_score[2]

                                current_game.winners.append(current_player)

                            p_count2 += 1
                    
                    #Adds game to Crawlers game_objs list
                    self.game_objs.append(current_game)
                            
                else:
                    print("Not A Valid Game...Skipping...")

            #Often this error gets when page initially loads
            except (DOMException):
                print("DOMException Thrown...Refreshing Page...")
                driver.refresh()
            
            #If not DOMException then this will still refresh the page
            except:
                driver.refresh()

#Intantiate the class. The second parameter is amount of games to be scraped
bot = Crawler(player_id, 1000)
bot.run_crawler()

#After all the games have been scraped the game class objects are pickled into an object file
file = open("game_data.obj", "wb")
pickle.dump(bot.game_objs, file)
