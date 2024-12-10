from flask import Flask, request, render_template, jsonify
import os
import json

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'datajson')


@app.route('/')
def index():
    return render_template('multisearch.html')


@app.route('/buscar', methods=['POST'])
def buscar():
    termo_de_busca = request.json.get('termo', '').lower()
    resultados_encontrados = []

    arquivos_json = ['equipments.json', 'materials.json', 'purchase_orders.json', 'sales_orders.json', 'workface.json']

    for arquivo in arquivos_json:
        caminho_arquivo = os.path.join(DATA_DIR, arquivo)
        if not os.path.exists(caminho_arquivo):
            continue

        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            if termo_de_busca in json.dumps(dados, ensure_ascii=False).lower():
                resultados_encontrados.append({
                    'arquivo': arquivo,
                    'dados': dados
                })

    if resultados_encontrados:
        return jsonify(resultados_encontrados)
    else:
        return jsonify({'mensagem': 'Nenhum resultado encontrado.'}), 404


if __name__ == '__main__':
    app.run(debug=True)
