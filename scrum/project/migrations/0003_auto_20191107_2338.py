# Generated by Django 2.2.6 on 2019-11-07 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20191107_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='developer',
            name='productOwner',
        ),
        migrations.AddField(
            model_name='developer',
            name='projectIndex',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddConstraint(
            model_name='developer',
            constraint=models.UniqueConstraint(fields=('project', 'projectIndex'), name='unique_project_developer'),
        ),
    ]