from django.conf import settings
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework import serializers

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tweets.forms import TweetForm
from tweets.models import Tweet
from .serializers import (
    TweetSerializer, 
    TweetActionSerializer,
    TweetCreateSerializer)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kargs):
    return render(request, "pages/home.html", {})

@api_view(['POST'])
#@authentication_classes([SessionAuthentication])
#@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kargs):
    user = request.data
    print(user)
    serializer = TweetCreateSerializer(data = request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = request.user)
        return Response(serializer.data, status=201)
    return Response({}, status = 400)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kargs):
    qs = Tweet.objects.filter(id = tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)    
    return Response(serializer.data, status = 200) 

@api_view(['GET'])
def tweet_list_view(request, *args, **kargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many = True)    
    return Response(serializer.data)    

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kargs):
    qs = Tweet.objects.filter(id = tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"Message": "You cannot delete this tweet"}, status=403)
    obj = qs.first()
    obj.delete()
    return Response({"Message": "You deleted this tweet"}, status = 200)  


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kargs):
    '''
    id is required
    action options are: like, unlike, retweet
    '''
    
    serializer = TweetActionSerializer(data = request.data)
    
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id = tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            
            return Response(serializer.data, status = 200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status = 200)
        elif action == "retweet":
            serializer = TweetSerializer(obj)
            new_tweet = Tweet.objects.create(
                user = request.user, 
                parent=obj,
                content=serializer.data.get("content"),)
            
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status = 201)
            

    print("here")
    return Response({}, status = 200)







def tweet_create_view_pure_django(request, *args, **kargs):
    user = request.user
    if not request.user.is_authenticated:
        if request.is_ajax():
            user = None
            return JsonResponse({}, status = 401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next")
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status = 201)

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    
    if form.errors:
        if request.is_ajax():
            print("400")
            return JsonResponse(form.errors, status = 400)
    return render(request, 'components/form.html', context={"form": form})

def tweet_list_view_pure_django(request, *args, **kargs):
    qs = Tweet.objects.all()

    tweets_list = [x.serialize() for x in qs]
    data = {
        "response": tweets_list
    }

    return JsonResponse(data)

def tweet_detail_view_pure_django(request, tweet_id, *args, **kargs):
    data = {
        "id": tweet_id,
    }
    status = 200
    try: 
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404


    return JsonResponse(data, status=status)