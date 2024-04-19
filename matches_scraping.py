import requests
from bs4 import BeautifulSoup
import csv
from datetime import date,timedelta
import os

dateset = input("Date (04-17-2024) / (04-18-2024): ").split('/',1)
date = date.fromisoformat(dateset[0])
date1 = date.fromisoformat(dateset[1])
diff = date1 - date
##                                                                                                                                         --date-structure 4/18/2024
pages = [requests.get(f'https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={(date+timedelta(days=i)).month}/{(date+timedelta(days=i)).day}/{(date+timedelta(days=i)).year}#') for i in range(diff.days)]

def main(page,date):
    src = page.content
    soup = BeautifulSoup(src, "html.parser")
    matches_details = []

    championships =soup.find_all("div", {'class':'matchCard'})
    

    def get_match_info(championship):
        all_matches = championship.contents[3].find_all('div',{'class':['item finish liItem','item future liItem','item now liItem']})
        championships_title = championship.contents[1].find("h2").text.strip()
        num_of_matchs = len(all_matches)
        
        for i in range(num_of_matchs):
            #get teams names
            teamsA = all_matches[i].find("div",{'class':'teams teamA'}).text.strip()
            teamsB = all_matches[i].find("div",{'class':'teams teamB'}).text.strip()
            match_results = all_matches[i].find("div",{'class':'MResult'}).find_all("span",{'class':'score'})
            score = f"{match_results[0].text.strip()} - {match_results[1].text.strip()}"
            match_time = all_matches[i].find("div",{'class':'MResult'}).find("span",{'class':'time'}).text.strip()
            # adding to matchs_details
            matches_details.append({"Type of championship":championships_title,"Frist team":teamsA,
            "Secend team":teamsB,"Match time":match_time,
            "Score":score,"Date":str(date)})
        
    for i in range(len(championships)):
        get_match_info(championships[i])

    keys = matches_details[0].keys()

    if os.path.exists(f"matches.csv") == False :
        with open(f"matches.csv","w",encoding="utf-8-sig",newline='') as output:
            dict_writer = csv.DictWriter(output,keys)
            dict_writer.writeheader()
            dict_writer.writerows(matches_details)
            print(f"file {output.name[:len(output.name)-4]} created")
    else:
        with open(f"matches.csv","a",encoding="utf-8-sig",newline='') as mod:
            dict_writer = csv.DictWriter(mod,keys)
            dict_writer.writerows(matches_details)
            print(f"date {mod.name[:len(mod.name)-4]} added")
        
    
for p in range(len(pages)):
    main(pages[p],(date + timedelta(days=p)))
    
# os.rename("matches.csv",f"matches{date}-{date1-timedelta(days=1)}.csv")
