from rest_framework import serializers
from configuration.models import ColumnConfiguration

class ConfigurationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColumnConfiguration
        fields = [
            'id', 'label', 'key', 'is_disabled', 'width', 'is_sortable',
            'is_filterable', 'filter_type', 'is_selected', 'module_id', 'user_id'
        ]

class ConfigurationSerializer(serializers.Serializer):
    user_preference_setting = ConfigurationDetailSerializer(many=True)

    def create(self, validated_data):
        user_preference_setting = validated_data.get('user_preference_setting', [])
        module_id = self.context.get('module_id')
        user_id = self.context.get('user_id')

        if user_preference_setting:
            module_id = user_preference_setting[0].get('module_id')
            user_id = user_preference_setting[0].get('user_id')

        if module_id is None or user_id is None:
            raise serializers.ValidationError("Module ID or User ID is missing from user_preference_setting.")

        ColumnConfiguration.objects.filter(module_id=module_id, user_id=user_id).delete()

        configurations = []
        for config_data in user_preference_setting:
            config_data.update({'module_id': module_id, 'user_id': user_id})
            configuration = ColumnConfiguration.objects.create(**config_data)
            configurations.append(configuration)

        return configurations

    def update(self, instance, validated_data):
        user_preference_setting = validated_data.get('user_preference_setting', [])
        module_id = instance.module_id
        user_id = instance.user_id

        if module_id is None or user_id is None:
            raise serializers.ValidationError("Module ID or User ID is missing from user_preference_setting.")

        updated_instances = []
        for config_data in user_preference_setting:
            config_id = config_data.get('id')
            if config_id:
                try:
                    configuration = ColumnConfiguration.objects.get(id=config_id, module_id=module_id, user_id=user_id)
                    ColumnConfiguration.objects.filter(module_id=module_id, user_id=user_id).exclude(id=config_id).delete()

                    for attr, value in config_data.items():
                        setattr(configuration, attr, value)
                    configuration.save()

                    updated_instances.append(configuration)
                except ColumnConfiguration.DoesNotExist:
                    raise serializers.ValidationError(f"ColumnConfiguration with id={config_id} does not exist.")
            else:
                config_data.update({'module_id': module_id, 'user_id': user_id})
                new_configuration = ColumnConfiguration.objects.create(**config_data)
                ColumnConfiguration.objects.filter(module_id=module_id, user_id=user_id).exclude(id=new_configuration.id).delete()
                updated_instances.append(new_configuration)

        return updated_instances

class ConfigurationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColumnConfiguration
        fields = '__all__'
