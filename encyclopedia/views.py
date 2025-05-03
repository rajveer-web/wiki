from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from django.urls import reverse
import random
import markdown2
from . import util




def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def entry(request, title):
    entry_content = util.get_entry(title)
    
    if entry_content:
        # Convert Markdown to HTML
        entry_content_html = markdown2.markdown(entry_content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": entry_content_html
        })
    else:
        return HttpResponseNotFound("Page not found")

def search(request):
    query = request.GET.get("q", "").lower()
    entries = util.list_entries()
    matching_entries = [entry for entry in entries if query in entry.lower()]
    
    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "matching_entries": matching_entries
    })


def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        
        # Check if the entry already exists
        if util.get_entry(title):
            return HttpResponseBadRequest("An entry with that title already exists.")
        
        # Save the new entry
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/create.html")



def edit(request, title):
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect("entry", title=title)

    content = util.get_entry(title)
    if content is None:
        return HttpResponseNotFound("Page not found")

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })


def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect("entry", title=random_entry)

