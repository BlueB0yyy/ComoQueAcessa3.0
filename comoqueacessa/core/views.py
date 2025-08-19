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
            print("Usuário autenticado?", request.user.is_authenticated)
            print("Usuário:", request.user)
            if request.user.is_authenticated:
                Hist_busca.objects.create(
                    user=request.user,
                    busca=query,
                    resposta=response
                )
            # Se foi um POST via HTMX, renderiza só os resultados
            if request.headers.get("HX-Request"):
                return render(request, "core/resultados.html", {
                "response": response,
                "results": results
                })
    else:
        form = Form_de_busca()

    return render(request, "core/master.html", {
        "form": form,
        "response": response,
        "results": results
    })

def guest(request):
    return render(request, "core/guest.html")  # pode criar um guest.html simples






