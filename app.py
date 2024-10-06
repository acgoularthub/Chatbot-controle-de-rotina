import os
import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Inicializa o Flask
app = Flask(__name__)

# Configura a chave da API do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para gerar resposta do ChatGPT
def get_gpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Rota para o webhook do WhatsApp
@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg:
        gpt_response = get_gpt_response(incoming_msg)
        msg.body(gpt_response)
    else:
        msg.body("Desculpe, não entendi sua mensagem.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
