from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("sua-chave.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1_kGPoAV8mT_1wzOvo_FsBgK2yGz8aPpc4Vxv5eNj34").sheet1

@app.route("/resposta")
def responder():
    nome_procurado = request.args.get("nome", "").lower()
    dados = sheet.get_all_records()

    for linha in dados:
        if linha["nome"].strip().lower() == nome_procurado:
            return jsonify({
                "status": linha.get("Status", "Não informado"),
                "função": linha.get("função", "Não informado"),
                "telefone": linha.get("telefone", "Não informado"),
                "email": linha.get("email", "Não informado"),
                "endereço": linha.get("endereço", "Não informado"),
                "cpf": linha.get("cpf", "Não informado")
            })

    return jsonify({"erro": "Profissional não encontrado."})

if __name__ == "__main__":
    app.run()
