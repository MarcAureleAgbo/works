from rest_framework import serializers
from .models import approvals

class ApprovalsSerializers(serializers.ModelSerializer):
    class meta:
        model=approvals
        fields='__all__'