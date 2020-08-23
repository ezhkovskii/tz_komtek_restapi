from rest_framework import serializers
from .models import Directory, Item_Directory


class DirectoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = '__all__'
        #fields = ('name', 'version', 'start_date')


class ItemDirListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item_Directory
        fields = ('id', 'code', 'value')