from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CRUD
from django.shortcuts import get_object_or_404
from .serializers import CRUD_Serializers,UserSerializer  # Use the corrected serializer name


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # This will require authentication for all methods
def home(request):
    if request.method == 'GET':
        snippets = CRUD.objects.all()
        serializer = CRUD_Serializers(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CRUD_Serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])  # This will require authentication for all methods
def home_by_Id(request, id):
    crud_instance = get_object_or_404(CRUD, uid=id)

    if request.method == 'GET':
        serializer = CRUD_Serializers(crud_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CRUD_Serializers(crud_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
    })

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        print(f"New user created: {user.username}, Token: {token.key}")
        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)