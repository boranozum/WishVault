from rest_framework import serializers

from account.serializers.user import BriefUserSerializer


class BaseModelSerializer(serializers.ModelSerializer):
    created_by = BriefUserSerializer(read_only=True)
    updated_by = BriefUserSerializer(read_only=True)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        abstract = True
        model = None
        fields = [
            'id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'is_active',
        ]
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        validated_data['updated_by'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)
