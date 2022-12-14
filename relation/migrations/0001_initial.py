# Generated by Django 4.0.3 on 2022-12-10 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliation',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('fields', models.JSONField(blank=True, null=True)),
                ('hot_index', models.IntegerField(blank=True, null=True)),
                ('scholars', models.JSONField(blank=True, null=True)),
                ('num_pubs_per_year', models.JSONField(blank=True, null=True)),
                ('logo', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Affiliation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('paper_id', models.TextField(blank=True, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Collection',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('paper_id', models.TextField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Complainauthor',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('reason', models.TextField(blank=True, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('reply', models.TextField(blank=True, null=True)),
                ('audit_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ComplainAuthor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Complaincomment',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('reason', models.TextField(blank=True, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('reply', models.TextField(blank=True, null=True)),
                ('audit_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ComplainComment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Complainpaper',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('paper_id', models.TextField(blank=True, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('audit_time', models.DateTimeField(blank=True, null=True)),
                ('reply', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ComplainPaper',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Field',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Follow',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('update_time', models.DateTimeField(blank=True, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'KeyWord',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Like1',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Like1',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('is_read', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Message',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('sender_id', models.IntegerField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Notice',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Scholar',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('affi', models.JSONField(blank=True, null=True)),
                ('field', models.CharField(blank=True, max_length=255, null=True)),
                ('hot_index', models.IntegerField(blank=True, null=True)),
                ('claim_time', models.DateTimeField(blank=True, null=True)),
                ('author_id', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Scholar',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Scholarportal',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('paper_show', models.JSONField(blank=True, null=True)),
                ('bgp', models.CharField(blank=True, max_length=255, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ScholarPortal',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('pwd', models.CharField(blank=True, max_length=255, null=True)),
                ('mail', models.CharField(blank=True, max_length=255, null=True)),
                ('avatar', models.CharField(blank=True, max_length=255, null=True)),
                ('identity', models.IntegerField(blank=True, null=True)),
                ('state', models.IntegerField(blank=True, null=True)),
                ('gender', models.IntegerField(blank=True, null=True)),
                ('bio', models.CharField(blank=True, max_length=255, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('login_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'User',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Viewhistory',
            fields=[
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
                ('paper_id', models.TextField(blank=True, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ViewHistory',
                'managed': False,
            },
        ),
    ]
