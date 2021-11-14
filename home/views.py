from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    allpost=Post.objects.all()
    context={'allpost':allpost}
    return render(request,'home/home.html',context)

def about(request):
    return render(request,'home/about.html')
def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<5:
            messages.warning(request,"Please fill form correctly.")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request,"Your message has been successfully sent")
    return render(request,'home/contact.html')

def search(request):
    query=request.GET['query']
    if len(query)>60 or len(query)==0:
        allpost=Post.objects.none()
    else:
        # searching query in title,stitle,author,content
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostssTitle= Post.objects.filter(stitle__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allpost=  allPostsTitle.union(allPostsContent, allPostsAuthor,allPostssTitle)

    if allpost.count()==0:
        messages.warning(request,"No search results found. Please refine your query.")
    
    params={'allpost': allpost,'query':query}
    return render(request,'home/search.html',params)

def create(request):
    if request.method=="POST":
        uname=request.POST['uname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        print(uname,email,pass1,pass2)
        if len(uname)>10:
            messages.warning(request, " Your user name must be under 10 characters")
            return render(request,'home/signup.html')
        if not uname.isalnum():
            messages.warning(request, " User name should only contain letters and numbers")
            return render(request,'home/signup.html')
        if (pass1!= pass2):
             messages.warning(request, " Passwords do not match")
             return render(request,'home/signup.html') 

        myuser = User.objects.create_user(uname, email, pass1)
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        
    return render(request,'home/signup.html')
