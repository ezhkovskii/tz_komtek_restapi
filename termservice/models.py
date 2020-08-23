from django.db import models

'''
Модель справочника
'''
class Directory(models.Model):
    name = models.CharField(verbose_name = 'Наименование', max_length=255)
    short_name = models.CharField(verbose_name = 'Короткое наименование', max_length=100)
    description = models.TextField(verbose_name = 'Описание')
    version = models.CharField(verbose_name = 'Версия справочника', max_length=20)
    start_date = models.DateField(verbose_name = 'Дата начала действия справочника текущей версии',)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'version'], name='unique_version')
        ]
        verbose_name = 'Directory'
        verbose_name_plural = 'Directories'

    def __str__(self):
        return self.name + ' v. ' + self.version


'''
Модель элемента справочника
'''
class Item_Directory(models.Model):
    id_dir = models.ForeignKey(Directory, verbose_name = 'Справочник', on_delete=models.CASCADE)
    code = models.CharField(verbose_name = 'Код элемента', max_length=20)
    value = models.CharField(verbose_name = 'Значение элемента', max_length=255)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Item_Directory'
        verbose_name_plural = 'Item_Directories'