from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from . import util
from markdown2 import Markdown
from django.urls import reverse
from django.http import HttpResponseRedirect
markdowner = Markdown()
from random import randint
class NewTaskForm(forms.Form):
    task = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))
class NewTaskForm1(forms.Form):
    task1 = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    task2 = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Write Encyclopedia'}))
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": NewTaskForm()
    })

def create1(request):
    return render(request, "encyclopedia/index2.html", {
        "entries": util.list_entries(), "form": NewTaskForm(), "form1": NewTaskForm1()
    })
def create2(request, name1):
    ntf1=NewTaskForm1({'task1':name1, 'task2':util.get_entry(name1)})
    return render(request, "encyclopedia/index2.html", {
        "entries": util.list_entries(), "form": NewTaskForm(), "form1": ntf1
    })
def entry1(request, name1):
    f1=util.get_entry(name1)
    if(name1=='Random_Page'):
        f1=util.list_entries()[randint(0, len(util.list_entries())-1)]
        return HttpResponseRedirect(reverse("entry1", args=[f1]))
    if(f1!=None):
        # return HttpResponse(markdowner.convert(f1))
        return render(request, "encyclopedia/index3.html", {"title1": name1, "html_content": markdowner.convert(f1)})
    elif(f1==None):
        return render(request, "encyclopedia/index3.html", {"title1": name1, "html_content": markdowner.convert("requested page not found")})
    # return render(request, f"encyclopedia/{name1}.md", {
    #     "entries": util.list_entries()
    # })
def entry2(request):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewTaskForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            task = form.cleaned_data["task"]
    if task in util.list_entries():
        return HttpResponseRedirect(reverse("entry1", args=[task]))
    l1=[]
    for i in util.list_entries():
        if(task in i):
            l1.append(i)
    if(len(l1)>0):
        return render(request, "encyclopedia/index1.html", {
        "entries": l1, "form": NewTaskForm()})
    elif(len(l1)==0):
        return entry1(request, task)
    
def entry3(request):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewTaskForm1(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            task1 = form.cleaned_data["task1"]
            task2=form.cleaned_data["task2"]
            print(task2[2:len(task1)+2])
        if(task2[2:len(task1)+2] == task1):
            util.save_entry(task1, task2)
            return HttpResponseRedirect(reverse("entry1", args=[task1]))
        elif(task2[2:len(task1)+2] != task1):
            return HttpResponse("The content should have a heading that is same as the title. In other words, since the title of your page is "+ task1+", start you content with the markdown # "+task1)

