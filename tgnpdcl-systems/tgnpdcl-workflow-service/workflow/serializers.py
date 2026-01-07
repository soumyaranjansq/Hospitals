from rest_framework import serializers
from .models import SanctionRequest, ApprovalLog, WorkflowStep

class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStep
        fields = '__all__'

class ApprovalLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    step_name = serializers.CharField(source='step.name', read_only=True)
    
    class Meta:
        model = ApprovalLog
        fields = '__all__'

class SanctionRequestSerializer(serializers.ModelSerializer):
    logs = ApprovalLogSerializer(many=True, read_only=True)
    current_step_name = serializers.CharField(source='current_step.name', read_only=True)
    
    class Meta:
        model = SanctionRequest
        fields = '__all__'
