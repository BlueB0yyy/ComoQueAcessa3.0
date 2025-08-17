# core/utils.py
from ddgs import DDGS
import ollama

def search_duckduckgo(query, num_results=12):
    """
    Faz uma busca no DuckDuckGo e retorna uma lista com até 'num_results' resultados.
    Cada item contém 'title' e 'link'.
    """
    results = [] #lista de resultados
    with DDGS() as ddgs: 
        for r in ddgs.text(query, max_results=num_results): #Para cada elemento da pesquisa da query
            results.append({ #cria uma lista gigante com 12 títulos e links
                "title": r.get("title"),
                "link": r.get("href")
            })
    return results


def resposta_da_ia(query, results):
    """
    Usa Ollama para gerar um passo a passo simples e numerado
    a partir dos resultados da busca.
    """
    # Monta um resumo dos resultados
    text = "\n".join([f"- {r['title']} ({r['link']})" for r in results])

    prompt = f"""
    O usuário perguntou: "{query}".
    Aqui estão algumas informações encontradas na web:
    {text}

    Gere um passo a passo claro, simples e numerado de como acessar essa informação.
    No final, inclua links úteis.
    """

    response = ollama.chat(
        model="wizardlm2:latest",  # ou outro modelo que você tenha baixado
        messages=[
            {"role": "system", "content": "Você é um assistente que ajuda pessoas a acessar informações digitais de forma simples e didática."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]

