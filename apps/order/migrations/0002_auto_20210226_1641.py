# Generated by Django 3.1.5 on 2021-02-26 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='frist_name',
            new_name='first_name',
        ),
    ]
