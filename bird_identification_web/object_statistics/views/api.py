from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import LoggedObject
from ..permissions import CanUploadPermission

class LoggedObjectUpload(APIView):
    permission_classes = (IsAuthenticated, CanUploadPermission)

    def post(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"detail": "Data should be a list of objects"}, status=status.HTTP_400_BAD_REQUEST)


        created_ids = []
        try:
            for item in data:
                obj = LoggedObject.objects.create(
                    class_name=item.get('class_name'),
                    start_time=item.get('start_time'),
                    end_time=item.get('end_time')
                )
                created_ids.append(obj.id)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_ids, status=status.HTTP_201_CREATED)
