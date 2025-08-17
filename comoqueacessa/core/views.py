# core/views.py
from django.shortcuts import render
from .forms import Form_de_busca
from .utility import search_duckduckgo, resposta_da_ia
from .models import Hist_busca

def home(request):
    response, results = None, None
    if request.method == "POST": #Se estiver postando
        form = Form_de_busca(request.POST) #Gera um form de busca
        if form.is_valid(): #teste de validação do form
            query = f'Como acessar'+form.cleaned_data["query"]+'?' #Query de busca do DuckDuckGo
            results = search_duckduckgo(query) #Retorno dos resultados
            response = resposta_da_ia(query, results) #Resposta da IA
            # if request.user.is_authenticated: #Se o usuário estiver logado
            #     Hist_busca.objects.create(user=request.user, query=query, response=response) #Cria um novo objeto no histórico
    else:
        form = Form_de_busca()

    return render(request, "core/home.html", {"form": form, "response": response, "results": results})

