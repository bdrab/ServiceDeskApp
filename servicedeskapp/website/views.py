import json

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from incident.models import Incident, Message, Group, Attachment, Category, Tag, KnowledgeFiles, KnowledgeArticle
from website.forms import IncidentForm
from django.core import serializers
from django.db.models import Q
from django.http import FileResponse


def index(request):
    if not request.user.is_authenticated:
        context = {}
        return render(request, "website/index.html", context=context)
    else:
        tickets = Incident.objects.all()
        user_tickets = tickets.filter(owner=User.objects.get(username=request.user))

        if "admin" not in list(request.user.profile.roles.values()):
            context = {"tickets": user_tickets}
            return render(request, "website/account.html", context=context)

        else:
            user_assigned_to_tickets = Incident.objects.all().filter(assigned_to=User.objects.get(username=request.user)).filter(~Q(state=False))
            user_assigned_to_tickets_closed = Incident.objects.all().filter(assigned_to=User.objects.get(username=request.user)).filter(~Q(state=True))

            groups = Group.objects.all().filter(members=request.user)
            queue_tickets_not_assigned = Incident.objects.all().filter(assignment_group=groups[0]).filter(assigned_to=None)
            queue_tickets_assigned = Incident.objects.all().filter(assignment_group=groups[0]).filter(assigned_to=not None)
            queue = serializers.serialize("json", queue_tickets_not_assigned)

            for group in groups[1:]:
                queue_tickets_not_assigned |= Incident.objects.all().filter(assignment_group=group).filter(assigned_to=None)
                queue_tickets_assigned |= Incident.objects.all().filter(assignment_group=group).filter(assigned_to=not None)

            context = {"user_assigned_to_tickets": user_assigned_to_tickets,
                       "queue_tickets": queue_tickets_not_assigned,
                       "queue_tickets_assigned": queue_tickets_assigned,
                       "queue_tickets_closed": user_assigned_to_tickets_closed,
                       "queue": queue,
                       "tickets": tickets}
            return render(request, "website/admin_panel.html", context=context)


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
    articles = KnowledgeArticle.objects.all()
    inc_articles = ticket.knowledge_article.all()
    context = {"ticket": ticket,
               "tags": tags,
               "messages": inc_messages,
               "attachments": attachments,
               "knowledge_articles": articles,
               "inc_knowledge_articles": inc_articles}
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


def knowledge(request):
    tags = Tag.objects.all()
    categories = Category.objects.all()
    articles = [{"name": article.name,
                 "pk": article.pk} for article in KnowledgeArticle.objects.all()]
    context = {"tags": tags,
               "categories": categories,
               "articles": articles}
    return render(request, "website/knowledge.html", context=context)
