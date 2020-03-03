# Generated by Django 3.0.3 on 2020-03-03 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0002_auto_20200302_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maze',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Default Title', max_length=127)),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='east_connection',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='north_connection',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='south_connection',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='west_connection',
            field=models.BooleanField(default=False),
        ),
    ]