from django.contrib import admin

from .models import Author, Category, Post, About, Like, Dislike, Comment, Tag, Report

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(About)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Comment)
admin.site.register(Tag)

@admin.register(Post) 
class PostAdmin(admin.ModelAdmin): 
    list_display = ('title', 'author', 'timestamp') 
    prepopulated_fields = {'slug': ('title',)} 
    filter_horizontal = ('tags',) # Sağ-sol pəncərəsi ilə tag seçimi

@admin.register(Report) 
class ReportAdmin(admin.ModelAdmin): 
    list_display = ['post', 'reporter_name', 'reason', 'timestamp', 'is_resolved'] 
    list_filter = ['reason', 'is_resolved'] 
    search_fields = ['post__title', 'reporter_name']