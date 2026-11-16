import os
from dotenv import load_dotenv
import assemblyai as aai

load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def transcrever_reuniao(caminho_audio: str) -> str:
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        language_code="pt"
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(caminho_audio, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(transcript.error)

    dialogo = []
    for fala in transcript.utterances:
        dialogo.append(f"Speaker {fala.speaker}: {fala.text}")

    return "\n".join(dialogo)



if __name__ == "__main__":
    resultado = transcrever_reuniao("audio.mp3")
    print(resultado)