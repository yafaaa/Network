from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Post


def index(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        content = request.POST.get("content")
        if content:
            Post.objects.create(user=request.user, content=content)
    posts = Post.objects.all().order_by("-timestamp")
    return render(request, "network/index.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def all_posts(request):
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, "network/all_posts.html", {
        "posts": posts
    })


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user).order_by('-timestamp')
    is_following = request.user in profile_user.followers.all()
    can_follow = request.user != profile_user

    if request.method == "POST" and can_follow:
        if is_following:
            profile_user.followers.remove(request.user)
        else:
            profile_user.followers.add(request.user)
        return redirect('profile', username=username)

    context = {
        "profile_user": profile_user,
        "posts": posts,
        "followers_count": profile_user.followers.count(),
        "following_count": profile_user.following.count(),
        "is_following": is_following,
        "can_follow": can_follow,
    }
    return render(request, "network/profile.html", context)


@login_required
def following(request):
    # Get users the current user is following
    following_users = request.user.following.all()
    # Get posts from those users
    posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')
    return render(request, "network/following.html", {
        "posts": posts
    })
