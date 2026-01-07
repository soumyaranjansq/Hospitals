from rest_framework import viewsets, parsers, permissions
from .models import Document
from .serializers import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Save original filename
        if 'file' in self.request.data:
            file_obj = self.request.data['file']
            serializer.save(original_filename=file_obj.name)
        else:
            serializer.save()
