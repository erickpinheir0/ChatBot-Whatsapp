from flask import Flask, request, jsonify
from services.waha import Waha
from bot.ai_bot import AI_Bot
import time
import random

app = Flask(__name__)

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json
    print(f'EVENTO RECEBIDO: {data}')

    # Inicializando o Waha e o AI_Bot
    waha = Waha()
    ai_bot = AI_Bot()

    # Obtendo o chat_id e a mensagem do evento
    chat_id = data['payload']['from']
    received_message = data['payload']['body']

    # Iniciando o typing para o usuario, enquanto ele espera a resposta
    waha.start_typing(chat_id=chat_id)
    time.sleep(random.randint(3, 10))

    # Enviando a mensagem para o ChatBot, recebendo a resposta, e enviando para o Whatsapp
    ai_bot_response = ai_bot.invoke(question=received_message)
    waha.send_message(chat_id=chat_id, message=ai_bot_response)

    # Parando o typing para o usuario
    waha.stop_typing(chat_id=chat_id)

    if data is None:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    return jsonify({ 'status': 'success' }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)