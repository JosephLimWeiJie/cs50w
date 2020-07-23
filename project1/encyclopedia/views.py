from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from django import forms
import markdown2

import random


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title of the entry:")
    content = forms.CharField(label="Content:")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    """
    Returns an entry view based on the title given by user. Redirects to
    an error page if title is not found in entries folder.
    """
    isFound = check_valid_entry(title)

    if isFound:
        return render(request, "encyclopedia/entry.html", {
            "title_of_website": title.capitalize(),
            "entry_content": markdown2.markdown(util.get_entry(title))
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error_message": "Sorry, the page you've requested is not found."
        })


def search(request):
    """
    Returns a particular entry view if the title of the entry matches the
    user's input completely. Shows a list of possible search results based
    on the user's input. Redirects to home page if all else fails.
    """
    if request.method == "GET":
        user_input = request.GET.get('q')
        isFound = check_valid_entry(user_input)

        if isFound:
            return render(request, "encyclopedia/entry.html", {
                "title_of_website": user_input.upper(),
                "entry_content": markdown2.markdown(util.get_entry(user_input))
            })
        else:
            substring_entry_list = get_substring_entry(user_input)
            return render(request, "encyclopedia/search.html", {
                "substring_entry_list": substring_entry_list
            })
    else:
        return index(request)


def newpage(request):
    """
    Returns a new entry. If an entry with a similar title exists, shows
    an error message indeed.
    """
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


def editpage(request, title):
    """
    Returns to an editing page to edit the title and content of an entry.
    Both title and content are pre-populated with existing Markdown content.
    """
    prev_content = util.get_entry(title)
    if request.method == "POST":
        edited_form = NewEntryForm(
            request.POST, initial={"title": title, "content": prev_content})
        if edited_form.is_valid():
            title = edited_form.cleaned_data["title"]
            content = edited_form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(
                reverse("encyclopedia:title", args=[title]))
    else:
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "form": NewEntryForm(
                initial={"title": title, "content": prev_content})
        })


def randompage(request):
    """
    Redirects user to a random entry page upon clicking.
    """
    random_title = random.choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        "title_of_website": random_title.capitalize(),
        "entry_content": markdown2.markdown(util.get_entry(random_title))
    })


""" Helper functions """


def check_valid_entry(input_to_be_checked):
    """
    Checks the current list of entries against the user's input.
    Returns True if the input matches the title of an entry and
    False if otherwise
    """
    isValid = False
    for entry in util.list_entries():
        if (input_to_be_checked.lower() == entry.lower()):
            isValid = True
            break
    return isValid


def get_substring_entry(input):
    """
    Checks the current list of entries against the user's input.
    Returns a list of possible substring combinations based on the
    input given.
    """
    substring_entry_list = []
    for entry in util.list_entries():
        if (input.lower() in entry.lower()):
            substring_entry_list.append(entry)
    return substring_entry_list
