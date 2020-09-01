from django.contrib import admin
from .models import Directory, ItemDirectory, DirectoryVersion


class ItemDirectoryAdmin(admin.ModelAdmin):
    list_display = ['dir', 'code', 'value', 'version']  #какие поля показывать в админке
    list_filter = ['dir', 'version']                    #по каким полям фильтровать
    search_fields = ['code', 'value', 'version']           #по каким полям проводить поиск
    fields = ['dir', ('code', 'value')]      #какие поля редактировать (в кортеже поля на одной строке)
    list_per_page = 10

    class Meta:
        model = ItemDirectory


class DirectoryVersionAdmin(admin.ModelAdmin):
    list_display = ['dir', 'version', 'start_date']
    list_filter = ['dir', 'version', 'start_date']
    search_fields = ['dir', 'version', 'start_date']
    fields = [('dir', 'version'), 'start_date']

    class Meta:
        model = DirectoryVersion


class DirectoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'version', 'start_date']
    list_filter = ['name', 'short_name', 'version', 'start_date']
    search_fields = ['name', 'short_name', 'version', 'start_date', 'description']
    fields = [('name', 'short_name'), 'description', ('version', 'start_date')]

    class Meta:
        model = Directory


admin.site.register(Directory, DirectoryAdmin)
admin.site.register(ItemDirectory, ItemDirectoryAdmin)
admin.site.register(DirectoryVersion, DirectoryVersionAdmin)

