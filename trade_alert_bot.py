from flask import Flask, request
import requests
import pickle
import numpy as np

app = Flask(__name__)

# رابط Discord Webhook الخاص بك - يجب أن يكون نص بين علامات اقتباس
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1412791293339369533/ZUtybPvag81Q90cu6laPM_E6OxAx6KeZtfsXyjyXbs7rmooxku-nHQgIPhWdjRiSiZ7r'

# تحميل نموذج التعلم الآلي المدرب مسبقاً
model = pickle.load(open('model.pkl', 'rb'))

def send_to_discord(message: str):
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

def extract_features(data):
    features = [
        float(data.get('rsi', 50)),
        float(data.get('macd', 0)),
        float(data.get('adx', 25)),
        float(data.get('volume', 0)),
        1 if data.get('signal') == "BUY" else 0
    ]
    return np.array(features).reshape(1, -1)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    features = extract_features(data)
    prediction = model.predict(features)[0]

    if prediction == 1:
        signal = data.get('signal')
        symbol = data.get('symbol')
        price = data.get('price')
        message = f"🚨 High Probability {signal} signal for {symbol} at price {price}"
        send_to_discord(message)
        return "Alert sent", 200
    else:
        print("Ignored low probability signal")
        return "Signal filtered", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


