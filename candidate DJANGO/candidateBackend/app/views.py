from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate
from .serializers import CandidateSerializer


@api_view(['GET'])
def apiOverview(request) :
    api_urls = {
		'List':'/candidate-list/',
		'Detail View':'/candidate-detail/<str:pk>/',
		'Create':'/candidate-create/',
		'Update':'/candidate-update/<str:pk>/',
		'Delete':'/candidate-delete/<str:pk>/',
		}
    
    return Response(api_urls)


@api_view(['GET'])
def candidate_list(request):
	candidates = Candidate.objects.all()
	serializer = CandidateSerializer(candidates, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def candidate_detail(request, pk):
	candidate = Candidate.objects.get(id= pk)
	serializer = CandidateSerializer(candidate, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def create_candidate(request):
    serializer = CandidateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Candidate created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def update_candidate(request, pk):
    candidate = Candidate.objects.get(id= pk)
    serializer = CandidateSerializer(instance= candidate, data= request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Candidate updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
def delete_candidate(request, pk):
    candidate = Candidate.objects.get(id= pk)
    candidate.delete()
    return Response({'message': 'Candidate deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

