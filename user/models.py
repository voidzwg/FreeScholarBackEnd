# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import re


class Affiliation(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    fields = models.JSONField(blank=True, null=True)
    hot_index = models.IntegerField(blank=True, null=True)
    scholars = models.JSONField(blank=True, null=True)
    num_pubs_per_year = models.JSONField(blank=True, null=True)
    logo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Affiliation'


class Collection(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('User', models.DO_NOTHING)
    paper_id = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Collection'


class Comment(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    paper_id = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Comment'


class Complainauthor(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    scholar = models.ForeignKey('Scholar', models.DO_NOTHING, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)
    audit_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ComplainAuthor'


class Complaincomment(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    report = models.ForeignKey('User', models.DO_NOTHING, related_name='report')
    reported = models.ForeignKey('User', models.DO_NOTHING, related_name='reported')
    comment = models.ForeignKey(Comment, models.DO_NOTHING)
    reason = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)
    audit_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ComplainComment'


class Complainpaper(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('Scholar', models.DO_NOTHING)
    paper_id = models.TextField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    audit_time = models.DateTimeField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ComplainPaper'


class Field(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    name = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Field'


class Follow(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    scholar = models.ForeignKey('Scholar', models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Follow'


class Keyword(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    name = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'KeyWord'


class Like1(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    comment = models.ForeignKey(Comment, models.DO_NOTHING, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Like1'


class Message(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    owner = models.ForeignKey('User', models.DO_NOTHING, related_name='owner')
    sender = models.ForeignKey('User', models.DO_NOTHING, related_name='sender')
    content = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    is_read = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Message'


class Notice(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('User', models.DO_NOTHING)
    sender_id = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Notice'


class Scholar(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey('User', models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=True, null=True)
    affi = models.JSONField(blank=True, null=True)
    field = models.CharField(max_length=255, blank=True, null=True)
    hot_index = models.IntegerField(blank=True, null=True)
    claim_time = models.DateTimeField(blank=True, null=True)
    author_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Scholar'


class Scholarportal(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    scholar = models.ForeignKey(Scholar, models.DO_NOTHING)
    paper_show = models.JSONField(blank=True, null=True)
    bgp = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ScholarPortal'


class User(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
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

    def validate_username(self):
        if type(self.name) is not str:
            return False
        if re.search(r"\s", self.name):
            return False
        return True

    def validate_password(self):
        if type(self.pwd) is not str:
            return False
        password = self.pwd.encode('utf8')
        if password.isdigit():
            return False
        if password.isalpha() and password.islower():
            return False
        if password.isalpha() and password.isupper():
            return False
        if password.isalpha() or password.isalnum():
            return True
        return False

    def validate_email(self):
        if type(self.mail) is not str:
            return False
        if re.match("^.+@(\\[?)[a-zA-Z0-9\\-.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", self.mail) is not None:
            return True
        else:
            return False

    class Meta:
        managed = False
        db_table = 'User'


class Viewhistory(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    user = models.ForeignKey(User, models.DO_NOTHING)
    paper_id = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ViewHistory'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
