# BF4_Visualization
This project is meant to be a custom data representation / analysis of my past Battlefield 4 games. It uses python with the selenium library to scrape data from my previous games on battlelog. 

**slurp.py** 
- scrapes battlelog and stores data into custom classes (player_class.py & game_class.py)
- the output of the script is saved as game_data.obj using the pickle library

**pickle_extractinator.py**
- loads in game_data.obj and parses the data from the custom classes into a json file (game_data.json and win_loss.json)
