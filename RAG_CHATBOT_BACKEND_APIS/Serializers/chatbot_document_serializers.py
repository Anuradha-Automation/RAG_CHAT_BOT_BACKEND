import logging
from rest_framework import serializers
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, ChatbotAppearance

# Configure logger
logger = logging.getLogger(__name__)

class ChatBotDBSerializer(serializers.ModelSerializer):
    """
    Serializer for the ChatBotDB model, including related ChatbotAppearance data.
    """
    chatbot_appearance_id = serializers.PrimaryKeyRelatedField(
        queryset=ChatbotAppearance.objects.all(),
        source='chatbot_appearance',  # Links chatbot_appearance_id to the actual object
        required=False,  # Make optional if not always required
        allow_null=True,  # Allow null values if applicable
    )

    class Meta:
        model = ChatBotDB
        fields = '__all__'  # Includes chatbot_appearance_id and all other fields

    def to_representation(self, instance):
        """
        Customizes the serialized representation of the ChatBotDB instance.
        """
        logger.debug(f"Serializing ChatBotDB instance: {instance}")
        representation = super().to_representation(instance)
        logger.debug(f"Serialized ChatBotDB representation: {representation}")
        return representation

    def to_internal_value(self, data):
        """
        Customizes the deserialization process for ChatBotDB data.
        """
        logger.debug(f"Deserializing ChatBotDB data: {data}")
        internal_value = super().to_internal_value(data)
        logger.debug(f"Deserialized ChatBotDB internal value: {internal_value}")
        return internal_value

    def validate(self, data):
        """
        Validates the ChatBotDB data before saving.
        """
        logger.debug(f"Validating ChatBotDB data: {data}")
        validated_data = super().validate(data)
        logger.debug(f"Validated ChatBotDB data: {validated_data}")
        return validated_data

class ChatbotAppearanceSerializer(serializers.ModelSerializer):
    """
    Serializer for the ChatbotAppearance model, including related ChatBotDB data.
    """
    chatbotdata = ChatBotDBSerializer(source='chatbot', read_only=True)  # Fetch related ChatBotDB object

    class Meta:
        model = ChatbotAppearance
        fields = '__all__'  # Includes all fields and chatbotdata

    def to_representation(self, instance):
        """
        Customizes the serialized representation of the ChatbotAppearance instance.
        """
        logger.debug(f"Serializing ChatbotAppearance instance: {instance}")
        representation = super().to_representation(instance)
        logger.debug(f"Serialized ChatbotAppearance representation: {representation}")
        return representation

    def to_internal_value(self, data):
        """
        Customizes the deserialization process for ChatbotAppearance data.
        """
        logger.debug(f"Deserializing ChatbotAppearance data: {data}")
        internal_value = super().to_internal_value(data)
        logger.debug(f"Deserialized ChatbotAppearance internal value: {internal_value}")
        return internal_value

    def validate(self, data):
        """
        Validates the ChatbotAppearance data before saving.
        """
        logger.debug(f"Validating ChatbotAppearance data: {data}")
        validated_data = super().validate(data)
        logger.debug(f"Validated ChatbotAppearance data: {validated_data}")
        return validated_data