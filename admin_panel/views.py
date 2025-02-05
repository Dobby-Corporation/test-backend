from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.files.uploadedfile import InMemoryUploadedFile

from .forms import CreateTestForm, EditTestForm
from testings.models import Test
from testings.services import make_version_from_json

def index(request):
    test_list = Test.objects.all().order_by('-id')
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

def edit_test(request, id: int):
    test = Test.objects.get(pk=id)
    if request.method == "POST":
        form = EditTestForm(request.POST, request.FILES)
        if form.is_valid():
            test.name = form.cleaned_data['name']
            test.description = form.cleaned_data['description']

            json_file: InMemoryUploadedFile = form.cleaned_data['json_file']
            if json_file is not None:
                json_data = json_file.read().decode('utf-8')
                make_version_from_json(json_data, test)

            test.save()

            return redirect("admin-panel.index")
    else:
        form = EditTestForm({
            "name": test.name,
            "description": test.description,
        })

    return render(request, "admin-panel/edit-test.html", {
        "form": form
    })
