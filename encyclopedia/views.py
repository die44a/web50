from django.shortcuts import render, redirect
from django import forms
from . import util
import markdown
import random


# Form for creating new pages
class NewCreateForm(forms.Form):
    title = forms.CharField(label="Your new page title")
    text = forms.CharField(label= "Create new page using standart Markdown syntax", widget=forms.Textarea(attrs={'class': 'createpage', 'placeholder': 'Enter page text here...'})) 

# Load main page
def index(request): 
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Load entry page
def entry(request, name):
    return render(request, "encyclopedia/entry.html", {
        "name": name.capitalize(),
        "text": markdown.markdown(util.get_entry(name))
    })

# Choose random page
def randompage(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)  # Pick a random entry
    return render(request, "encyclopedia/entry.html", {
        "name": random_entry.capitalize(),
        "text": markdown.markdown(util.get_entry(random_entry))
    })

# Create new page in wiki
def create(request):
    if request.method == "POST":
        form = NewCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            if title not in util.list_entries():
                util.save_entry(title, text)
            else:
                return render(request, "encyclopedia/alreadyexists.html")
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    
    return render(request, "encyclopedia/create.html",  {
        "form": NewCreateForm()
    })

# Search Encyclopedia
def search(request):
    prompt = request.POST.get("prompt")
    entries = []
    
    for entry in util.list_entries():
        
        if prompt.lower() == entry.lower():
            return redirect('entry', name=prompt)
        
        elif prompt.lower() in entry.lower():
            entries.append(entry)
    
    return render(request, "encyclopedia/search.html", {
        "entries": entries
    })
    
    