## Import necessary packages
from django.http.response import JsonResponse
# import requests 
import json
from django.shortcuts import render
from urllib.parse import parse_qs, urlparse
from hunspell import Hunspell

## define hunspell variables
h = Hunspell()

## render views function
def index(request):
    return render(request,"main/index.html")

## hunspell check function
def spell_check(request):
    word_text=request.GET.get('word')
    print(word_text)## for testing in console
    word_string= json.dumps(word_text)
    print(word_string)## for testing in console
    replaced_string = word_string.replace('"', "")
    print(replaced_string)## for testing in console
    word_list= h.suggest(replaced_string)
    print(word_list)## for testing in console
    separator = ", "
    new_word_list= separator.join(word_list)
    transformed_string=new_word_list.replace(",","")
    data ={'output': transformed_string}
    print(data)## for testing in console
    return JsonResponse(data)
