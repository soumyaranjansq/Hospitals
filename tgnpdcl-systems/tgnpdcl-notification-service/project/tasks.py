import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings') # If using Django settings, or remove if standalone

# Basic Celery app
app = Celery('tgnpdcl_notifications')
app.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

@app.task
def send_email_notification(recipient, subject, body):
    print(f"Sending email to {recipient}: {subject}")
    # Integration with email service would go here
    return True
