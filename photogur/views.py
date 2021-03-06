from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from photogur.models import Picture, Comment
from photogur.forms import LoginForm, PictureForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
 
from django.contrib.auth.forms import UserCreationForm

# def root_path(request):
#     return HttpResponseRedirect('')

def pictures(request):
    pictures = Picture.objects.all() 
    return render(request, 'pictures.html', {
        'pictures': pictures
    })

def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    return  render(request, 'picture.html', {
        'picture': picture
    })

def picture_search(request):
    query = request.GET['query']
    search_results = Picture.objects.filter(artist=query)
   
    return render(request,'search_results.html', {
        'pictures': search_results,
        'query': query,
    })

@login_required
def new_picture(request):
    form = PictureForm(request.POST)
    if form.is_valid():
        new_picture = form.save(commit=False)
        new_picture.user = request.user
        new_picture.save()
        return redirect('pictures')
    else:
        return render(request, 'new_picture_form.html', {
        'form': form
    })

@login_required
def edit_picture(request, id):
    picture = get_object_or_404(Picture, pk=id, user=request.user.pk)
    if request.method == 'GET':
        form = PictureForm(instance=picture)
        return render(request, 'edit_picture_form.html', {
            "picture": picture,
            "form": form
        })
    elif request.method == 'POST': 
        form = PictureForm(request.POST, instance=picture) 
        if form.is_valid(): 
            update_picture = form.save() 
            return redirect(reverse('picture_details', args=[picture.id]))
        else: 
            context = { 'form': form, 'picture': picture }
            return render(request, 'edit_picture_form.html', context) 

@login_required
def delete_picture(request, id):
    picture = get_object_or_404(Picture, pk=id, user=request.user.pk)
    picture.delete() 
    return redirect(reverse('pictures'))



@login_required
def create_comment(request):
    picture_id = request.POST['picture']
    picture = Picture.objects.get(id=picture_id)
    new_comment = Comment()
    new_comment.name = request.POST['name']
    new_comment.message = request.POST['message']
    new_comment.picture = picture
    new_comment.save()

    return render(request, 'picture.html', {'picture': picture})

@login_required
def delete(request, id): 
    comment = Comment.objects.get(pk=id) 
    comment.delete() 
    return redirect(reverse('pictures'))

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')
    else: 
        form = UserCreationForm()
        
    return render(request, 'signup.html', {
        'form': form
    })



