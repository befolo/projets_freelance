# Generated by Django 4.2.11 on 2024-04-21 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projet', '0002_remove_projet_coordonnee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projet',
            name='descrip_reduit',
            field=models.CharField(max_length=350, null=True),
        ),
    ]
