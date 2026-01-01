from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReceiptScanSerializer
from .models import ReceiptScan
from .tasks import process_receipt_task

class ReceiptScanView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ReceiptScanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        scan_id = kwargs.get('scan_id')
        if scan_id is None:
            serializer = ReceiptScanSerializer(ReceiptScan.objects.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        try:
            serializer = ReceiptScanSerializer(ReceiptScan.objects.get(id=scan_id))
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ReceiptScan.DoesNotExist:
            return Response({'error': 'Receipt scan not found'}, status=status.HTTP_404_NOT_FOUND)

class ReceiptScanProcessView(APIView):
    def post(self, request, *args, **kwargs):
        image = request.data.get('image')
        if not image:
            return Response({'error': 'Image is required'}, status=status.HTTP_400_BAD_REQUEST)
        scan = ReceiptScan.objects.create(image=image)
        process_receipt_task.delay(scan.pk)
        return Response({'id': scan.pk}, status=status.HTTP_201_CREATED)
