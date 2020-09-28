# 犬種を判別するLineBot
## Messaging API, GoogleCloudPlatformのAuto ML, HerokuでLineBotを作成しました。

### 仕組み
#### 
1. ユーザーがボットにメッセージを送ると、Webhookを利用し、Messaging APIを通して、Herokuへリクエストを送信します。
2. 画像の場合、学習モデルのAPIを呼び出し、値をHerokuへ返します。
3. Herokuが受け取った応答リクエストを、Messaging APIへ送ります。
4. LINEが受け取り、データが表示されます。
####
### トレーニングデータの収集
1. スクレイピングで犬種名を取得する。
2. 取得した犬種名のリストを元に画像を収集しました。
