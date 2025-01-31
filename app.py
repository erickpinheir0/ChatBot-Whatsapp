from flask import Flask, request, jsonify
from services.waha import Waha

app = Flask(__name__)

@app.route('/chatbot/webhook/', methods=['POST'])

def webhook():
    data = request.json
    print(f'EVENTO RECEBIDO: {data}')

    waha = Waha()
    chat_id = data['payload']['from']
    waha.send_message(chat_id=chat_id, message='Resposta Automática =)')

    if data is None:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    return jsonify({ 'status': 'success' }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)