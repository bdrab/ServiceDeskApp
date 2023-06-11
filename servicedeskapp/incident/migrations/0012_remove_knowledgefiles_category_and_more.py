# Generated by Django 4.2.1 on 2023-06-09 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0011_incident_knowledge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knowledgefiles',
            name='category',
        ),
        migrations.RemoveField(
            model_name='knowledgefiles',
            name='tag',
        ),
        migrations.AddField(
            model_name='knowledgefiles',
            name='category',
            field=models.ManyToManyField(blank=True, default=None, to='incident.category'),
        ),
        migrations.AddField(
            model_name='knowledgefiles',
            name='tag',
            field=models.ManyToManyField(blank=True, default=None, to='incident.tag'),
        ),
    ]
