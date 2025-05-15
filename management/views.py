from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Profile, Tag, Photo
from .forms import ProfileUpdateForm, PhotoUploadForm

def index(request):
    tag_filter = request.GET.get('tag')
    if tag_filter:
        photos = Photo.objects.filter(tags__name=tag_filter)
    else:
        photos = Photo.objects.all()
    tags = Tag.objects.all()
    return render(request, 'index.html', {'photos': photos, 'tags': tags})

@login_required
def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if request.user in photo.liked_by.all():
        photo.liked_by.remove(request.user)  # Unlike the photo
    else:
        photo.liked_by.add(request.user)  # Like the photo
    return redirect('photo_detail', photo_id=photo.id)

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'photo_detail.html', {'photo': photo})

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})

@login_required
def profile_update(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'profile_update.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user  # Set the user who uploaded the photo
            photo.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            return redirect('index')
    else:
        form = PhotoUploadForm()
    return render(request, 'upload_photo.html', {'form': form})

@login_required
def my_photos(request):
    photos = Photo.objects.filter(uploaded_by=request.user)
    return render(request, 'my_photos.html', {'photos': photos})