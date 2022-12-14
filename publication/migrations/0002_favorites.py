# Generated by Django 4.0.3 on 2022-12-10 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('field_id', models.IntegerField(db_column='_id', primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('avatar', models.CharField(blank=True, max_length=255, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Favorites',
                'managed': False,
            },
        ),
    ]
