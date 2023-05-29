# Generated by Django 4.2.1 on 2023-05-23 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_students_delete_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('release_date', models.DateTimeField(verbose_name='Realse Date')),
                ('blog_time', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Date')),
            ],
        ),
    ]
