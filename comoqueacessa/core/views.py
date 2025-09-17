# core/views.py
from django.contrib.auth.decorators import login_required
import markdown
from django.utils.safestring import mark_safe
from django.shortcuts import render, get_object_or_404
from .forms import Form_de_busca
from .utility import search_duckduckgo, resposta_da_ia
from .models import Hist_busca

def home(request):
    response, results = None, None

    if request.method == "POST":                    #Se estiver postando
        form = Form_de_busca(request.POST)          #Gera um form de busca

        if form.is_valid():                         #teste de validação do form
            print('Processando')
            query = f'Como "{form.cleaned_data["query"]}"?'      #Query de busca do DuckDuckGo
            print(query)
            results = search_duckduckgo(form.cleaned_data["query"])                          #Retorno dos resultados
            print('Busca feita!')

            raw_response = resposta_da_ia(query, results)               #Resposta da IA
            print('Resposta da IA processada!')
            response = mark_safe(markdown.markdown(raw_response))       #Formatar pra aparecer certo na página

            print("Usuário autenticado?", request.user.is_authenticated)    #Só pra verificar se está logado
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
            return render(request, "core/main.html", {
                "form": form,
                "response": response,
                "results": results
            })
    else:
        form = Form_de_busca()

    return render(request, "core/main.html", {
        "form": form,
        "response": response,
        "results": results
    })

@login_required
def historico_pesquisas(request):
    pesquisas = Hist_busca.objects.filter(user=request.user).order_by("-data")
    return render(request, "core/historico.html", {"pesquisas": pesquisas})

def ver_pesquisa(request, pk):
    pesquisa = get_object_or_404(Hist_busca, pk=pk, user=request.user)
    return render(request, "core/ver_pesquisa.html", {"pesquisa": pesquisa})