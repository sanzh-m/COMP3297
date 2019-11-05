# Generated by Django 2.2.6 on 2019-11-05 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprints', '0004_auto_20191105_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('N', 'Not Started'), ('DI', 'Development In Progress'), ('DD', 'Development Done'), ('TI', 'Testing In Process'), ('TD', 'Testing Done'), ('D', 'Done')], default='N', max_length=2, null=True),
        ),
    ]