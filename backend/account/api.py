from django.http import JsonResponse
from django.db.models import Q

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignupForm
from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save()

        # Enviar a verificação por email depois!
    else:
        message = 'error'

    return JsonResponse({'message': message})


@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)

    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': FriendshipRequestSerializer(requests, many=True).data
    }, safe=False)


@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)

    requests_between_users = FriendshipRequest.objects.filter(
        Q (created_for=request.user, created_by=user) |
        Q (created_for=user, created_by=request.user))
    rejected_by_target = FriendshipRequest.objects.filter(created_for=user, created_by=request.user, status=FriendshipRequest.REJECTED)
    rejected_by_me = FriendshipRequest.objects.filter(created_for=request.user, created_by=user, status=FriendshipRequest.REJECTED)
    pending_from_target = FriendshipRequest.objects.filter(created_for=user, created_by=request.user, status=FriendshipRequest.SENT)

    if not requests_between_users.exists():
        FriendshipRequest.objects.create(created_for=user, created_by=request.user)
        return JsonResponse({'message': 'solicitação de amizade criada'})
        
    elif rejected_by_target.exists():
        return JsonResponse({'message': 'solicitação já rejeitada'})
    
    elif rejected_by_me.exists() and not pending_from_target.exists():
        FriendshipRequest.objects.create(created_for=user, created_by=request.user)
        return JsonResponse({'message': 'solicitação de amizade criada'})
    
    return JsonResponse({'message': 'solicitação já enviada'})


@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.get(created_for=request.user, created_by=user)
    friendship_request.status = status
    friendship_request.save()

    if status == FriendshipRequest.ACCEPTED:
        user.friends.add(request.user)
        request.user.friends.add(user)

        user.friends_count += 1
        request.user.friends_count += 1

        user.save()
        request.user.save()

    return JsonResponse({'message': 'solicitação de amizade atualizada'})
