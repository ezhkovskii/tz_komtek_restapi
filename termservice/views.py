from django.shortcuts import render
from rest_framework import generics
from .models import Directory, ItemDirectory, DirectoryVersion
from .serializers import *


def home(request):
    return render(request, 'index.html')

def docs(request):
    return render(request, 'docs.html')

class DirectoryListView(generics.ListAPIView):
    serializer_class = DirectoryListSerializer

    def get_queryset(self):
        '''
        Получение всех справочников
        или актуальных на указанную дату
        '''
        query_params = self.request.query_params
        date = query_params.get('date', None)
        qs = []
        if date is not None:
            list_dir = Directory.objects.all()
            queryset_list = DirectoryVersion.objects.filter(start_date__gte=date)
            for d in queryset_list:
                qs.append(
                    {
                        'id': d.dir.pk,
                        'name': list_dir.get(pk=d.dir.pk).name,
                        'short_name': list_dir.get(pk=d.dir.pk).short_name,
                        'description': list_dir.get(pk=d.dir.pk).description,
                        'version': d.version,
                        'start_date': d.start_date
                    }
            )
        else:
            list_dir = Directory.objects.all()
            queryset_list = DirectoryVersion.objects.all()
            for d in queryset_list:
                qs.append(
                    {
                        'id': d.dir.pk,
                        'name': list_dir.get(pk=d.dir.pk).name,
                        'short_name': list_dir.get(pk=d.dir.pk).short_name,
                        'description': list_dir.get(pk=d.dir.pk).description,
                        'version': d.version,
                        'start_date': d.start_date
                    }
                )

        return qs


class ItemDirListView(generics.ListAPIView):
    serializer_class = ItemDirListSerializer

    def get_queryset(self):
        '''
        Получение элементов заданного справочника текущей версии
        или указанной версии.
        '''
        query_params = self.request.query_params
        dir = query_params.get('dir', None)
        version = query_params.get('version', None)

        if dir is not None and version is None:
            dir_current_version = Directory.objects.get(pk=dir)
            queryset_list = ItemDirectory.objects.filter(dir=dir, version=dir_current_version.version)

        elif dir is not None and version is not None:
            queryset_list = ItemDirectory.objects.filter(dir=dir, version=version)

        return queryset_list



class ValidatingItemDirListView(generics.ListAPIView):
    serializer_class = ItemDirListSerializer

    def get_queryset(self):
        '''
        Валидация элементов заданного справочника текущей версии или указанной версии.
        Возвращает null в полях id, code, value, если элемент не найден.
        '''
        query_params = self.request.query_params
        dir = query_params.get('dir', None)
        version = query_params.get('version', None)
        code = query_params.get('code', None)

        if dir is not None and code is not None and version is None:
            dir_current_version = Directory.objects.get(pk=dir)
            queryset_list = ItemDirectory.objects.filter(dir=dir, version=dir_current_version.version, code=code)

        elif dir is not None and code is not None and version is not None:
            queryset_list = ItemDirectory.objects.filter(dir=dir, version=version, code=code)

        if not queryset_list:
            queryset_list = [
                {
                'id': None,
                'code': None,
                'value': None
                }
            ]

        return queryset_list



