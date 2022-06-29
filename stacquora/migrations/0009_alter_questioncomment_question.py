# Generated by Django 4.0.5 on 2022-06-29 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stacquora', '0008_questioncomment_delete_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questioncomment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questioncomment', to='stacquora.question'),
        ),
    ]
