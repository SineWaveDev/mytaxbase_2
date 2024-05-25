from rest_framework import serializers

class JSONFileSerializer(serializers.Serializer):
    json_content = serializers.JSONField()

