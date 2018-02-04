import urllib3
import urllib
import re
import requests
import pprint
import threading
import lxml
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MYLink= 'https://www.pro-football-reference.com'


#Open the specific link without comments
def open_link(link):
    comm = re.compile('<!--|-->')
    request = urllib.request.urlopen(link)
    soup = BeautifulSoup(comm.sub('', request.read().decode('utf-8')), 'lxml')
    return soup

#Return the basic information about players  and tables about their stats
def get_player_basic_information(player_link):
    player_soup =open_link(player_link)
    player_infos = player_soup.find('div', {'class': 'players'})
    id=player_link[-12:-4]
    try:
        name =player_infos.find('h1', {'itemprop': 'name'}).text
    except AttributeError:
        name = ""
    try:
        nick_name = player_infos.find('span', {'itemprop': 'nickname'}).text.strip()
    except AttributeError:
        nick_name = ""
    #print(player_infos)
    try:
        full_name_list =player_infos.find('strong').text.strip().split('(')
        full_name=full_name_list[0]
    except AttributeError:
        full_name=''
    try:
        position=player_infos.find_all('p')[1].text.strip().split()[1]
    except AttributeError:
        position=''
    try:
        height=player_infos.find('span', {'itemprop': 'height'}).text.strip()
    except AttributeError:
        height=''
    try:
        weight=player_infos.find('span', {'itemprop': 'weight'}).text.strip()[:-2]
    except AttributeError:
        weight=''
    try:
        team = player_infos.find('span', {'itemprop': 'affiliation'}).text.strip()
    except AttributeError:
        team =''
    try:
        birth_date_l=player_infos.find('span', {'itemprop': 'birthDate'}).text.strip().split()
        birth_date=birth_date_l[0]+' '+birth_date_l[1][:-1]+' '+birth_date_l[2]
        birth_place = ''
        birth_place_L=player_infos.find('span', {'itemprop': 'birthPlace'}).text.strip().split()[1:][:-1]
        for tag in birth_place_L:
            birth_place=birth_place+" "+tag
        birth_place =birth_place[:-1]
    except AttributeError:
        birth_date=''
        birth_place=''
    try:
        university=player_infos.find('a',href = re.compile(r'/schools/*')).text
    except AttributeError:
        university=''

    #to fix
    #weighted_carrer_AV=player_infos.find_all(p).('a',href = re.compile(r'/blog/*')).text.split()[4]
    weighted_carrer_AV=0

    #if drafted
    try:
        draft_team=player_infos.find_all('p')[8].find('a').text.strip()
        draft_class=player_infos.find_all('p')[8].find('a',href = re.compile(r'/year*')).text.strip().split()[0]
    except AttributeError:
        draft_team='Undrafted'
        draft_class=''
    try:
        salary=player_infos.find('a',href = re.compile(r'/players/salary')).text.strip()
    except AttributeError:
        salary=''
    try:
        picture_URL=player_infos.find('img',{'itemscope': 'image'})['src']
    except TypeError:
        picture_URL=''

    player_info = {'player_id':id,
                   'name':name,
                   'nick_name':nick_name,
                   'full_name':full_name,
                   'position':position,
                   'height':height,
                   'weight':weight,
                   'team':team,
                   'birth_date':birth_date,
                   'birth_place':birth_place,
                   'university':university,
                   'weighted_career_AV':weighted_carrer_AV,
                   'draft_team':draft_team,
                   'draft_class':draft_class,
                   'salary':salary,
                   'picture_URL':picture_URL}

    tables=player_soup.find_all('table',{'id':True})
    for table in tables:
        if table['id']!='sim_scores' or table['id']!='all_pro':
            player_info[table['id']]=get_Table_Information(player_link,table['id'])

    return player_info

#Return the unique id of the person
def get_players_ID_and_Name(PlayersLink):
    player_soup = open_link(PlayersLink)
    player_infos = player_soup.find('div', {'id': 'div_players'})
    href_tags=[]
    for a in player_infos.find_all('b'):
        href_tags.append(a.find('a')['href'])
    return href_tags
#Return the information from the table
def get_Table_Information(player_link,table_type):
    player_soup = open_link(player_link)
    try:
        player_infos = player_soup.find('table', {'id':table_type})
        years=player_infos.find_all('tr',{'class':'full_table'})
        year_stats=[]
        for year in years:
            keys=[]
            values=[]
            for item in year.find_all('th', attrs={'data-stat': True}):
                keys.append(item['data-stat'])
                values.append(item.text)
            for item in year.find_all('td', attrs={'data-stat': True}):
                keys.append(item['data-stat'])
                values.append(item.text)

            d = dict(zip(keys, values))
            year_stats.append(d)
        print(year_stats)
    except AttributeError:
        year_stats=[]
    return year_stats



# A:65  Z:91
all_player = []
for i in range(65,66):
    plink=[]
    linkin=[]
    PlayersLink = 'https://www.pro-football-reference.com/players'+'/'+chr(i)
    print(PlayersLink)
    plink = get_players_ID_and_Name(PlayersLink)
    for link in plink:
        print(MYLink +"/"+ link)
        all_player.append(get_player_basic_information(MYLink +"/"+ link))
    print('Letter %s Done.' % (chr(i)))

with open('2017_all_player.data', 'w+') as out_file:
        pp = pprint.PrettyPrinter(indent=4, stream=out_file)
        pp.pprint(all_player)


#For debug
'''

#get_WR_and_RB_information('https://www.pro-football-reference.com//players/A/AbbrJa00.htm','receiving_and_rushing')
res=get_player_basic_information('https://www.pro-football-reference.com/players/B/BradTo00.htm')
with open('2017_all_player.data', 'w+') as out_file:
    pp = pprint.PrettyPrinter(indent=4, stream=out_file)
    pp.pprint(res)
'''



