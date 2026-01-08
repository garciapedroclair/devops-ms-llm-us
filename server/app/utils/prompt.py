import requests
import re

OLLAMA_URL="http://172.17.0.1:11434/api/generate"
OLLAMA_MODEL = "gemma:2b"

def evaluate_with_llm(task: dict) -> dict:
    prompt = f"""
        Você é um avaliador de Engenharia de Software.

        Avalie a história de usuário e seus casos de uso, usando APENAS os scores 0, 5 ou 10.

        Critérios:
        - Score 0: O participante não completou a tarefa ou falhou em atender aos elementos obrigatórios.
        - Score 5: O participante atendeu parcialmente à tarefa.
        - Score 10: O participante atendeu completamente à tarefa.

        História de usuário, padrão esperado: 
                                            EU COMO <persona>,     
                                            GOSTARIA DE <ação>,     
                                            PARA <benefício>.

        Caso de uso, fluxo principal e alterantivo. Padão espereado: 
                                            DADO QUE <pré-condição> E <pré-condição> ... 
                                            QUANDO <Ação> E <Ação> ... 
                                            ENTÃO <pós-condição> E <pós-condição> ...

        Descrição:
        {task.get("description", "")}

        Fluxo principal:
        {task.get("main_flow", "")}

        Fluxos alternativos:
        {task.get("alt_flow", "")}

        Formato da resposta (siga exatamente):
        Score: <0|5|10>
        Comentário: <texto justificando o Score>
        """.strip()

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 512,
            "temperature": 0.0
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )
        response.raise_for_status()
        text = response.json().get("response", "")
    except Exception as e:
        return {
            "score": 0,
            "comment": f"Erro ao consultar o LLM: {str(e)}"
        }

    # =======================
    # Parsing robusto
    # =======================

    score_match = re.search(r"Score:\s*(0|5|10)", text)
    comment_match = re.search(r"Comentário:\s*(.*)", text, re.DOTALL)

    score = int(score_match.group(1)) if score_match else 0
    comment = comment_match.group(1).strip() if comment_match else ""

    if score != 10 and not comment:
        comment = "Comentário não fornecido pelo avaliador."

    if score == 10:
        comment = ""

    return {
        "score": score,
        "comment": comment
    }
