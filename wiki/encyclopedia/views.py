from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django import forms
import random

# create class for sidebar search form, inherits from the Form class in django forms
class FormSearch(forms.Form):
    search = forms.CharField(label="search", widget=forms.TextInput(attrs={"placeholder": "query.."}))

# create class for new entry
class CreateEntry(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(
        attrs={"placeholder": "title"}))
    textarea = forms.CharField(label="", widget=forms.Textarea(
        attrs={"placeholder": "markdown"}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

# index page receives current list entries as data and the django form
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchform": FormSearch()
    })


# function to get html for page by its title
def html(title):
    markdowner = Markdown()
    md = util.get_entry(title)
    html = markdowner.convert(md)

    return html


# renders the wiki entry page
def entry(request, title):
    md = util.get_entry(title)
    # show error page if no entry page
    if not md:
        return render(request, "encyclopedia/entry_does_not_exist.html", {
            "title": title,
            "searchform": FormSearch()
        })
    # render the entry page
    else:
        return render(request, "encyclopedia/entry.html", {
            # pass through context to entry page
            "searchform": FormSearch(),
            "entry": html(title),
            "title": title

        })

# wiki page search
def search(request):
    if request.method == 'GET':   #when the page is reached through GET request show null values
        return render(request, "encyclopedia/search.html", {
            "searchform": FormSearch(),          
            "outcomes": "",
            "search": ""
        })
    else: #the user requested the page by submitted the search form 
        input = FormSearch(request.POST) #get form data by binding the data from the request to our form
        total_entries = util.list_entries() #list of all of the entries currentlyon the website 
        search_matches = []   # initiate list of substring matching entries for the search to use later
        #form validation
        if input.is_valid():
            search_term = input.cleaned_data["search"]   #get search term
            #check for matches and redirect to page
            for title in total_entries:
                if search_term.upper() == title.upper():
                    return HttpResponseRedirect(reverse("entry", args=[title]))
                # display the sub-string matches
                if search_term.upper() in title.upper():
                    search_matches.append(title)
            #render list of substring matches to user
            return render(request, "encyclopedia/search.html", {
                "substrings": search_matches,
                "searchform": FormSearch()
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "searchform": input
            })
        


#create wiki page
def create(request):
    if request.method == "GET":     # if user navigated to the page
        return render(request, "encyclopedia/create.html", {    #render create page
            "searchform": FormSearch(),
            "entryform": CreateEntry()
        })
    else:
        input = CreateEntry(request.POST) # get form data
        if input.is_valid():    # validate form data    
            title = input.cleaned_data["title"] # get title
            textarea = input.cleaned_data["textarea"] # get text area
            if util.get_entry(title) is None or input.cleaned_data['edit'] is True:
                util.save_entry(title, textarea)
                return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
            else:
                return render(request, "encyclopedia/create.html", {
                    "searchform": FormSearch(),
                    "entryform": CreateEntry(),
                    "except": "Title already exists!"
                })
        else:
            return render(request, "encyclopedia/create.html", {
            "searchform": FormSearch(),
            "entryform": CreateEntry()

            })


# render random entry
def random_page(request):
    total_entries = util.list_entries()
    random_title = random.choice(total_entries)
    return HttpResponseRedirect(reverse("entry", args=[random_title])) # redirect user to page


# edit exisiting entry page
def edit(request, title):
    page = util.get_entry(title)
    form = CreateEntry()
    form.fields["title"].initial = title
    form.fields["title"].widget = forms.HiddenInput()
    form.fields["textarea"].initial = page
    form.fields["edit"].initial = True
    return render(request, "encyclopedia/create.html", {
        "entryform": form,
        "edit": form.fields["edit"]
    })



        
            















