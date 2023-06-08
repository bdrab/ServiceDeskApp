from django.shortcuts import render, HttpResponse, redirect
from .models import Tag, User, Incident, KnowledgeFiles, Category
import json


def tags(request, tag):
    tag = Tag.objects.get(name=tag)
    incs = Incident.objects.filter(tags=tag)
    files = KnowledgeFiles.objects.filter(tag=tag)

    incs = [{"number": inc.number,
             "description": inc.description} for inc in incs]

    files = [{"name": file.name,
              "extension": file.extension,
              "path": str(file.file)} for file in files]

    data = json.dumps({"tickets": incs,
                       "files": files})

    return HttpResponse(data, content_type="application/json")


def categories(request, category):
    category_instance = Category.objects.get(name=category)
    incs = Incident.objects.filter(category=category_instance)
    files = KnowledgeFiles.objects.filter(category=category_instance)

    incs = [{"number": inc.number,
             "description": inc.description} for inc in incs]

    files = [{"name": file.name,
              "extension": file.extension,
              "path": str(file.file)} for file in files]

    data = json.dumps({"tickets": incs,
                       "files": files})

    return HttpResponse(data, content_type="application/json")


def create_tag(request):
    if request.method != "POST":
        return redirect("index")
    else:
        tag_name = request.POST.get('tag-name')
        inc_number = request.POST.get('inc-number')

        try:
            new_tag = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            new_tag = Tag.objects.create(name=tag_name)

        inc = Incident.objects.get(number=inc_number)
        inc.tags.add(new_tag)
        return redirect("index")
