# Generated by Django 4.0.4 on 2022-08-06 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0007_remove_rolepriv_mainmenu_rolepriv_mainmenu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rolepriv',
            name='mainmenu',
        ),
        migrations.AddField(
            model_name='rolepriv',
            name='mainmenu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mainmenus', to='Authentication.mainmenu'),
        ),
    ]
