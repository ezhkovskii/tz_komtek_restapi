from django.shortcuts import render
from rest_framework import generics
from .models import Directory, Item_Directory
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

        if date is not None:
            #Directory.objects.filter(start_date__gte=date)
            queryset_list = Directory.objects.raw('''SELECT * 
                                                        FROM termservice_directory
                                                        WHERE start_date >= %s''', [date])
        else:
            queryset_list = Directory.objects.all()


        return queryset_list



class ItemDirListView(generics.ListAPIView):
    serializer_class = ItemDirListSerializer

    def get_queryset(self):
        '''
        Получение элементов заданного справочника текущей версии
        или указанной версии
        '''
        query_params = self.request.query_params
        dir = query_params.get('dir', None)
        version = query_params.get('version', None)

        if dir is not None and version is None:
            queryset_list = Item_Directory.objects.raw('''SELECT id, code, value   
                                                    FROM termservice_item_directory 
                                                    WHERE id_dir_id in 
                                                        (SELECT Max(id) as id
                                                        FROM termservice_directory 
                                                        WHERE short_name = %s
                                                        GROUP BY name)''', [dir])

        elif dir is not None and version is not None:
            queryset_list = Item_Directory.objects.raw('''SELECT id, code, value   
                                                    FROM termservice_item_directory 
                                                    WHERE id_dir_id in 
                                                        (SELECT id as id
                                                        FROM termservice_directory 
                                                        WHERE short_name = %s and version = %s)''', [dir, version])

        return queryset_list



class ValidatingItemDirListView(generics.ListAPIView):
    serializer_class = ItemDirListSerializer

    def get_queryset(self):
        '''
        Валидация элементов заданного справочника текущей версии или указанной версии.
        Вовзращает null в полях id, code, value, если элемент не найден.
        '''
        query_params = self.request.query_params
        dir = query_params.get('dir', None)
        version = query_params.get('version', None)
        code = query_params.get('code', None)

        if dir is not None and code is not None and version is None:
            queryset_list = Item_Directory.objects.raw('''SELECT id, code, value   
                                                    FROM termservice_item_directory 
                                                    WHERE id_dir_id in 
                                                        (SELECT Max(id) as id
                                                        FROM termservice_directory 
                                                        WHERE short_name = %s
                                                        GROUP BY name) and code = %s''', [dir, code])

        elif dir is not None and code is not None and version is not None:
            queryset_list = Item_Directory.objects.raw('''SELECT id, code, value   
                                                    FROM termservice_item_directory 
                                                    WHERE id_dir_id in 
                                                        (SELECT id as id
                                                        FROM termservice_directory 
                                                        WHERE short_name = %s and version = %s) and code = %s''', [dir, version, code])

        if not queryset_list:
            queryset_list = [
                {
                'id': None,
                'code': None,
                'value': None
                }
            ]

        return queryset_list



