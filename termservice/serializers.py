from rest_framework import serializers
from .models import Directory, ItemDirectory, DirectoryVersion


class DirectoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = '__all__'


class ItemDirListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDirectory
        fields = ('id', 'code', 'value')


class DirectoryVersionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectoryVersion
        fields = '__all__'