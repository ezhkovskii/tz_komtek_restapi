from django.db import models

'''
Модель справочника
'''
class Directory(models.Model):
    name = models.CharField(verbose_name = 'Наименование', max_length=255)
    short_name = models.CharField(verbose_name = 'Короткое наименование', max_length=100)
    description = models.TextField(verbose_name = 'Описание')
    version = models.CharField(verbose_name = 'Версия справочника', max_length=20)
    start_date = models.DateTimeField(auto_now=True, verbose_name = 'Дата начала действия справочника текущей версии')

    __current_version = None

    def __init__(self, *args, **kwargs):
        super(Directory, self).__init__(*args, **kwargs)
        self.__current_version = self.version #сохранение текущей версии для проверки изменения

    def save(self, *args, **kwargs):
        '''
        При изменении версии справочника все элементы из него добавляются в таблицу "ItemDirectory" с измененным полем "Версия"
        и в таблицу "DirectoryVersion" добавляется новая версия справочника
        '''
        if self.version != self.__current_version:
            super(Directory, self).save(*args, **kwargs)
            list_items = ItemDirectory.objects.filter(dir=self)
            for item in list_items:
                item_dir = ItemDirectory(dir=item.dir, version=self.version, code=item.code, value=item.value).save()
            dir_version = DirectoryVersion(dir=self, version=self.version, start_date=self.start_date).save()

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'version'], name='unique_name_version')
        ]
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'


'''
Модель элемента справочника
'''
class ItemDirectory(models.Model):
    dir = models.ForeignKey(Directory, verbose_name = 'Справочник', on_delete=models.CASCADE)
    version = models.CharField(verbose_name='Версия справочника', max_length=20)
    code = models.CharField(verbose_name = 'Код элемента', max_length=20)
    value = models.CharField(verbose_name = 'Значение элемента', max_length=255)

    def save(self, *args, **kwargs):
        '''
        При добавлении нового элемента в справочник поле "версия" заполняется значением из поля "версия" справочника
        '''
        list_dir = Directory.objects.filter(id=self.dir.pk)
        self.version = list_dir[0].version
        super(ItemDirectory, self).save(*args, **kwargs)

    def __str__(self):
        return self.code

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'version'], name='unique_code_version')
        ]
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочников'


'''
Модель таблицы "версии справочников"
'''
class DirectoryVersion(models.Model):
    dir = models.ForeignKey(Directory, verbose_name ='Справочник', on_delete=models.CASCADE)
    version = models.CharField(verbose_name='Версия справочника', max_length=20)
    start_date = models.DateTimeField(auto_now=True, verbose_name='Дата начала действия версии справочника')

    def __str__(self):
        return str(self.dir)

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'