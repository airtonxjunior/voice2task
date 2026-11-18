import os
import tempfile
from flask import Flask, request, jsonify
from ai_pipeline import transcrever_reuniao, extrair_tarefas, disparar_automacao_webhook

app = Flask(__name__)


@app.route("/", methods=["GET"])
def status():
    return jsonify({"status": "online", "servico": "voice2task API"})


@app.route("/processar-reuniao", methods=["POST"])
def processar_reuniao():
    if "audio" not in request.files:
        return jsonify({"erro": "Envie um arquivo no campo 'audio'"}), 400

    arquivo = request.files["audio"]
    extensao = os.path.splitext(arquivo.filename)[1] or ".mp3"

    with tempfile.NamedTemporaryFile(delete=False, suffix=extensao) as temp:
        arquivo.save(temp.name)
        caminho_temp = temp.name

    try:
        transcricao = transcrever_reuniao(caminho_temp)
        resultado = extrair_tarefas(transcricao)
        disparar_automacao_webhook(resultado)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)


if __name__ == "__main__":
    app.run(debug=True)