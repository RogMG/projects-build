from django.shortcuts import redirect, render
from django import forms
from django.urls import reverse
from . import util
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from markdown2 import Markdown
import random
import re
import markdown2

class CreateNewForm(forms.Form):
    title = forms.CharField(label="Choose a title for your entry", widget=forms.TextInput(attrs={'placeholder': 'Insert title....','class':'form-control mb-4'}))
    information = forms.CharField(label="Write the information", widget=forms.Textarea(attrs={'placeholder': 'Insert some information.....','class':'form-control mb-4 '}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def createPage(request):
    if request.method == "POST":
        form = CreateNewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            information = form.cleaned_data["information"]
            wikitext = "# "+title+"\n"+information
            if title in util.list_entries():
                return HttpResponse("Error, entry already in the wiki")
            else:
                util.save_entry(title, wikitext)
                return redirect(entry, title=title)
        else:
            return render(request, "encyclopedia/newPage.html",{
                "form": form
            })
    return render(request, "encyclopedia/newPage.html",{
        "form":CreateNewForm()
    })


def entry(request, title):
    notfound = "Entry not found"
    if util.get_entry(title) == None:
             return render(request, "encyclopedia/entry.html",{
                 "title": notfound
             })
    else:
        return render(request, "encyclopedia/entry.html",{
        "bartitle": title,
        "title": replace(util.get_entry(title))
        })
    
def replace(information):
    #md = Markdown().convert(information)
    #md = markdown2.markdown(information)
    md = markdown2.markdown(information, extras=["fenced-code-blocks","tables","footnotes","cuddled-lists","spoiler","strike","wiki-tables"])
    return md



def randomize(request):
    listr = util.list_entries()
    title = random.choice(listr)
    return redirect(entry,title=title)


def editpage(request, title):
    if request.method == "POST":
        info = request.POST.get('Information')
        util.save_entry(title, info)
        return redirect(entry, title=title)
    
    return render(request, "encyclopedia/edit.html",{   
            "title": title,
            "information": util.get_entry(title)
    }  )

def searchq(request):
    if request.method == "POST":
            query = request.POST.get('q')
            if util.get_entry(query) == None:
             listtr = [i for i in util.list_entries() if query in i] 
             return render(request, "encyclopedia/index.html", {
             "entries": listtr
             })
            else:
                return render(request, "encyclopedia/entry.html",{
                    "bartitle": query,
                    "title": replace(util.get_entry(query))
                })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })

 

    
