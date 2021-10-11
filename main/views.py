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
    word_text=request.GET.get('word')
    print(word_text)
    word_string= json.dumps(word_text)
    print(word_string)
    replaced_string = word_string.replace('"', "")
    print(replaced_string)
    word_list= h.suggest(replaced_string)
    print(word_list)
    separator = ", "
    new_word_list= separator.join(word_list)
    transformed_string=new_word_list.replace(",","")
    data ={'output': transformed_string}
    print(data)
    return JsonResponse(data)
