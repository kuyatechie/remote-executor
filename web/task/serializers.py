from rest_framework import serializers
from task.models import Task


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    uid = serializers.UUIDField(required=True)
    created = serializers.DateTimeField(required=True)
    script = serializers.CharField(required=True)
    arguments = serializers.DictField()
    started = serializers.DateTimeField(required=False)
    finished = serializers.DateTimeField(required=False)
    diskspace_before = serializers.IntegerField(required=False)
    diskspace_after = serializers.IntegerField(required=False)
    retcode = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return Task.objects.create(**validated_data)


class TaskObjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
