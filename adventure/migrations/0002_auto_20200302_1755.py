# Generated by Django 3.0.3 on 2020-03-02 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='e_to',
            new_name='maze',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='n_to',
            new_name='x',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='s_to',
            new_name='y',
        ),
        migrations.RemoveField(
            model_name='room',
            name='description',
        ),
        migrations.RemoveField(
            model_name='room',
            name='title',
        ),
        migrations.RemoveField(
            model_name='room',
            name='w_to',
        ),
    ]
