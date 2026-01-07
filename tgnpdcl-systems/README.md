# TGNPDCL Medical Bill Reimbursement System

## Microservices Architecture

- **Hospital Service**: Port 8001
- **Workflow Service**: Port 8002
- **Document Service**: Port 8003
- **Notification Service**: Background Worker

## Getting Started

1. **Start the stack**:
   ```bash
   docker-compose up --build
   ```

2. **Access APIs**:
   - Hospital Service: http://localhost:8001/api/
   - Workflow Service: http://localhost:8002/api/
   - Document Service: http://localhost:8003/api/

3. **Development flow**:
   - Create a superuser in hospital service: `docker-compose exec hospital-service python manage.py createsuperuser`
   - Log in and submit bills.
