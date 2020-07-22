from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from django import forms


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title of the entry:")
    content = forms.CharField(label="Content:")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    isFound = check_valid_entry(title)

    if isFound:
        return render(request, "encyclopedia/entry.html", {
            "title_of_website": title.capitalize(),
            "entry_content": util.get_entry(title)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error_message": "Sorry, the page you've requested is not found."
        })


def search(request):
    if request.method == "GET":
        user_input = request.GET.get('q')
        isFound = check_valid_entry(user_input)

        if isFound:
            return render(request, "encyclopedia/entry.html", {
                "title_of_website": user_input.upper(),
                "entry_content": util.get_entry(user_input)
            })
        else:
            substring_entry_list = get_substring_entry(user_input)
            return render(request, "encyclopedia/search.html", {
                "substring_entry_list": substring_entry_list
            })
    else:
        return index(request)


def newpage(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if (check_valid_entry(title)):
                return render(request, "encyclopedia/error.html", {
                    "error_message":
                        "Sorry, you cannot create an existing entry."
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(
                    reverse("encyclopedia:title", args=[title]))
    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": NewEntryForm()
        })


""" Helper functions """


def check_valid_entry(input_to_be_checked):
    isValid = False
    for entry in util.list_entries():
        if (input_to_be_checked.lower() == entry.lower()):
            isValid = True
            break
    return isValid


def get_substring_entry(input):
    substring_entry_list = []
    for entry in util.list_entries():
        if (input.lower() in entry.lower()):
            substring_entry_list.append(entry)
    return substring_entry_list
