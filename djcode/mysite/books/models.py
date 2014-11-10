# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __unicode__(self):
        return self.name

class testAuthor(models.Model):
    name = models.CharField(max_length=30,verbose_name=u'作者姓名')
    email = models.EmailField(blank='Ture')
    def __unicode__(self):
        return self.name



class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(blank='Ture')
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
        #return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    #authors = models.ManyToManyField(Author)
    authors = models.ManyToManyField(testAuthor)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()

    def __unicode__(self):
        return self.title


