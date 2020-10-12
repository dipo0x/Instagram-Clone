from django.contrib import admin
from core.models import Journal, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# Register your models here.
class JournalAdmin(admin.ModelAdmin):

    list_display = ('Your_Post_Title', 'Country')

    prepopulated_fields = {'slug': ('Your_Post_Title',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Journal, JournalAdmin)


