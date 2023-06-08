# Generated by Django 4.2.1 on 2023-06-08 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0008_knowledgefiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='knowledgefiles',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='incident.tag'),
        ),
    ]
