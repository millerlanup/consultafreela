from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Autenticação com o Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("sua-chave.json", scope)
client = gspread.authorize(creds)

# Abre a planilha (coloque o ID da sua planilha aqui)
sheet = client.open_by_key("1_kGPoAV8mT_i1wzOvo_FsBgK2yGz8aPpc4Vxv5eNj34").sheet1

@app.route("/resposta")
def responder():
    pergunta = request.args.get("pergunta", "").lower()
    dados = sheet.get_all_records()

    for linha in dados:
        if linha["Palavra-chave"].lower() == pergunta:
            return jsonify({"resposta": linha["Resposta"]})
    return jsonify({"resposta": "Desculpe, não encontrei uma resposta."})

if __name__ == "__main__":
    app.run()
