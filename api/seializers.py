from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    people = serializers.StringRelatedField(many=True)
    transaction = serializers.StringRelatedField(many=True)
    class Meta:
        model = Invoice
        fields = ['id', 'name', 'people', 'transaction', 'people_num']