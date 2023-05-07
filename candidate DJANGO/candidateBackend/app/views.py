from django.http import FileResponse
from django.conf import settings


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.permissions import IsAdminUser

from .models import Candidate
from .serializers import CandidateSerializer

import os
import re
import base64


SIZE_LIMIT = 3
CV_PATH_FOLDER  = "CVs/"
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

def string_to_64(cv_string):
    cv_path = os.path.join(CV_PATH_FOLDER, cv_string.replace('/', ''))
    cv_file = open(cv_path, 'rb')
    cv_data = cv_file.read()
    cv_base64 = base64.b64encode(cv_data).decode('utf-8')
    return cv_base64


@api_view(['GET'])
def apiOverview(request) :
    api_urls = {
		'List':'/candidate-list/',
		'Detail':'/candidate-detail/<int:pk>/',
		'Create':'/candidate-create/',
		'Update':'/candidate-update/<int:pk>/',
		'Patch':'/candidate-patch/<int:pk>/',
		'Delete':'/candidate-delete/<int:pk>/',
		'DeleteAll':'/candidate-delete-all/',
		}
    
    return Response(api_urls)



@api_view(['GET'])
def candidate_list(request):
    candidates = Candidate.objects.all()
    serializer = CandidateSerializer(candidates, many=True)
    candidates_object = []
    for candidate in serializer.data:
        candidate["cv"] = string_to_64(candidate["cv"])
        candidates_object.append(candidate)

    return Response(candidates_object)
    

@api_view(['GET'])
def candidate_detail(request, pk):
    try:
        candidate = Candidate.objects.get(id=pk)
    except Candidate.DoesNotExist:
        return Response({'message': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    serializer = CandidateSerializer(candidate, many=False)
    candidate = serializer.data
    candidate["cv"] = string_to_64(candidate["cv"])
    return Response(candidate)



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
        

        # if the CVs folder does not exist, create it
        if not os.path.exists(CV_PATH_FOLDER):
            os.makedirs(CV_PATH_FOLDER)


        cv_path = os.path.join(CV_PATH_FOLDER, filename )
        with open(cv_path, 'wb') as f:
            for chunk in cv.chunks():
                f.write(chunk)
        
        serializer.save(cv=filename)

        return Response({'message': 'Candidate created successfully '}, status=status.HTTP_201_CREATED)
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

    os.remove(CV_PATH_FOLDER+ str(filename))
    candidate.delete()
    return Response({'message': 'Candidate deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
# @permission_classes([IsAdminUser])
def delete_all_candidates(request):
    Candidate.objects.all().delete()
    for filename in os.listdir(CV_PATH_FOLDER):
        os.remove(CV_PATH_FOLDER+ str(filename))

    return Response({'message': 'all candidates are deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

