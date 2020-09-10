from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Blog, Contact
import math

# Create your views here.
def home(request):
    return render(request, 'index.html')

def register(request):
    context = {'message': ''}
    if request.method == 'POST':
        user_e = User.objects.all().filter(Q(username= request.POST.get("username",False)) | Q(email= request.POST.get("email",False)))
        if user_e:
            context = {'message': 'Username or email is already used! Please kindly change'}
            return render(request, 'register.html', context)
        else:
            if request.POST.get("pswd",False) == request.POST.get("c_pswd",False):
                user=User.objects.create_user(username= request.POST.get("username",False),email= request.POST.get("email",False),password=request.POST.get("pswd",False))
                user.first_name=request.POST.get("fistName",False)
                user.last_name=request.POST.get("lastName",False)
                user.save()
                if user is not None:
                    user_authenticate = authenticate(request, username= request.POST.get("username",False), password=request.POST.get("password",False))
                    login(request,user_authenticate)  
                    return redirect('home')
                else:
                    context = {'message': 'Please fill all fields'}
                    return render(request, 'register.html', context)
            else:
                context = {'message': 'Passwords don`t match!'}
                return render(request, 'register.html', context)

        
    return render(request, 'register.html')

def login_view(request):
    context = {'message': ''}
    if request.method == 'POST':
        user_id = request.POST.get("user_id",False)
        password = request.POST.get("pswd",False) 
        user = authenticate(request, username=user_id, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            context = {'message': 'Invalid Credentials'}
            return render(request, 'login.html', context)

    return render(request, 'login.html')

def blog(request):
    numPosts = 5
    page = request.GET.get('page')

    if page is None:
        page = 1
    else:
        page = int(page)
    
    t_blogs = Blog.objects.all()
    length = len(t_blogs)
    blogs = Blog.objects.all()[(page-1)*numPosts: page*numPosts]

    if page>1:
        prev = page - 1
    else:
        prev = None

    if page<math.ceil(length/numPosts):
        next = page + 1
    else:
        next = None

    context = {'blogs': blogs, 'prev': prev, 'next': next}

    return render(request, 'blog.html', context)

def editor(request):
    context = {'success': ''}

    if request.method == "POST":
        #Handle the blog form
        title = request.POST['title']
        author = request.POST['author']
        slug = request.POST['b_slug']
        content = request.POST['content']

        b_article = Blog(title=title, author=author, slug=slug, content=content)
        b_article.save()

        context = {'success': 'Your article has been successfully created and published.', 'slug': slug}

    return render(request, 'editor.html', context)

def blogpost(request, slug):
    blog = Blog.objects.filter(slug=slug).first()
    context = {'blog': blog}

    #return HttpResponse(f"You are viewing {slug}")
    return render(request, 'blogpost.html', context)

def contact(request):
    context = {'success': ''}

    if request.method == "POST":
        
        #Creating variables and assigning to them content submited by the form
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        #Creat instance
        contact = Contact(name=name, email=email, message=message)
        #Save intance to the database
        contact.save()

        context = {'success': 'Your message has been sent. We shall reply to you via your email.'}

    return render(request, 'contact.html', context)

def search(request):
    if request.method == 'GET':
        srch = request.GET.get('search')
        blogs = Blog.objects.all().filter(Q(title__icontains=srch) |
        Q(author__icontains=srch))

        context = {'blogs': blogs, 'srch_input': srch}

    return render(request, 'search.html', context)