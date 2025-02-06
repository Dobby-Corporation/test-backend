from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.files.uploadedfile import InMemoryUploadedFile

from .forms import CreateTestForm
from testings.models import Test
from testings.services import make_version_from_json

def index(request):
    test_list = Test.objects.all()
    paginator = Paginator(test_list, 10) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # return render(request, "list.html", {"page_obj": page_obj})

    return render(request, "admin-panel/index.html", {"page_obj": page_obj})

def create_test(request):
    if request.method == "POST":
        form = CreateTestForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            test = Test(name=name, description=description)
            test.save()

            json_file: InMemoryUploadedFile = form.cleaned_data['json_file']
            json_data = json_file.read().decode('utf-8')
            make_version_from_json(json_data, test)

            # test_version.test = test
            
            return redirect("admin-panel.index")
    else:
        form = CreateTestForm()

    return render(request, "admin-panel/create-test.html", {
        "form": form
    })

def create_test(request):
    if request.method == "POST":
        form = CreateTestForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            test = Test(name=name, description=description)
            test.save()

            json_file: InMemoryUploadedFile = form.cleaned_data['json_file']
            json_data = json_file.read().decode('utf-8')
            make_version_from_json(json_data, test)

            # test_version.test = test
            
            return redirect("admin-panel.index")
    else:
        form = CreateTestForm()

    return render(request, "admin-panel/create-test.html", {
        "form": form
    })
