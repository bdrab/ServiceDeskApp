# Generated by Django 4.2.1 on 2023-06-18 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0017_incident_knowledge_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, default=None, max_length=12, null=True),
        ),
    ]