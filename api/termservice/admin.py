from django.contrib import admin
from .models import Directory, Item_Directory


class Item_DirectoryAdmin(admin.ModelAdmin):
    list_display = ['id_dir', 'code', 'value']  #какие поля показывать в админке
    list_filter = ['id_dir']                    #по каким полям фильтровать
    search_fields = ['code', 'value']           #по каким полям проводить поиск
    fields = ['id_dir', ('code', 'value')]      #какие поля редактировать (в кортеже поля на одной строке)
    list_per_page = 10

    class Meta:
        model = Item_Directory

class Item_DirectoryInline(admin.TabularInline):
    model = Item_Directory
    extra = 0

class DirectoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'version', 'start_date']
    list_filter = ['name', 'short_name', 'version', 'start_date']
    search_fields = ['name', 'short_name', 'version', 'start_date', 'description']
    fields = [('name', 'short_name'), 'description', ('version', 'start_date')]
    inlines = [Item_DirectoryInline]    #связанная модель. позволяет редактировать элементы справочника в админке в самом справочнике

    class Meta:
        model = Directory

admin.site.register(Directory, DirectoryAdmin)
admin.site.register(Item_Directory, Item_DirectoryAdmin)

