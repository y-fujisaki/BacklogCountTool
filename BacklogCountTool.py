import requests
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import json
import slackweb
import config

# 設定値(Backlog)
## ホスト名
host = config.host

## API KEY
api= config.api

## MEMBER名とIDを指定
ASSIGNED_MEMBER=config.assigend_member

# slack webhook
SLACK=config.slack_webhook

def lambda_handler(event, context):
    try:
        # 月初と月末をそれぞれ開始日、期限日にセット
        today = date.today()
        getDate=get_first_last_date(today) 
        DUE_DATE_SINCE= 'dueDateSince={0}'.format(getDate[0]) #開始日
        DUE_DATE_UNTIL= 'dueDateUntil={0}'.format(getDate[1])  # 期限日

        ## 画面出力
        slack_post = "集計期間:" + str(getDate[0]) + "〜" + str(getDate[1]) + '\n'   

        # 担当者分、下記処理を回す。
        length= len(ASSIGNED_MEMBER)
        i=0

        while i < length:            
            ASSIGNED_ID = 'assigneeId[]={0}'.format(ASSIGNED_MEMBER[i][1])

            ## HOST:backlogのスペースをURLに    
            HOST = 'https://' + host + '.backlog.jp'
            ## API_KEY：BacklogのAPI_KEYをクエリ用に
            API_KEY = 'apiKey=' + api

            # 予実の取得
            budget=budgetControl(HOST,API_KEY,ASSIGNED_ID,DUE_DATE_SINCE,DUE_DATE_UNTIL)
            # チケット総数の取得
            count= countIssue(HOST,API_KEY,ASSIGNED_ID,DUE_DATE_SINCE,DUE_DATE_UNTIL)

            # Slackへの投稿内容
            slack_post = slack_post + str(ASSIGNED_MEMBER[i][0]) \
                + " : " + "チケット総数:" \
                + str(count)  \
                + " : " + "予定工数:" \
                + str(budget[0]) \
                + " : " + "実績工数:" \
                + str(budget[1]) \
                + '\n'        

            i=i+1
        # Slackへの投稿処理
        slackpost(slack_post)
    except:
       slackpost('Backlogの予実情報が取得できませんでした')    

## 予実計算関数
def budgetControl(HOST,API_KEY,ASSIGNED_ID,DUE_DATE_SINCE,DUE_DATE_UNTIL):
        r = requests.get(HOST + '/api/v2/issues' + '?' + API_KEY + '&' + ASSIGNED_ID + '&' + DUE_DATE_SINCE  + '&' + DUE_DATE_UNTIL + '&count=100' + '&parentChild=0') 
        # print(r.json())
        len_issues = len(r.json())
        i=0
        ESTIMATED_HOURS = 0
        ACTUAL_HOURS = 0
        while i < len_issues:
            # 予定時間の集計
            if r.json()[i]['estimatedHours'] is not None:
                ESTIMATED_HOURS =ESTIMATED_HOURS + r.json()[i]['estimatedHours']
            # 実績時間の集計
            if r.json()[i]['actualHours'] is not None:
                ACTUAL_HOURS =ACTUAL_HOURS + r.json()[i]['actualHours']
            i += 1        
               
        return ESTIMATED_HOURS,ACTUAL_HOURS

# 対象チケット件数関数
def countIssue(HOST,API_KEY,ASSIGNED_ID,DUE_DATE_SINCE,DUE_DATE_UNTIL):
         r = requests.get(HOST + '/api/v2/issues/count' + '?' + API_KEY + '&' + ASSIGNED_ID + '&' + DUE_DATE_SINCE  + '&' + DUE_DATE_UNTIL)  
         ISSUE_COUNT = r.json()['count']
         return ISSUE_COUNT

# slack投稿
def slackpost(POST):

    slack = slackweb.Slack(url=SLACK)
    slack.notify(text=POST)

# 月初日・月末日を取得
def get_first_last_date(today):

    firstDate = today - timedelta(days=today.day-1)
    lastDate  = today + relativedelta(months=1) - timedelta(days=today.day)
    return firstDate,lastDate

# 翌月　月初日・月末日を取得
def get_next_first_last_date(today):
    

    firstDate = today - timedelta(days=today.day-1)
    nextfirstDate= firstDate + relativedelta(months=1)
    nextlastDate  = today + relativedelta(months=2) - timedelta(days=today.day)
    return nextfirstDate,nextlastDate