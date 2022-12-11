# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Favorites(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    title = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Favorites'


class User(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    name = models.CharField(max_length=255, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    pwd = models.CharField(max_length=255, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    mail = models.CharField(max_length=255, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    avatar = models.CharField(max_length=255, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    identity = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    bio = models.CharField(max_length=255, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    login_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'
