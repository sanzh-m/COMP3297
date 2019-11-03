# Generated by Django 2.2.6 on 2019-11-02 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBacklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SprintBacklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline', models.TimeField()),
                ('status', models.CharField(max_length=50)),
                ('duration', models.CharField(max_length=50)),
                ('pb_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.ProductBacklog')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('effort', models.IntegerField()),
                ('title', models.CharField(max_length=50)),
                ('pb_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.ProductBacklog')),
                ('sprint_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.SprintBacklog')),
            ],
        ),
        migrations.CreateModel(
            name='ProductBacklogItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('size', models.IntegerField()),
                ('status', models.CharField(max_length=50)),
                ('pb_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.ProductBacklog')),
                ('sprint_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pages.SprintBacklog')),
            ],
        ),
    ]
