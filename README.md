# 🎙️ voice2task — Automação de Reuniões para Tarefas com IA

API REST e pipeline inteligente em Python que transforma gravações de reuniões em tarefas estruturadas, priorizadas e prontas para automação, eliminando o trabalho manual de criar atas e distribuir demandas.

---

## ⚙️ Como funciona (Arquitetura)

1. **Transcrição e Diarização (`AssemblyAI`):** Converte o áudio da reunião em texto em português identificando automaticamente quem falou cada trecho (`Speaker A`, `Speaker B`).
2. **Extração Estruturada e Análise Operacional (`Groq` + `Pydantic`):** Orquestra o modelo `openai/gpt-oss-120b` com *Structured Outputs* para gerar:
   * Resumo executivo da reunião;
   * Lista de tarefas acionáveis com identificação automática do responsável real pelo contexto da conversa e classificação de prioridade (`Alta`, `Média`, `Baixa`);
   * Métricas de produtividade (total de tarefas, estimativa de minutos economizados e principal gargalo/risco identificado).
3. **API REST (`Flask`):** Expõe o endpoint `POST /processar-reuniao` para envio de arquivos de áudio e retorno imediato em JSON.
4. **Integração via Webhook (`n8n` / `Make` / `Zapier`):** Dispara automaticamente o payload estruturado para fluxos externos de automação (envio para Kanban, Slack, Discord ou planilhas).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem & Framework:** Python, Flask
* **Inteligência Artificial:** AssemblyAI API (Speech-to-Text & Speaker Diarization), Groq API (`openai/gpt-oss-120b`)
* **Validação & Contratos de Dados:** Pydantic (`json_schema` / Structured Outputs)
* **Integrações:** APIs REST, Webhooks (`requests`), `python-dotenv`

---

## 🚀 Como rodar localmente

### 1. Clone o repositório e crie o ambiente virtual
```bash
git clone https://github.com/airtonxjunior/voice2task.git
cd voice2task
python -m venv venv
```

Ative o ambiente virtual:
* **Windows:** `venv\Scripts\activate`
* **Linux/Mac:** `source venv/bin/activate`

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto (baseado no `.env.example`) e preencha suas chaves:
```env
ASSEMBLYAI_API_KEY=sua_chave_assemblyai
GROQ_API_KEY=sua_chave_groq
AUTOMATION_WEBHOOK_URL=sua_url_webhook_opcional
```

### 4. Execute a API
```bash
python app.py
```
O servidor iniciará em `http://127.0.0.1:5000`.

---
