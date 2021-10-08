from django.http.response import JsonResponse
import requests 
import json
from django.shortcuts import render
from urllib.parse import parse_qs, urlparse
from hunspell import Hunspell

h = Hunspell()

def format_list (new_word_list):
    for word in new_word_list:
        print(word, end=", ")
        print("\b\b", end="")
        print(" ")
    return word

def index(request):
    return render(request,"main/index.html")

def spell_check(request):
    ##result ={'word': request.GET.get('word', None)}
    ##test=parse_qs(urlparse(result).query)
    ##result=request.GET.get('word', None)
    word_text=request.GET.get('word')
    print(word_text)
    word_string= json.dumps(word_text)
    print(word_string)
    word_list= h.suggest(word_string)
    ##print(word_list)
    data ={'output': word_list}
    print(data)
    return JsonResponse(data)
    ##return render(request,"main/index.html",data)
    ##result = request.GET.dict()
    ##word_text=(result['enter_text'])
    ##data ={'output': word_text}
    ##return render(request,"main/index.html",data)
    # word_list= h.suggest(word_text)
    # separator = ", "
    # new_word_list= separator.join(word_list)
    # transformed_string=new_word_list.replace(",","")
    # data ={'output': transformed_string}
    # return render(request, "main/index.html",data)


# #Create your views here.
# def index(request):
#     ## Get url parameters "enter_text"
#     result = request.GET.dict()
#     ## If not available start with default parameters
#     res = not bool(result)
#     if res==True :
#         result = {'enter_text': 'default'}
#         word_text=(result['enter_text'])
#         word_list=h.suggest(word_text)
#         data ={'output': word_list}
#         ## Else enter your word of choice
#     else:
#         word_text=(result['enter_text'])
#         ##word_text= "helo"
#         word_list= h.suggest(word_text)
#         data ={'output': word_list}
#     return render(request, "main/index.html",data)




