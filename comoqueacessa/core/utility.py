# core/utility.py
from ddgs import DDGS
import ollama

def search_duckduckgo(query, num_results=6):
    """
    Faz uma busca no DuckDuckGo e retorna uma lista com até 'num_results' resultados.
    Cada item contém 'title' e 'link'.
    """
    results = [] #lista de resultados
    with DDGS() as ddgs: 
        for r in ddgs.text(query, region='pt-br', max_results=num_results): #Para cada elemento da pesquisa da query
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
    Busque nos sites também se forem os sites onde o usuário poderá encontrar a informação, e exiba o passo a passo dos sites.
    Quero que visite os sites passados e retorne as opções detalhadas nos sites sobre como acessar a informação.
    As listagens devem ser separadas por links, exceto quando forem relacionadas. Quaisuqer subtópicos devem ser subitens da lista.
    Evite dar instruções sobre conexão com navegador, pois o usuário já tem esse acesso.
    No passo a passo, inclua links clicáveis para os sites que os usuários devem acessar, não direcionando eles para outros sistemas de busca.
    Divida respostas diferentes em listagens diferentes (se for explicar um certo passo a passo, ao passar para um novo, comece do 1 novamente)
    No final, inclua links úteis.
    """

    print(prompt)
    response = ollama.chat(
        model="wizardlm2:latest",  # ou outro modelo que você tenha baixado
        messages=[
            {"role": "system", "content": "Você é um assistente que ajuda pessoas a acessar informações digitais de forma simples e didática."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]

