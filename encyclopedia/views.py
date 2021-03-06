import re
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    source = util.get_entry(title)
    if source==None:
        return render(request, "encyclopedia/entry.html",{
            "title": "Error",
            "content": "<h1>Error</h1>\n<p>Could not find the page you requested</p>\n"
        })

    p = re.compile(r'^(#+) (.+?)\s', re.MULTILINE)
    test = p.finditer(source)
    for item in test:
        if len(item.group(1))!=0:
            s = item.group(2)
            source = p.sub(f"<h{len(item.group(1))}>{s}</h{len(item.group(1))}>\n", source, 1)
   
    parPatren = re.compile(r'(^\w.*)(\s|\.)$', re.MULTILINE)
    source = parPatren.sub(r'<p>\g<1></p>\n', source)
    linkPattren = re.compile(r'\[(\w+?)\]\((.*?)\)')
    source = linkPattren.sub(r'<a href="\g<2>">\g<1></a>', source)
    listPattren = re.compile(r'^(\*|\+|\-)( .*)+(\r)$', re.MULTILINE)
    source = listPattren.sub(r'<li>\g<2></li>\n', source)
    ulpattren = re.compile(r'<li>.*</li>', re.DOTALL)
    source = ulpattren.sub(r'<ul>\n\g<0>\n</ul>', source)
    source = re.sub(r'\*\*(.*?)\*\*', r'<strong>\g<1></strong>', source)
    return render(request, "encyclopedia/entry.html",{
        "title": title.upper(),
        "content": source
    })

def search(request):
    #this method eccept POST only
    if request.method == 'POST':
        query = request.POST["q"]
        query = query.upper()
        listOfFiles = util.list_entries()
        print(listOfFiles)
        #searching for the exact name in the entery list
        if query in listOfFiles:
            return HttpResponseRedirect(reverse("entry", args=(query,)))
        #searching for the substring in the entery list and return the list that matches
        searchPattren = re.compile(query, re.IGNORECASE)
        resultList = []
        for item in listOfFiles:
            if searchPattren.search(item)!=None:
                resultList.append(item)
        #return the list of entries
        return render(request, "encyclopedia/search.html",{
                "title": "Search",
                "entries": resultList,
        })
        