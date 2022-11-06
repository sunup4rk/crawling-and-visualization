import selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

import time

###############################################################################################################

# chromedriver 위치
driver = webdriver.Chrome("C:/Users/thp4r/Desktop/KOSTA/python/PythonProject/bigdata/KBO_STATS_PS/chromedriver.exe")
driver.implicitly_wait(3)
driver.get('https://www.koreabaseball.com/Record/Player/HitterBasic/BasicOld.aspx?sort=HRA_RT')

###############################################################################################################

year = []
for i in range(0, 41):
    year.append(str(1982 + i))  

# 4 : 와일드카드, 3 : 준플레이오프, 5 : 플레이오프, 7 : 한국시리즈
progress = ["4", "3", "5", "7"]
                                                                                                                 
# OB : 두산, LT : 롯데, SS : 삼성, WO : 키움, HH : 한화
# HT : KIA, KT : KT, LG : LG, NC : NC, SK : SSG
# HD : 현대(해체)
team = ["OB", "LT", "SS", "WO", "HH", "HT", "KT", "LG", "NC", "SK", "HD"]

###############################################################################################################

players_NAME = []   # 이름
players_ID = []     # ID
players_TEAM = []   # 팀
players_AVG = []    # 타율
players_GAME = []   # 출장경기 수
players_PA = []     # 타석
players_AB = []     # 타수
players_H = []      # 안타
players_H2 = []     # 2루타
players_H3 = []     # 3루타
players_HR = []     # 홈런
players_RBI = []    # 타점
players_SB = []     # 도루
players_CS = []     # 도루 실패
players_BB = []     # 볼넷
players_HBP = []    # 몸에 맞는 볼
players_SO = []     # 삼진
players_GDP = []    # 병살타
players_ERR = []    # 실책

sorted_data = {}

for y in year:
    select_menu = Select(driver.find_element("id", "cphContents_cphContents_cphContents_ddlSeason_ddlSeason"))
    select_menu.select_by_value(y)
    time.sleep(1)
    for p in progress:
        try:            
            select_menu = Select(driver.find_element("id", "cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
            select_menu.select_by_value(p)
            time.sleep(1)
            for t in team:
                try:
                    select_menu = Select(driver.find_element("id", "cphContents_cphContents_cphContents_ddlTeam_ddlTeam"))
                    select_menu.select_by_value(t)
                    time.sleep(1)

                    page = driver.page_source
                    soup = bs(page, "html.parser") 

                    player_info = soup.select('div.record_result td a')
                    data_AVG = soup.find_all('td', {'data-id':"HRA_RT"})
                    data_GAME = soup.find_all('td', {'data-id':"GAME_CN"})
                    data_PA = soup.find_all('td', {'data-id':"PA_CN"})
                    data_AB = soup.find_all('td', {'data-id':"AB_CN"})
                    data_H = soup.find_all('td', {'data-id':"HIT_CN"})
                    data_H2 = soup.find_all('td', {'data-id':"H2_CN"})
                    data_H3 = soup.find_all('td', {'data-id':"H3_CN"})
                    data_HR = soup.find_all('td', {'data-id':"HR_CN"})
                    data_RBI = soup.find_all('td', {'data-id':"RBI_CN"})
                    data_SB = soup.find_all('td', {'data-id':"SB_CN"})
                    data_CS = soup.find_all('td', {'data-id':"CS_CN"})
                    data_BB = soup.find_all('td', {'data-id':"BB_CN"})
                    data_HBP = soup.find_all('td', {'data-id':"HP_CN"})
                    data_SO = soup.find_all('td', {'data-id':"KK_CN"})
                    data_GDP = soup.find_all('td', {'data-id':"GD_CN"})
                    data_ERR = soup.find_all('td', {'data-id':"ERR_CN"})

                    for element in player_info:
                        players_NAME.append(element.text)           ## 0
                        id_href = element.attrs['href']
                        ## id_href.split.('=')의 [1]번(두 번째) 요소
                        players_ID.append(id_href.split('=')[1])    ## index
                    for avg in data_AVG:                            ## 1, 값이 제대로 입력되지 않음
                        if avg == '-':
                            players_AVG.append(float(0))
                        else:
                            players_AVG.append(float(avg.text))           
                    for game in data_GAME:                          ## 2
                        players_GAME.append(int(game.text))
                    for pa in data_PA:
                        players_PA.append(int(pa.text))
                    for ab in data_AB:
                        players_AB.append(int(ab.text))
                    for h in data_H:
                        players_H.append(int(h.text))
                    for h2 in data_H2:
                        players_H2.append(int(h2.text))
                    for h3 in data_H3:
                        players_H3.append(int(h3.text))
                    for hr in data_HR:
                        players_HR.append(int(hr.text))                        
                    for rbi in data_RBI:
                        players_RBI.append(int(rbi.text))
                    for sb in data_SB:                              ## 10                           
                        players_SB.append(int(sb.text))
                    for cs in data_CS:
                        players_CS.append(int(cs.text))
                    for bb in data_BB:
                        players_BB.append(int(bb.text))
                    for hbp in data_HBP:
                        players_HBP.append(int(hbp.text))
                    for so in data_SO:
                        players_SO.append(int(so.text))
                    for gdp in data_GDP:
                        players_GDP.append(int(gdp.text))
                    for err in data_ERR:                            ## 16
                        players_ERR.append(int(err.text))

                except:
                    break
        except:
            pass
        
## 중복 데이터 정리
for i in range(len(players_ID)):
    if players_ID[i] in sorted_data:
        sorted_data[players_ID[i]][1] += players_AVG[i]
        sorted_data[players_ID[i]][2] += players_GAME[i]
        sorted_data[players_ID[i]][3] += players_PA[i]
        sorted_data[players_ID[i]][4] += players_AB[i]
        sorted_data[players_ID[i]][5] += players_H[i]
        sorted_data[players_ID[i]][6] += players_H2[i]
        sorted_data[players_ID[i]][7] += players_H3[i]
        sorted_data[players_ID[i]][8] += players_HR[i]
        sorted_data[players_ID[i]][9] += players_RBI[i]
        sorted_data[players_ID[i]][10] += players_SB[i]
        sorted_data[players_ID[i]][11] += players_CS[i]
        sorted_data[players_ID[i]][12] += players_BB[i]
        sorted_data[players_ID[i]][13] += players_HBP[i]
        sorted_data[players_ID[i]][14] += players_SO[i]
        sorted_data[players_ID[i]][15] += players_GDP[i]
        sorted_data[players_ID[i]][16] += players_ERR[i]
    else:
        sorted_data[players_ID[i]] = [players_NAME[i], players_AVG[i], players_GAME[i], players_PA[i],
                                      players_AB[i], players_H[i], players_H2[i], players_H3[i],
                                      players_HR[i], players_RBI[i], players_SB[i], players_CS[i],
                                      players_BB[i], players_HBP[i], players_SO[i], players_GDP[i], players_ERR[i]] 

driver.close()

import csv

record_index = ["이름", "타율", "경기 수", "타석", "타수", "안타", "2루타", "3루타", "홈런", "타점", "도루", "도루실패", "볼넷", "사구", "삼진", "병살타", "실책"]
df = pd.DataFrame(sorted_data, index=record_index)
df.to_csv("C:/Users/thp4r/Desktop/KOSTA/python/PythonProject/bigdata/KBO_STATS_PS/data_ps_all.csv", encoding="cp949")