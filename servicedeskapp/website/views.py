import json

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from incident.models import Incident, Message, Group, Attachment, Category, Tag, KnowledgeFiles
from website.forms import IncidentForm
from django.core import serializers
from django.db.models import Q
from django.http import FileResponse


def index(request):
    if not request.user.is_authenticated:
        context = {}
        return render(request, "website/index.html", context=context)
    else:
        user_tickets = Incident.objects.all().filter(owner=User.objects.get(username=request.user))

        if "admin" not in list(request.user.profile.roles.values()):
            context = {"tickets": user_tickets}
            return render(request, "website/account.html", context=context)

        else:
            user_assigned_to_tickets = Incident.objects.all().filter(assigned_to=User.objects.get(username=request.user)).filter(~Q(state=False))
            user_assigned_to_tickets_closed = Incident.objects.all().filter(assigned_to=User.objects.get(username=request.user)).filter(~Q(state=True))

            groups = Group.objects.all().filter(members=request.user)
            queue_tickets = Incident.objects.all().filter(assignment_group=groups[0]).filter(assigned_to=None)
            queue = serializers.serialize("json", queue_tickets)

            for group in groups[1:]:
                queue_tickets |= Incident.objects.all().filter(assignment_group=group).filter(assigned_to=None)

            context = {"user_assigned_to_tickets": user_assigned_to_tickets,
                       "queue_tickets": queue_tickets,
                       "queue_tickets_closed": user_assigned_to_tickets_closed,
                       "queue": queue}
            return render(request, "website/admin_panel.html", context=context)


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


def user_logout(request):
    logout(request)
    return redirect("index")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        messages.error(request, 'Incorrect password.')
        return redirect('login')

    context = {}

    return render(request, "website/login.html", context=context)


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

        return render(request, "website/create.html", {'form': form})
    else:
        return redirect("index")


def inc_details(request, inc_number):
    try:
        ticket = Incident.objects.get(number=inc_number)

    except Incident.DoesNotExist:
        return redirect('index')

    inc_messages = Message.objects.all().filter(incident=ticket).order_by('-created')
    attachments = Attachment.objects.all().filter(incident=ticket)
    tags = ticket.tags.all()

    files = []
    if tags:
        files = KnowledgeFiles.objects.all().filter(tag=tags[0])

        for tag in tags[1:]:
            files |= KnowledgeFiles.objects.all().filter(tag=tag)

    context = {"ticket": ticket,
               "tags": tags,
               "knowledge_files": files,
               "messages": inc_messages,
               "attachments": attachments}
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return render(request, "website/task_guest.html", context=context)

    if "admin" in list(user.profile.roles.values()):
        return render(request, "website/task_admin.html", context=context)
    else:
        return render(request, "website/task_guest.html", context=context)


def view_attachment(request, attachment_name):
    file = Attachment.objects.get(file="files/inc_attachments/" + attachment_name)
    return FileResponse(file.file.open(), as_attachment=True)


def view_knowledge_file(request, knowledge_file_name):
    file = KnowledgeFiles.objects.get(file="files/knowledge_files/" + knowledge_file_name)
    return FileResponse(file.file.open(), as_attachment=True)


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
        incident.state = not incident.state
        update_note(request, inc_number, state=incident.state)
        incident.save()
    return HttpResponse("Ticket successfully closed")


def knowledge(request):
    tags = Tag.objects.all()
    categories = Category.objects.all()
    context = {"tags": tags,
               "categories": categories}
    return render(request, "website/knowledge.html", context=context)
