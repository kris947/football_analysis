import pandas as pd
import numpy as np
import json
from pprint import pprint

def get_list_from_Table(key,dict):
    temp_list=[]
    for player in dict:
        try:
            for row in player[key]:
                row['player_id'] = player['player_id']
                temp_list.append(row)
        except KeyError:
            continue
    return temp_list

playerdict = json.load(open('2017_all_player_A.txt'))

Player_Information=pd.DataFrame()
Fantasy=pd.DataFrame()
Player_Information_Pool=pd.DataFrame(playerdict)
Player_Information = Player_Information_Pool[['player_id', 'name','nick_name','full_name','position','height','weight','team','birth_date','birth_place','university','weighted_career_AV', 'draft_team', 'draft_class','salary','picture_URL']]

receiving_and_rushing=receiving_and_rushing_playoffs=returns=scoring=scoring_playoffs=defense=rushing_and_receiving=rushing_and_receiving_playoffs=kicking=passing=passing_playoffs=pd.DataFrame()


Fantasy=pd.DataFrame(get_list_from_Table('fantasy',playerdict))
receiving_and_rushing=pd.DataFrame(get_list_from_Table('receiving_and_rushing',playerdict))
receiving_and_rushing_playoffs=pd.DataFrame(get_list_from_Table('receiving_and_rushing_playoffs',playerdict))
returns=pd.DataFrame(get_list_from_Table('returns',playerdict))
scoring_playoffs=pd.DataFrame(get_list_from_Table('scoring_playoffs',playerdict))
scoring=pd.DataFrame(get_list_from_Table('scoring',playerdict))
defense=pd.DataFrame(get_list_from_Table('defense',playerdict))
rushing_and_receiving=pd.DataFrame(get_list_from_Table('rushing_and_receiving',playerdict))
rushing_and_receiving_playoffs=pd.DataFrame(get_list_from_Table('rushing_and_receiving_playoffs',playerdict))
kicking=pd.DataFrame(get_list_from_Table('kicking',playerdict))
passing=pd.DataFrame(get_list_from_Table('passing',playerdict))
passing_playoffs=pd.DataFrame(get_list_from_Table('passing_playoffs',playerdict))
print(passing_playoffs)


#Fantasy=Player_Information
#pprint(Player_Information)
##pprint(playerdict)

