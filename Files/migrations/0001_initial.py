# Generated by Django 4.0.3 on 2022-12-12 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
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
        migrations.CreateModel(
            name='User',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_collation='utf8mb4_0900_ai_ci', max_length=255, null=True)),
                ('pwd', models.CharField(blank=True, db_collation='utf8mb4_0900_ai_ci', max_length=255, null=True)),
                ('mail', models.CharField(blank=True, db_collation='utf8mb4_0900_ai_ci', max_length=255, null=True)),
                ('avatar', models.CharField(blank=True, db_collation='utf8mb4_0900_ai_ci', max_length=255, null=True)),
                ('identity', models.IntegerField(blank=True, null=True)),
                ('state', models.IntegerField(blank=True, null=True)),
                ('gender', models.IntegerField(blank=True, null=True)),
                ('bio', models.CharField(blank=True, db_collation='utf8mb4_0900_ai_ci', max_length=255, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('login_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'User',
                'managed': False,
            },
        ),
    ]
