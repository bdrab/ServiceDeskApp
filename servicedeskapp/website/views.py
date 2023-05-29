from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from incident.models import Incident, Message, Category, Group
from website.forms import IncidentForm


def index(request):
    context = {}

    return render(request, "website/index.html", context=context)


def create_incident(request):
    form = IncidentForm()
    if request.method == "POST":
        form = IncidentForm(request.POST)
        inc = form.save(commit=False)
        inc.owner = request.user
        group = Group.objects.all().filter(scope=inc.category).first()
        inc.assignment_group = group
        inc.save()
    return render(request, "website/create.html", {'form': form})


def account(request):
    user_tickets = Incident.objects.all().filter(owner=User.objects.get(username=request.user))
    context = {"tickets": user_tickets}
    return render(request, "website/account.html", context=context)


def user_logout(request):
    logout(request)
    return redirect("index")


def admin_panel(request):
    if request.user.is_authenticated:

        if "admin" not in list(request.user.profile.roles.values()):
            return redirect("index")

        user_tickets = Incident.objects.all().filter(assigned_to=User.objects.get(username=request.user))

        groups = Group.objects.all().filter(members=request.user)
        queue_tickets = Incident.objects.all().filter(assignment_group=groups[0])

        for group in groups[1:]:
            queue_tickets |= Incident.objects.all().filter(assignment_group=group)

        context = {"user_tickets": user_tickets,
                   "queue_tickets": queue_tickets}
        return render(request, "website/admin_panel.html", context=context)
    else:
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


def inc_details(request, inc_number):
    try:
        ticket = Incident.objects.get(number=inc_number)

    except Incident.DoesNotExist:
        return redirect('index')

    inc_messages = Message.objects.all().filter(incident=ticket).order_by('-created')

    context = {"ticket": ticket,
               "messages": inc_messages}

    print(ticket.assigned_to)
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return render(request, "website/task_guest.html", context=context)

    if "admin" in list(user.profile.roles.values()):
        return render(request, "website/task_admin.html", context=context)
    else:
        return render(request, "website/task_guest.html", context=context)


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

    return redirect("inc", inc_number=1685256960705431800)
