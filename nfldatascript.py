from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen
import requests
import re
import csv
import time

YEARS_START=1920
YEARS_END=2017

yearteam = {}
tempteam = []
with open('nfl_elo.csv', 'r') as nflstat:#open origional data file to get all team abbreviations
    filereader = csv.reader(nflstat)#treat it as csv
    s="1920"#start year
    t=1#used to skip first line
    for row in filereader:#for each row
        if t==1:#if first row we skip
            t=0
            continue
        if s != row[1]:#else if we encounter a new year
            yearteam[s] = set(tempteam) #save the old team list (as set to remove duplicates)
            s=row[1] #
            tempteam = []
        tempteam.append(row[4].lower())#add first team
        tempteam.append(row[5].lower())#add second team
#print(yearteam['1920'])
#print(yearteam['2013'])
#exit()
#TEAMS = ['crd', 'atl', 'rav', 'buf', 'car', 'chi', 'cin', 'cle', 'dal', 'den', 'det', 'gnb', 'htx', 'clt', 'jax', 'kan', 'mia', 'min', 'nwe', 'nor', 'nyg', 'nyj', 'rai', 'phi', 'pit', 'sdg', 'sfo', 'sea', 'ram', 'tam', 'oti', 'was']
#print(len(TEAMS))
TEAMS=[]
with open('roster.csz', 'w') as f:#open file so we can write to it
    for year in range(YEARS_START, YEARS_END+1):#for each year
        TEAMS = yearteam[str(year)]#set teams from our dictionary above
        #print(year)
        successful = False#veriable to retry if we get a server error
        itr = 0;
        while not successful: 
            for team in TEAMS:#for each team
                itr = itr +1
                #print(team)
                url = "https://www.pro-football-reference.com/teams/%s/%s_roster.htm" % (team, year)#make team/year url
                #html = requests.get(url).text
                #html2 = re.sub("<!--", "", html)
                #html3 = re.sub("-->", "", html2)
                time.sleep(0.1)#sleep so server stops thinking Im a DOS attack
                roster = []#store team here
                try:
                    page = urlopen(url)#open url
                except:#page does not exist
                    roster.append('ERROR')
                    f.write('' + str(year) + ':'+ team + ',' + ','.join(roster) + '\r\n')
                    continue;
                try:
                    soup = BeautifulSoup(page)#make soup
                    body = soup.find("body")#get body
                    #print(soup)
                    #exit()
                    comments = soup.find_all(text=lambda text:isinstance(text, Comment))#get all comments
                    for comment in comments:#for each html comment
                        commentsoup = BeautifulSoup(comment)#make soup
                        tabletag = commentsoup.find('table')#search for table element
                        if tabletag is not None:#if table object is found
                            body.insert_after(tabletag)#uncomment table
                        
                    table = soup.find('table', id='games_played_team')#find roster table
                    #print(table)
                    #exit()
                    table_body = table.find('tbody')#go inside
                    #print(table_body)
                    #exit()
                    rows = table_body.find_all('tr')#get rows
                    #print(rows)
                    #exit()
                    for row in rows:#for each row
                        cols = row.find_all('td')#get columns
                        #print(cols)
                        #exit()
                        #print(cols[0].find('a').text)
                        #exit()
                        roster.append(cols[0].find('a').text)#add player coloumn text (name)
                    successful = True #we succeed no server error so don't retry
                except Exception as e:#server error occurs
                    #print(e)
                    print(str(year) + ':' +team)#fancy 404 error
                    #print(url)
                    roster.append('ERROR')#say so in file for further investigation
                finally:
                    f.write('' + str(year) + ':'+ team + ',' + ','.join(roster) + '\r\n')#write roster to file
                if itr == 4:#if we try four times then stop retying
                    successful = True;
