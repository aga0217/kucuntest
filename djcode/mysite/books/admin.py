# -*- coding: utf-8 -*-
from django.contrib import admin
from books.models import Publisher,Author,Book ,testAuthor


# Register your models here.
class TestAuthorAdmin(admin.ModelAdmin):
    list_display =  ('name', 'email')

class AuthorAdmin(admin.ModelAdmin):
	list_display = ('first_name',  'last_name', 'email')
	search_fields = ('first_name', 'last_name')

class BookAdmin(admin.ModelAdmin):
	list_display = ('title','publisher', 'publication_date' ,)
	#list_fields = ('publication_date',)
    #fields = ('title', 'authors', 'publisher', 'publication_date')
	#filter_horizontal = ('authors',)
	filter_vertical = ('authors',)
	#raw_id_fields = ('publisher',)



admin.site.register(Publisher)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(testAuthor, TestAuthorAdmin)
