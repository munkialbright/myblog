from django.shortcuts import render, HttpResponse
from blog.models import Blog, Contact
import math

# Create your views here.
def home(request):
    return render(request, 'index.html')

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
    return render(request, 'search.html')