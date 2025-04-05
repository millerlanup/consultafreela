from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Conexão com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("sua-chave.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1_kGPoAV8mT_1wzOvo_FsBgK2yGz8aPpc4Vxv5eNj34").sheet1

@app.route("/resposta")
def responder():
    try:
        nome_procurado = request.args.get("nome", "").strip().lower()
        if not nome_procurado:
            return jsonify({"erro": "Informe o nome na URL. Ex: ?nome=miller"}), 400

        dados = sheet.get_all_records()
        if not dados:
            return jsonify({"erro": "A planilha está vazia."}), 404

        for linha in dados:
            nome = linha.get("nome", "").strip().lower()
            if nome == nome_procurado:
                return jsonify({
                    "status": linha.get("Status", "Não informado"),
                    "função": linha.get("função", "Não informado"),
                    "telefone": linha.get("telefone", "Não informado"),
                    "email": linha.get("email", "Não informado"),
                    "endereço": linha.get("endereço", "Não informado"),
                    "cpf": linha.get("cpf", "Não informado")
                })

        return jsonify({"erro": f"O nome '{nome_procurado}' não foi encontrado na planilha."}), 404

    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor", "detalhes": str(e)}), 500

if __name__ == "__main__":
    app.run()
