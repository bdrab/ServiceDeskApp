from django.shortcuts import render, HttpResponse, redirect
from incident.models import Tag, User, Incident, KnowledgeFiles, Category, KnowledgeArticle
from .models import Notification
import json
import random


def create_knowledge_article(request):

    all_notifications = Notification.objects.all()

    data = json.dumps({"status": "ok"})

    return HttpResponse(data, content_type="application/json")
