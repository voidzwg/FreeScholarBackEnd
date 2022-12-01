# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Affiliation(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    fields = models.JSONField(blank=True, null=True)
    hot_index = models.IntegerField(blank=True, null=True)
    scholars = models.JSONField(blank=True, null=True)
    num_pubs_per_year = models.JSONField(blank=True, null=True)
    logo = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Affiliation'


class Collection(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('User', models.DO_NOTHING)
    paper_id = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Collection'


class Comment(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    paper_id = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Comment'


class Complainauthor(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    scholar = models.ForeignKey('Scholar', models.DO_NOTHING, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)
    audit_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ComplainAuthor'


class Complaincomment(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    report = models.ForeignKey('User', models.DO_NOTHING, related_name='report')
    reported = models.ForeignKey('User', models.DO_NOTHING, related_name='reported')
    comment = models.ForeignKey(Comment, models.DO_NOTHING)
    reason = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)
    audit_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ComplainComment'


class Complainpaper(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('Scholar', models.DO_NOTHING)
    paper_id = models.TextField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    audit_time = models.DateTimeField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ComplainPaper'


class Field(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    name = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Field'


class Follow(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    scholar = models.ForeignKey('Scholar', models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Follow'


class Keyword(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    name = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'KeyWord'


class Like1(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    comment = models.ForeignKey(Comment, models.DO_NOTHING, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Like1'


class Message(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    owner = models.ForeignKey('User', models.DO_NOTHING, related_name='owner')
    sender = models.ForeignKey('User', models.DO_NOTHING, related_name='sender')
    content = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    is_read = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Message'


class Notice(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('User', models.DO_NOTHING)
    sender_id = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Notice'


class Scholar(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('User', models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=True, null=True)
    affi = models.JSONField(blank=True, null=True)
    field = models.CharField(max_length=255, blank=True, null=True)
    hot_index = models.IntegerField(blank=True, null=True)
    claim_time = models.DateTimeField(blank=True, null=True)
    author_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Scholar'


class Scholarportal(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    scholar = models.ForeignKey(Scholar, models.DO_NOTHING)
    paper_show = models.JSONField(blank=True, null=True)
    bgp = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ScholarPortal'


class User(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    name = models.CharField(max_length=255, blank=True, null=True)
    pwd = models.CharField(max_length=255, blank=True, null=True)
    mail = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    identity = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    login_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'User'


class Viewhistory(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey(User, models.DO_NOTHING)
    paper_id = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ViewHistory'

