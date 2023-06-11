from django.shortcuts import render, HttpResponse, redirect
from .models import Tag, User, Incident, KnowledgeFiles, Category, KnowledgeArticle
import json, random


def tags(request, tag):
    tag = Tag.objects.get(name=tag)
    incs = Incident.objects.filter(tags=tag)
    articles = KnowledgeArticle.objects.none()
    for inc in incs:
        articles |= KnowledgeArticle.objects.filter(incident=inc)

    files = KnowledgeFiles.objects.none()
    for article in articles:
        files |= article.knowledge_files.all()

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

    articles = KnowledgeArticle.objects.none()
    for inc in incs:
        articles |= KnowledgeArticle.objects.filter(incident=inc)

    files = KnowledgeFiles.objects.none()
    for article in articles:
        files |= article.knowledge_files.all()

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


def create_knowledge_article(request):
    knowledge_files = []
    if request.method == "POST":
        article_name = request.POST.get('name')
        inc_number = request.POST.get('inc-number')
        description = request.POST.get('description')
        for file in request.FILES.getlist("file"):
            if file.size <= 4194304:
                if "." in str(file.name):
                    name, extension = str(file.name).split(".")
                else:
                    name = file.name
                    extension = ""

                if len(name) >= 10:
                    name = name[:10]
                else:
                    name = name
                knowledge_file = KnowledgeFiles(name=name, extension=extension, file=file)
                knowledge_file.save()
                knowledge_files.append(knowledge_file)

    inc = Incident.objects.get(number=inc_number)

    new_knowledge_article = KnowledgeArticle.objects.create(name=article_name, description=description)
    new_knowledge_article.knowledge_files.set(knowledge_files)
    new_knowledge_article.save()
    inc.knowledge_article.set([*inc.knowledge_article.all(), new_knowledge_article])
    inc.save()

    data = json.dumps({"status": "ok"})
    return HttpResponse(data, content_type="application/json")
