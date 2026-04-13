from flask import Flask, request, jsonify
from flask_cors import CORS
import pyttsx3
import threading
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

def speak(message):
    def run():
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'french' in voice.name.lower() or 'fr' in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.say(message)
        engine.runAndWait()
    thread = threading.Thread(target=run)
    thread.start()

@app.route('/alert', methods=['POST'])
def receive_alert():
    data = request.json
    alerts = data.get('alerts', [])
    for alert in alerts:
        name        = alert.get('labels', {}).get('alertname', 'Alerte inconnue')
        severity    = alert.get('labels', {}).get('severity', 'inconnue')
        summary     = alert.get('annotations', {}).get('summary', '')
        description = alert.get('annotations', {}).get('description', '')
        resolved    = alert.get('resolved', False)

        if resolved:
            message = f"Bonne nouvelle. {summary} est de nouveau en ligne. Incident resolu."
        else:
            message = f"Attention ! {summary}. {description}. Severite : {severity}."

        app.logger.info(f"Alerte recue : {message}")
        speak(message)
    return jsonify({"status": "ok"}), 200

@app.route('/resolved', methods=['POST'])
def receive_resolved():
    data = request.json
    server_name = data.get('server', 'Serveur inconnu')
    message = f"Bonne nouvelle. {server_name} est de nouveau en ligne. Incident resolu."
    app.logger.info(f"Resolution recue : {message}")
    speak(message)
    return jsonify({"status": "ok"}), 200

@app.route('/test', methods=['GET'])
def test_voice():
    speak("Test vocal du tableau de bord de supervision. Systeme operationnel.")
    return jsonify({"status": "test envoye"}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)