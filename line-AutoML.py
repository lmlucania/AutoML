from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)
import os

from io import BytesIO

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

dic = {'Afghan_Hound': 'アフガンハウンド', 'Akita': '秋田犬', 'Alaskan_Malamute': 'アラスカンマラミュート', 'American_Cocker_Spaniel': 'アメリカンコッカースパニエル', 'Basset_Hound': 'バセットハウンド'
, 'Beagle': 'ビーグル', 'Bernese_Mountain_Dog': 'バーニーズ', 'Bichon_Frise': 'ビションフリーゼ', 'Border_Collie': 'ボーダーコリー', 'Borzoi': 'ボルゾイ', 'Boston_Terrier': 'ボストンテリア'
, 'Boxer': 'ボクサー', 'Bulldog': 'ブルドッグ', 'Cat': '猫', 'Cavalier_King_Charles_Spaniel': 'キャバリア', 'Chihuahua': 'チャウチャウ', 'Chinese_Crested_Dog': 'チャイニーズ・クレストドッグ'
, 'Collie': 'コリー', 'Dalmatian': 'ダルメシアン', 'Doberman': 'ドーベルマン', 'English_Cocker_Spaniel': 'イングリッシュ・コッカースパニエル', 'French_Bulldog': 'フレンチブルドッグ'
, 'Golden_Retriever': 'ゴールデン・レトリーバー', 'Great_Dane': 'グレートデーン', 'Great_Pyrenees': 'グレートピレニーズ', 'Irish_Setter': 'アイリッシュ・セッター'
, 'Irish_Wolfhound': 'アイリッシュ・ウルフハウンド','Italian_Greyhound': 'イタリアン・グレーハウンド','Jack_Russell_Terrier': 'ジャックラッセルテリア','Japanese_Chin': '狆'
, 'Japanese_Spitz': '日本スピッツ','Kai': '甲斐犬','Kishu': '紀州犬','Labrador_Retriever': 'ラブラドール・レトリーバー','Maltese': 'マルチーズ','Miniature Pinscher': 'ミニチュアピンシャー'
, 'Miniature_Dachshund': 'ミニチュアダックスフンド', 'Miniature_Schnauzer': 'ミニチュアシュナウザー', 'Mix': 'ミックス', 'Papillon': 'パピヨン', 'Pekingese': 'ペキニーズ'
, 'Pembroke_Welsh_Corgi': 'コーギー', 'Pomeranian': 'ポメラニアン', 'Poodle': 'スタンダードプードル', 'Pug': 'パグ', 'Rottweiler': 'ロットワイラー', 'Saint_Bernard': 'セントバーナード'
, 'Saluki': 'サルーキ', 'Samoyed': 'サモエド', 'Shetland_Sheepdog': 'シェットランドシープドッグ','Shiba': '柴犬', 'Shih_Tzu': 'シーズー', 'Shikoku': '四国犬', 'Siberian_Husky': 'シベリアンハスキー'
, 'Tosa': '土佐犬', 'Toy_Poodle': 'トイプードル', 'Weimaraner': 'ワイマラナー', 'Whippet': 'ウィペット', 'White_Shepherd': 'ホワイトシェパード', 'Yorkshire_Terrier': 'ヨークシャーテリア'}


app = Flask(__name__)

#herokuから取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

#確認用
@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# テキスト返信
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = 'わんちゃんの写真から犬種を判別するよ'
    #webhookエラー回避
    if event.reply_token == "00000000000000000000000000000000":
        return

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message)
    )
#画像返信
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)

    image_bin = BytesIO(message_content.content)
    image = image_bin.getvalue()
    request = get_prediction(image)
    #AutoMLオブジェクトなし
    if not request.payload:
        message = '識別できませんでした。'
        send_message(event, message)
    score = request.payload[0].classification.score
    display_name = request.payload[0].display_name
    if display_name == 'Cat':
        message = 'おやおや、この写真はねこですね！\nねこは毛柄によって性格が違うようですよ\nhttps://sippo.asahi.com/article/11928822'
        send_message(event, message)
    elif display_name in dic.keys():
        message = str(int(score*100))+'％の確率で、'
        #日本語変換
        display_name = dic[display_name]
        message += display_name
        message += 'です'
        send_message(event, message)
def send_message(event, message):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message)
     )
#AutoML設定
def get_prediction(content):
    project_id = '718397402380'
    model_id = 'ICN8251487320784502784'
    KEY_FILE = "arcane-fire-268313-d167296f9068.json"
    prediction_client = automl_v1beta1.PredictionServiceClient.from_service_account_json(KEY_FILE)

    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request 


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
