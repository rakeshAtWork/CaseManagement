from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from configuration.serializers import ConfigurationListSerializer, ConfigurationSerializer, \
    ConfigurationDetailSerializer

from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from configuration.models import ColumnConfiguration
from configuration.serializers import ConfigurationListSerializer, ConfigurationSerializer
from acl.models import MasterModule


class ConfigurationCreateAPIView(CreateAPIView):
    serializer_class = ConfigurationSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     user_id = self.request.user.id
    #     module_id = self.request.query_params.get('module_id', None)
    #
    #     queryset = ColumnConfiguration.objects.filter(user_id=user_id)
    #
    #     if module_id is not None:
    #         queryset = queryset.filter(module_id=module_id)
    #
    #     return queryset

    def post(self, request, *args, **kwargs):
        user_preference_setting = request.data.get('user_preference_setting', [])

        if not user_preference_setting:
            return Response({'error': 'user_preference_setting is empty'}, status=status.HTTP_400_BAD_REQUEST)

        first_item = user_preference_setting[0]
        module_id = first_item.get('module_id')
        user_id = first_item.get('user_id')

        if not module_id:
            return Response({'error': 'Module ID is required in user_preference_setting'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not user_id:
            return Response({'error': 'User ID is not available in user_preference_setting'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not MasterModule.objects.filter(module_id=module_id).exists():
            return Response({'error': 'Invalid module ID'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ConfigurationSerializer(data={'user_preference_setting': user_preference_setting},
                                             context={'module_id': module_id, 'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        configurations = serializer.save()

        response_serializer = ConfigurationListSerializer(configurations, many=True)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ConfigurationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ColumnConfiguration.objects.all()
    serializer_class = ConfigurationDetailSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """
        Override this method to handle the update operation.
        """
        try:
            # Save the updated instance
            instance = serializer.save()

            # Get the module_id and user_id from the instance
            module_id = instance.module_id
            user_id = instance.user_id

            if module_id is not None and user_id is not None:
                # Delete all configurations with the same module_id and user_id except the updated one
                ColumnConfiguration.objects.filter(module_id=module_id, user_id=user_id).exclude(
                    id=instance.id).delete()
        except ValidationError as e:
            raise ValidationError({"error": str(e)})

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()


class ConfigurationListAPIView(ListAPIView):
    serializer_class = ConfigurationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned configurations to a given user and module_id.
        """
        user_id = self.request.user.id
        module_id = self.request.query_params.get('module_id', None)

        queryset = ColumnConfiguration.objects.filter(user_id=user_id)

        if module_id is not None:
            queryset = queryset.filter(module_id=module_id)

        return queryset
