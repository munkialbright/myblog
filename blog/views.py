from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Blog, Contact
from django.core.mail import send_mail
from django.conf import settings
import math

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        context = {'authenticated': True}
    else:
        context = {'authenticated': False}
    return render(request, 'index.html', context)

def register(request):
    context = {'message': '', 'successful': ''}
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
                context = {'successful': 'Account has been successfully created.'}
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
            return redirect('profile')
        else:
            context = {'message': 'Invalid Credentials'}
            return render(request, 'login.html', context)

    return render(request, 'login.html', context)

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

    if request.user.is_authenticated:
        context = {'blogs': blogs, 'prev': prev, 'next': next, 'authenticated': True}
    else:
        context = {'blogs': blogs, 'prev': prev, 'next': next, 'authenticated': False}

    return render(request, 'blog.html', context)

def editor(request):
    if request.user.is_authenticated:
        context = {'success': '', 'authenticated': True}

        if request.method == "POST":
            #Handle the edited blog
            title = request.POST['title']
            author = request.POST['author']
            slug = request.POST['b_slug']
            content = request.POST['content']

            b_article = Blog.objects.filter(slug=slug)

            if b_article:
                u_article = Blog.objects.filter(slug=slug).update(title=title, author=author,user_name = request.user, slug=slug, content=content)

                context = {'success': 'Your article has been successfully edited and published.', 'slug': slug, 'blog': blog, 'authenticated': True}
            else:
                b_article = Blog(title=title, author=author,user_name = request.user, slug=slug, content=content)
                b_article.save()

                context = {'success': 'Your article has been successfully created and published.', 'slug': slug, 'authenticated': True}

        return render(request, 'editor.html', context)
    else:
        return redirect('login')

def editpost(request, slug):
    if request.user.is_authenticated:
        blog = Blog.objects.filter(Q(slug=slug) & Q(user_name=request.user.id)).first()
        context = {'success': '', 'blog': blog, 'authenticated': True}

        return render(request, 'editpost.html', context)
    else:
        return redirect('login')

def deletepost(request, slug):
    if request.user.is_authenticated:
        blog = Blog.objects.filter(slug=slug).delete()

        return redirect('profile')
    else:
        return redirect('login')

def blogpost(request, slug):
    blog = Blog.objects.filter(slug=slug).first()

    if request.user.is_authenticated:
        context = {'blog': blog, 'authenticated': True}
    else:
        context = {'blog': blog, 'authenticated': False}

    #return HttpResponse(f"You are viewing {slug}")
    return render(request, 'blogpost.html', context)

def contact(request):
    if request.user.is_authenticated:
        context = {'success': '', 'authenticated': True}

        if request.method == "POST":
            
            #Creating variables and assigning to them content submited by the form
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']

            mail_subject = "My Blog (" + name + ", " + email + ")"
        
            #Send an email to the owner of the site
            send_mail(mail_subject, message, email, [settings.EMAIL_HOST_USER])

            #Creat instance
            contact = Contact(name=name, email=email, message=message)
            #Save intance to the database
            contact.save()

            context = {'success': 'Your message has been sent. We shall reply to you via your email.', 'authenticated': True}

        return render(request, 'contact.html', context)
    else:
        return redirect('login')

def profile(request):
    if request.user.is_authenticated:
        u_blog = Blog.objects.filter(user_name=request.user.id)
        u_info = User.objects.filter(username=request.user.id).first()

        context = {'blogs': u_blog, 'user_info': u_info, 'authenticated': True}

        return render(request, 'profile.html', context)
    else:
        return redirect('login')

def search(request):
    if request.method == 'GET':
        srch = request.GET.get('search')
        blogs = Blog.objects.all().filter(Q(title__icontains=srch) |
        Q(author__icontains=srch))

        if request.user.is_authenticated:
            context = {'blogs': blogs, 'srch_input': srch, 'authenticated': True}
        else:
            context = {'blogs': blogs, 'srch_input': srch, 'authenticated': False}

    return render(request, 'search.html', context)

def logout_view(request):
    logout(request)
    return render(request, "login.html")
