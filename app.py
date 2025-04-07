from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

MAKE_WEBHOOK_URL = "https://hook.us2.make.com/ktna7jnxh8d7l14uuejyjtic75pp4apr"

@app.route("/consultar_dados_profissional", methods=["POST"])
def consultar_dados_profissional():
    data = request.json
    nome = data.get("nome")

    if not nome:
        return jsonify({"erro": "Parâmetro 'nome' não informado"}), 400

    try:
        # Envia o nome para o Make
        response = requests.post(MAKE_WEBHOOK_URL, json={"nome": nome})
        resposta_make = response.text

        return jsonify({
            "resposta": resposta_make
        })

    except Exception as e:
        return jsonify({
            "erro": "Erro ao consultar dados",
            "detalhes": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
