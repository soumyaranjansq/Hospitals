from django.contrib import admin
from .models import WorkflowStep, SanctionLimit, SanctionRequest, ApprovalLog

admin.site.register(WorkflowStep)
admin.site.register(SanctionLimit)
admin.site.register(SanctionRequest)
admin.site.register(ApprovalLog)
