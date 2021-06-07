from tweetme2.settings import ALLOWED_HOSTS
from django import http
from django.conf import settings
from django.http.response import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.http import HttpResponse, Http404, JsonResponse
import random

from tweets.forms import TweetForm
from tweets.models import Tweet

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kargs):
    return render(request, "pages/home.html", {})

def tweet_create_view(request, *args, **kargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next")
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()

    return render(request, 'components/form.html', context={"form": form})

def tweet_list_view(request, *args, **kargs):
    qs = Tweet.objects.all()

    tweets_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 200)} for x in qs]
    data = {
        "response": tweets_list
    }

    return JsonResponse(data)

def tweet_detail_view(request, tweet_id, *args, **kargs):
    try: 
        obj = Tweet.objects.get(id=tweet_id)
    except:
        raise Http404

    data = {
        "id": tweet_id,
        "content": obj.content
    }

    return JsonResponse(data)