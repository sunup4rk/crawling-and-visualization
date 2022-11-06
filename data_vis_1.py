import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("C:/Users/thp4r/Desktop/KOSTA/python/PythonProject/bigdata/KBO_STATS_PS/data_ps_all.csv", index_col=0, encoding="cp949")

players_ID = data.keys()

players_NAME = []   # 이름
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

for key in players_ID:
    players_NAME.append(data[key][0])
    players_AVG.append(data[key][1])
    players_GAME.append(float(data[key][2]))
    players_PA.append(float(data[key][3]))
    players_AB.append(float(data[key][4]))
    players_H.append(float(data[key][5]))
    players_H2.append(float(data[key][6]))
    players_H3.append(float(data[key][7]))
    players_HR.append(float(data[key][8]))
    players_RBI.append(float(data[key][9]))
    players_SB.append(float(data[key][10]))
    players_CS.append(float(data[key][11]))
    players_BB.append(float(data[key][12]))
    players_HBP.append(float(data[key][13]))
    players_SO.append(float(data[key][14]))
    players_GDP.append(float(data[key][15]))
    players_ERR.append(float(data[key][16]))

df = pd.DataFrame()
df['AB'] = players_AB
df['GDP'] = players_GDP
df['NAME'] = players_NAME

import matplotlib
matplotlib.rcParams['font.family'] ='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] =False

cutoff1 = (((df['GDP'] > df['AB'] * 0.035)) & (df['GDP'] > 5)) | (df['GDP'] > 10)
df['color1'] = np.where(cutoff1==True, "orangered", "lightblue")
# Scatter Plot with regression line by seaborn regplot()
sns.regplot(x=df['AB'], 
           y=df['GDP'], 
           fit_reg=True,
           scatter_kws={'facecolors': df['color1']}) # default
plt.title('포스트시즌 최다 더블플레이', fontsize=20)
plt.xlabel('타수', fontsize=14)
plt.ylabel('더블플레이', fontsize=14)

for i, txt in enumerate(players_NAME):
    if ((players_GDP[i] > players_AB[i] * 0.035) and (players_AB[i] > 150 or players_GDP[i] > 5)) or players_GDP[i] > 10:
        plt.annotate(txt, (players_AB[i], players_GDP[i]))
    else:
        pass

plt.show()