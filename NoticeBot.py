#!/usr/bin/env python
# encoding=utf-8
import requests
import time
from bs4 import BeautifulSoup
import telegram
import copy
import yaml

yamldoc = yaml.load(open('securityToken.yml의 절대경로', 'r'), Loader=yaml.FullLoader)
bot = telegram.Bot(token=yamldoc['telegram']['botToken'])
chatBot_id = bot.getUpdates()[1].channel_post.chat.id

if __name__ == '__main__':
    try:
        print("강대 컴정 공지사항 봇")
        changeList = None
        while True:
            req = requests.get('https://cse.kangwon.ac.kr:60443/')
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            checklist = []
            noticesCrop = soup.find("div", {"class": "tab t1 on"})
            noticeList = noticesCrop.find_all("li")
            for i in noticeList:
                title = i.find("a").get("title")
                herf = i.find("a").get("href")
                noticetTime = i.find("span").text
                checklist.append([title, herf, noticetTime])
                print(title)
            if changeList is None:
                changeList = copy.deepcopy(checklist)
            print(checklist)
            # 비교
            setChange = set(tuple(row) for row in changeList)
            setCheck = set(tuple(row) for row in checklist)
            diff = setCheck - setChange
            if len(diff) > 0:
                changeList = copy.deepcopy(checklist)
            for index in diff:
                print(index[0])
                botText = '<strong>[강대 컴퓨터학과 공지사항 업데이트]</strong>'+'\n\n'
                botText = botText+'<strong>'+index[0]+'</strong>\n\n'
                botText = botText+'<i>'+index[2]+'</i>\n'
                botText = botText +"https://cse.kangwon.ac.kr:60443/"+index[1]
                bot.send_message(chat_id=chatBot_id, text=botText, parse_mode=telegram.ParseMode.HTML)
            print('작동중!')
            time.sleep(900) # 15분 간격으로 크롤링 >
    except Exception as es:
        print("오류 발생!!! 오류원인: "+str(es))
        bot.sendMessage(yamldoc['telegram']['channelNum'], u'강대 컴정봇이 맛탱이가 갔습니다 확인해주세요.' + '   ' + str(es))

