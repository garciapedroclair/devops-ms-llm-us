import requests

OLLAMA_URL = "http://ollama:11434/api/generate"
OLLAMA_MODEL = "phi3:mini"

def evaluate_with_llm(task: dict) -> dict:
    prompt = f"""
Você é um avaliador de Engenharia de Software.

Avalie a história de usuário usando APENAS os scores 0, 5 ou 10.

Critérios:
- Score 0: O participante não tentou a tarefa ou falhou em atender aos elementos obrigatórios.
- Score 5: O participante atendeu parcialmente à tarefa. O motivo do score DEVE ser explicado.
- Score 10: O participante atendeu completamente à tarefa. NÃO escreva comentário.

História de usuário (padrão esperado: "Como <persona>, quero <ação>, para <benefício>"):

Descrição:
{task["description"]}

Fluxo principal:
{task["main_flow"]}

Fluxos alternativos:
{task["alt_flow"]}

Formato da resposta (siga exatamente):
Score: <0|5|10>
Comentário: <texto ou vazio>
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.0
        },
        timeout=300
    )

    text = response.json()["response"]

    score = None
    comment = ""

    for line in text.splitlines():
        if line.startswith("Score:"):
            score = int(line.replace("Score:", "").strip())
        elif line.startswith("Comentário:"):
            comment = line.replace("Comentário:", "").strip()

    if score != 10 and not comment:
        comment = "Comentário não fornecido pelo avaliador."

    return {
        "score": score,
        "comment": comment
    }