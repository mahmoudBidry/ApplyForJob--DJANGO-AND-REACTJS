from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Candidate
from .serializers import CandidateSerializer

import os
import re

SIZE_LIMIT = 3
CV_PATH  = "CVs/"
allowed_extensions = ['.pdf']


def is_valid_email(email):
    """Check if the given email address is valid"""
    email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return bool(email_regex.match(email))

def is_email_exist(email):
    try:
        Candidate.objects.get(email=email)
        return True
    except Candidate.DoesNotExist:
        return False

def is_valid_extension(extension):
    if extension.lower() in allowed_extensions :
        return True
    return False

def is_valid_cv_size(cv_size):
    if cv_size <= SIZE_LIMIT*1024*1024:
        return True
    return False




@api_view(['GET'])
def apiOverview(request) :
    api_urls = {
		'List':'/candidate-list/',
		'Detail View':'/candidate-detail/<int:pk>/',
		'Create':'/candidate-create/',
		'Update':'/candidate-update/<int:pk>/',
		'Patch':'/candidate-patch/<int:pk>/',
		'Delete':'/candidate-delete/<int:pk>/',
		'DeleteAll':'candidate-delete-all/',
		}
    
    return Response(api_urls)


@api_view(['GET'])
def candidate_list(request):
	candidates = Candidate.objects.all()
	serializer = CandidateSerializer(candidates, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def candidate_detail(request, pk):
    try:
        candidate = Candidate.objects.get(id=pk)
    except Candidate.DoesNotExist:
        return Response({'message': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    serializer = CandidateSerializer(candidate, many=False)
    return Response(serializer.data)



@api_view(['POST'])
def create_candidate(request):
    serializer = CandidateSerializer(data=request.data)
    if not is_valid_email(request.data["email"]) :
        return Response({'message': 'email format is invalid.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if is_email_exist(request.data["email"]):
        return Response({'message': 'email already exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    if serializer.is_valid():   
        cv = request.FILES['cv']
        
        # Check file extension
        _, extension = os.path.splitext(cv.name)

        if not is_valid_extension(extension) :
            return Response({'message': 'Only PDF files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)        

        # Check if the file size is less than or equal to "SIZE_LIMIT" MB
        if not is_valid_cv_size(cv.size):
            return Response({"message": "The submitted file size should be less than "+str(SIZE_LIMIT)+"MB."}, status=status.HTTP_400_BAD_REQUEST)
        
        filename = request.data['first_name'] +"_"+ request.data['last_name'] + extension.lower()
        
        serializer.save(cv=filename)

        # if the CVs folder does not exist, create it
        if not os.path.exists('CVs'):
            os.makedirs('CVs')


        cv_path = os.path.join(CV_PATH, filename )
        with open(cv_path, 'wb') as f:
            for chunk in cv.chunks():
                f.write(chunk)

        return Response({'message': 'Candidate created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def update_candidate(request, pk):
    try:
        candidate = Candidate.objects.get(id=pk)
    except Candidate.DoesNotExist:
        return Response({'message': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CandidateSerializer(candidate, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Candidate updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def patch_candidate(request, pk):
    try:
        candidate = Candidate.objects.get(id=pk)
    except Candidate.DoesNotExist:
        return Response({'message': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CandidateSerializer(candidate, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Candidate updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_candidate(request, pk):
    try:
        candidate = Candidate.objects.get(id=pk)
    except Candidate.DoesNotExist:
        return Response({'message': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)
    
    filename = candidate.cv    
    # return Response({'message': str(filename)}, status=status.HTTP_204_NO_CONTENT)

    os.remove(CV_PATH+ str(filename))
    candidate.delete()
    return Response({'message': 'Candidate deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_all_candidates(request):
    Candidate.objects.all().delete()
    for filename in os.listdir(CV_PATH):
        os.remove(CV_PATH+ str(filename))

    return Response({'message': 'all candidates are deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

