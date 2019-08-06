from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render 
from photogur.models import Picture, Comment
from photogur.forms import LoginForm
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm

# def root_path(request):
#     return HttpResponseRedirect('')

def pictures(request):
    pictures = Picture.objects.all() 
    context = {'pictures': pictures}
    response = render(request, 'pictures.html', context)
    return HttpResponse(response)

def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    context = {'picture': picture} 
    response = render(request, 'picture.html', context)
    return HttpResponse(response)

def picture_search(request):
    query = request.GET['query']
    search_results = Picture.objects.filter(artist=query)
    context = {'pictures': search_results,
               'query': query,
    }
    response = render(request,'search_results.html', context)
    return HttpResponse(response)

def create_comment(request):
    picture_id = request.POST['picture']
    picture = Picture.objects.get(id=picture_id)
    new_comment = Comment()
    new_comment.name = request.POST['name']
    new_comment.message = request.POST['message']
    new_comment.picture = picture
    new_comment.save()
    context = {'picture': picture}
    response = render(request, 'picture.html', context)
    return HttpResponse(response)

def login_view(request):
    form = LoginForm()
    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)


def logout_view(request):
    logout(request)
    context = {"pictures": pictures}
    return HttpResponse(request, 'pictures.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('pictures')
    else: 
        form = UserCreationForm()
    html_response = render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)



