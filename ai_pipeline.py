import os
import json
import requests
from dotenv import load_dotenv
import assemblyai as aai
from groq import Groq
from pydantic import BaseModel, Field

load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class Tarefa(BaseModel):
    titulo: str = Field(description="Título curto e acionável da tarefa")
    descricao: str = Field(description="Detalhes do que precisa ser feito")
    responsavel: str = Field(description="Nome real citado na conversa ou 'Speaker A/B'")
    prioridade: str = Field(description="Alta, média ou baixa")


class AnaliseReuniao(BaseModel):
    total_tarefas: int = Field(description="Quantidade total de tarefas identificadas")
    minutos_economizados: int = Field(description="Estimativa de minutos economizados automatizando a ata e triagem")
    gargalo_identificado: str = Field(description="Principal ponto de atenção ou risco citado na conversa")


class ResultadoReuniao(BaseModel):
    resumo: str = Field(description="Resumo executivo da reunião")
    analise: AnaliseReuniao = Field(description="Métricas e análise de produtividade da reunião")
    tarefas: list[Tarefa] = Field(description="Lista de tarefas extraídas")




def transcrever_reuniao(caminho_audio: str) -> str:
    config = aai.TranscriptionConfig(speaker_labels=True, language_code="pt")
    transcript = aai.Transcriber().transcribe(caminho_audio, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(transcript.error)

    return "\n".join(f"Speaker {fala.speaker}: {fala.text}" for fala in transcript.utterances)


def extrair_tarefas(transcricao: str) -> dict:
    schema_json = json.dumps(ResultadoReuniao.model_json_schema(), ensure_ascii=False)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": f"Você extrai tarefas e métricas de reuniões em português. Responda APENAS um JSON válido seguindo exatamente este schema: {schema_json}"
            },
            {
                "role": "user",
                "content": f"Analise a transcrição e extraia resumo, análise e tarefas:\n\n{transcricao}"
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )

    return ResultadoReuniao.model_validate_json(response.choices[0].message.content).model_dump()



def disparar_automacao_webhook(dados: dict, webhook_url: str | None = None) -> bool:
    url = webhook_url or os.getenv("AUTOMATION_WEBHOOK_URL")
    if not url:
        return False
    response = requests.post(url, json=dados, timeout=10)
    return response.ok


if __name__ == "__main__":
    dialogo = transcrever_reuniao("audio.mp4")
    resultado = extrair_tarefas(dialogo)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    disparar_automacao_webhook(resultado)