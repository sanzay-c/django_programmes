# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.response import Response
# from .models import PersonDetail
# from .serializers import PersonDetailSerializer

# # Create your views here.
# class PersonsDetailsView(APIView):
#     # GET request to fetch
#     def get(self, request):
#         Persons_Detail = PersonDetail.objects.all()
#         serializer = PersonDetailSerializer(Persons_Detail, many=True) 
#         return Response(serializer.data)
    
#      # POST request to create a new blog post
#     def post(self, request):
#         serializer = PersonDetailSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# myapp/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PersonDetail
from .serializers import PersonDetailSerializer

class PersonDetailList(APIView):
    def get(self, request, format=None):
        # Fetch all PersonDetail objects from the database
        people = PersonDetail.objects.all()
        # Serialize the data
        serializer = PersonDetailSerializer(people, many=True)
        return Response(serializer.data)



class PersonDetailView(APIView):
    def get(self, request, pk, format=None):
        try:
            person = PersonDetail.objects.get(pk=pk)  # Fetch person by primary key (ID)
        except PersonDetail.DoesNotExist:
            return Response({"error": "Person not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonDetailSerializer(person)  # Serialize the person
        return Response(serializer.data)