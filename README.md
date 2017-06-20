# BacklogCountTool
## 概要
backlogの、当月1ヶ月分のメンバー毎のチケット総数、予定時間、実績時間を集計し、Slackへ通知するLambda Functionです。

## リポジトリのclone
```
git clone https://github.com/y-fujisaki/BacklogCountTool.git
```

## ライブラリインストール
* Lambdaに標準で入っていないライブラリを使用します。
* cloneしたフォルダで実行してください。

```
cd BacklogCountTool
pip install requests -t .
pip install datetime -t .
pip install python-dateutil -t .
pip install slackweb -t .
```

## config.pyの変更
ご利用の環境に合わせて値を入力してください。

``` config.py
## ホスト名
host = '{your-space}' 
## Backlog API KEY
api = '{your-apikey}'
## MEMBER名とIDを指定：集計する担当者分セット
assigend_member=[['name1',{担当者のID}],['name2',{担当者のID}]]
## Slack Webhook
slack_webhook="your-slack-Webhook URL"

```

## zipで圧縮

```
zip -r upload.zip *
```

## アップロード
* Lambda Functionを作成し、AWS マネジメントコンソールまたはAWS CLIからZIPファイルをアップロードしてください

## ハンドラー
[設定]-[ハンドラー]には実行スクリプト名に合わせた、以下の値を入力して下さい。

```
BacklogCountTool.lambda_handler
```

## イメージ（Slack通知）
![サンプル](https://s3-ap-northeast-1.amazonaws.com/backlog-count-tool/image.png "サンプル")

