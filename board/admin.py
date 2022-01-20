from django.contrib import admin
from  .models import Board,Topic,Post


class PostInline(admin.TabularInline):
    model = Post
    extra = 3


class BoardAdmin(admin.ModelAdmin):
    fieldsets = [
        ('论坛名字', {'fields': ['name']}),
        ('描述', {'fields': ['description']}),
    ]
    list_display = ('name', 'description')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('board','subject', 'starter','last_updated')
    inlines = [PostInline]


admin.site.register(Board,BoardAdmin)
admin.site.register(Topic,TopicAdmin)