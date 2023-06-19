from django.shortcuts import HttpResponse, redirect
from .models import Tag, User, Incident, KnowledgeFiles, Category, KnowledgeArticle, Attachment, Message, Group
from website.forms import IncidentForm
import json


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


def add_attachment(request):
    if request.user.is_authenticated:
        incident_number = request.POST.get("incident")
        inc = Incident.objects.get(number=incident_number)
        for file in request.FILES.getlist("file"):
            if file.size <= 4194304:
                try:
                    if "." in str(file.name):
                        name, extension = str(file.name).split(".")
                    else:
                        name = file.name
                        extension = ""

                    if len(name) >= 10:
                        name = name[:10]
                    else:
                        name = name

                    attachment = Attachment(name=name, extension=extension, incident=inc, file=file)
                    attachment.save()
                except Exception as e:
                    print(e)
                    return HttpResponse("NOT OK")
    return HttpResponse("ALL OK")


def create_note(request):
    if request.user.is_authenticated:
        author = User.objects.get(username=request.user.username)
        if request.method == "POST":
            try:
                incident_number = request.POST.get('inc-number')
                content = request.POST.get('content')
                incident = Incident.objects.get(number=incident_number)

                new_incident = Message(author=author, incident=incident, content=content)
                new_incident.save()

            except Incident.DoesNotExist:
                return HttpResponse("Error has occurred.")

            return HttpResponse("New message has been created")

    return redirect("index")


def create_incident(request):
    if request.user.is_authenticated:
        form = IncidentForm()
        if request.method == "POST":

            category = request.POST.get('category')
            category = Category.objects.get(pk=category)
            description = request.POST.get('description')
            group = Group.objects.all().filter(scope=category).first()

            inc = Incident(owner=request.user, category=category, description=description, assignment_group=group)
            inc.save()
            response = json.dumps({"status": "ok",
                                   "number": inc.number})

            for file in request.FILES.getlist("file"):
                if file.size <= 4194304:
                    try:
                        if "." in str(file.name):
                            name, extension = str(file.name).split(".")
                        else:
                            name = file.name
                            extension = ""

                        if len(name) >= 10:
                            name = name[:10]
                        else:
                            name = name

                        attachment = Attachment(name=name, extension=extension, incident=inc, file=file)
                        attachment.save()
                    except Exception as e:
                        print(e)
                        response = json.dumps({"status": "failed",
                                               "number": "N/A"})
                        return HttpResponse(response, content_type="application/json")
            return HttpResponse(response, content_type="application/json")
    response = json.dumps({"status": "failed",
                           "number": "N/A"})
    return HttpResponse(response, content_type="application/json")


def update_note(request, incident_number, **kwargs):
    if request.user.is_authenticated:
        author = User.objects.get(username=request.user.username)

        incident = Incident.objects.get(number=incident_number)
        incident_fields = [e.name for e in incident._meta.fields]
        for kwarg in kwargs.items():
            if kwarg[0] in incident_fields:
                content = f"Field '{kwarg[0]}' has been set to '{kwarg[1]}' by '{author}'"
                new_message = Message(author=author, incident=incident, content=content)
                new_message.save()


def start_work(request, inc_number):
    incident = Incident.objects.get(number=inc_number)
    incident.assigned_to = request.user
    update_note(request, inc_number, assigned_to=request.user)
    incident.save()
    return HttpResponse("Inc has been assigned to engineer.")


def resolve_inc(request, inc_number):
    incident = Incident.objects.get(number=inc_number)
    if request.user.username == incident.assigned_to.username:
        if incident.state:
            if not incident.knowledge_article.all():
                response = json.dumps({"status": "failed",
                                       "details": "knowledge article not added"})
                return HttpResponse(response, content_type="application/json")

        incident.state = not incident.state
        update_note(request, inc_number, state=incident.state)
        incident.save()

    response = json.dumps({"status": "ok",
                           "details": "ok"})
    return HttpResponse(response, content_type="application/json")
