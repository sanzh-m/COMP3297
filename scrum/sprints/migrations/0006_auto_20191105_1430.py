# Generated by Django 2.2.6 on 2019-11-05 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprints', '0005_auto_20191105_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('NS', 'Not Started'), ('DI', 'Development In Progress'), ('DD', 'Development Done'), ('TI', 'Testing In Process'), ('TD', 'Testing Done'), ('DO', 'Done')], default='NS', max_length=2, null=True),
        ),
    ]
