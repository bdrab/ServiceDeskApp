# Generated by Django 4.2.1 on 2023-05-29 15:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('incident', '0002_alter_incident_assigned_to_alter_incident_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='number',
            field=models.IntegerField(default=1685374254807121700),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('scope', models.ManyToManyField(to='incident.category')),
            ],
        ),
    ]
