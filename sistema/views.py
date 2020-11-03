#from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from sistema.serializers import *
from rest_framework import generics, permissions
from rest_framework import viewsets
#from rest_auth.registration.views import RegisterView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic.detail import DetailView
from .forms import SignInForm
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def create(self, request, *args, **kwargs):
        super(PostViewSet, self).create(request, *args, **kwargs)
        # here may be placed additional operations for
        # extracting id of the object and using reverse()
        return HttpResponseRedirect(redirect_to='/api/newpost/')

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# desplegar una imagen en el archivo imagen.html
@login_required
def image(request,pk):
    form = ContactForm()
    formr = ResponseForm()
    formar = CommentRepliesForm()
    template = get_template('image.html')
    username = request.user.username
    if not username:
        username = None
    comr=list()
    try:
        post = Post.objects.get(pk=pk)
        try:
            comment = Comment.objects.filter(post=post)
        except Comment.DoesNotExist:
            comment = 0
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    if comment != 0:
        replies =Response.objects.all()
        #for reply in replies:
            #comr.append(reply.comment)
        if replies.count==0:
            replies = 0
    if request.method=='GET':
        html = template.render({'post': post, 'comment':comment, 'form':form, 'formr':formr,
                        'comr':comr,'replies':replies,'formar':formar,'username':username }, request)
        return HttpResponse(html)

    elif request.method == 'POST':
        if request.POST['flag']=="responder":
            if request.user.is_staff and request.user.is_superuser:
                try:
                    com = Comment.objects.get(pk=request.POST['primarkey'])
                except Comment.DoesNotExist:
                    com = 0
                formr = ResponseForm(data=request.POST)
                formr.fields['respuesta'].error_messages = {'required': 'Este campo es requerido'}
                if formr.is_valid():
                    usr = request.user.username
                    if (not request.user.username):
                        usr = "Anónimo"
                    Response.objects.create(repliedBy=usr, text=request.POST['respuesta'], comment=com)
                return HttpResponseRedirect("/api/rest/posts/" + str(post.id) + "/image/")
            else:
                return HttpResponse('Forbidden access', status=403)
        elif  request.POST['flag']=="comentar":
            form = ContactForm(data=request.POST)
            form.fields['mensaje'].error_messages = {'required': 'Este campo es requerido'}
            if form.is_valid():
                usr = request.user.username
                if (not request.user.username):
                    usr = "Anónimo"
                Comment.objects.create(createdBy=usr, text=request.POST['mensaje'], post=post)
            return HttpResponseRedirect("/api/rest/posts/" + str(post.id) + "/image/")
def home(request):
    template = get_template('home.html')
    username = request.user.username
    if not username:
        username = None
    if request.method=='GET':
        html = template.render({ 'username':username}, request)
        return HttpResponse(html)
def about(request):
    template = get_template('about.html')
    username = request.user.username
    if not username:
        username = None
    if request.method=='GET':
        html = template.render({ 'username':username}, request)
        return HttpResponse(html)
#create a new post and retrieve all posts
@login_required
def post(request):
    if request.user.is_superuser and request.user.is_staff:
        formp = PostForm()
        allposts = Post.objects.all()
        username = request.user.username
        if not username:
            username = None
        template = get_template('createpost.html')
        if request.method == 'GET':
            html = template.render({'formp': formp, 'allposts': allposts, 'username': username}, request)
            return HttpResponse(html)
    else:
        return HttpResponse('Forbidden access', status=403)
#retrieve all posts
def allposts(request):
    template = get_template('posts.html')
    allposts = Post.objects.all()
    sform = SearchForm()

    username = request.user.username
    if not username:
        username = None
    if request.method=='GET':
        html = template.render({'allposts':allposts,'username':username,'sform':sform }, request)
        return HttpResponse(html)
    elif request.method == 'POST':
        name=request.POST['name']
        allposts = Post.objects.filter(postTitle__icontains=name)
        # filtrando con icontains no importan las mayusculas ni minusculas
        if allposts.count == 0:
            allposts = 0
        sform = SearchForm()
        html = template.render({'allposts':allposts, 'username': username, 'sform': sform}, request)
        return HttpResponse(html)
def contact(request):
    template = get_template('contacto.html')
    username = request.user.username
    if not username:
        username = None
    if request.method=='GET':
        html = template.render({'username':username }, request)
        return HttpResponse(html)

@login_required
def singlepost(request,pk):
    if request.user.is_superuser and request.user.is_staff:
        formp = PostForm()
        username = request.user.username
        post = Post.objects.get(pk=pk)
        if not username:
            username = None
        template = get_template('postdata.html')
        contador=0
        if request.method == 'GET':
            html = template.render({'formp': formp,'contador':contador,
                                    'username': username, 'post': post},request)
            return HttpResponse(html)
        elif request.method == 'POST':
            if request.POST['delete'] == "update":
                try:
                    post.postTitle = request.POST['postTitle']
                    post.postDescription = request.POST['postDescription']
                    post.link = request.POST['link']
                    post.save()
                except Post.DoesNotExist:
                    pass
                return HttpResponseRedirect(redirect_to='/api/rest/posts/' + str(pk) + '/data/')
            elif request.POST['delete'] == "delete":
                Post.objects.filter(pk=pk).delete()
                return HttpResponseRedirect(redirect_to='/api/newpost/')
    else:
        return HttpResponse('Forbidden access', status=403)
@login_required
def addimages(request,pk):
    if request.user.is_superuser and request.user.is_staff:
        formar = CommentRepliesForm()
        formr = ResponseForm()
        template = get_template('addimages.html')
        username = request.user.username
        if not username:
            username = None
        try:
            post = Post.objects.get(pk=pk)
            try:
                comment = Comment.objects.filter(post=post)
            except Comment.DoesNotExist:
                comment = 0
        except Post.DoesNotExist:
            return HttpResponse(status=404)
        responses=Response.objects.all()
        if responses.count()==0:
            responses=0
        if request.method == 'GET':
            html = template.render({ 'post': post,'formar':formar,
            'formr':formr,'responses':responses,'comment':comment, 'username': username}, request)
            return HttpResponse(html)
        elif request.method == 'POST':
            if request.POST['flag']=="deleteresponse":
                Response.objects.filter(pk=request.POST['primarkey']).delete()
                return HttpResponseRedirect("/api/rest/posts/" + str(post.id) + "/addimages/")
            elif request.POST['flag'] == "delete":
                Comment.objects.filter(pk=request.POST['commentid']).delete()
                return HttpResponseRedirect("/api/rest/posts/" + str(post.id) + "/addimages/")
    else:
        return HttpResponse('Forbidden access', status=403)
class Login(APIView):
    def post(self, request, format=None):
        data = request.data
        flag = data.get('flag')
        if flag == "login":
            username = data.get('usuario')
            password = data.get('password')
            account = authenticate(username=username, password=password)
            if account is not None:
                user = get_user_model().objects.get(username=username)
                if user.is_active:
                    login(request, account)
                    if user.is_superuser and user.is_staff:
                        return HttpResponseRedirect("/api/newpost/")
                    #serialized = UserSerializer(account)
                    return HttpResponseRedirect("/api/home/")
                else:
                    return HttpResponse('Bad Request', status=400)
            else:
                return HttpResponse('Bad Request', status=400)
        elif flag=="register":
            formu = SignUpForm(data=request.POST)
            #formu.fields['username'].error_messages = {'required': 'Este campo es requerido'}
            #formu.fields['name'].error_messages = {'required': 'Este campo es requerido'}
            #formu.fields['firstLastName'].error_messages = {'required': 'Este campo es requerido'}
            #formu.fields['secondLastName'].error_messages = {'required': 'Este campo es requerido'}
            #formu.fields['password'].error_messages = {'required': 'Este campo es requerido'}
            #formu.fields['password2'].error_messages = {'required': 'Este campo es requerido'}
            #formu.fields['email'].error_messages = {'required': 'Este campo es requerido'}
            if formu.is_valid():
                serializer = UserSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                return HttpResponseRedirect("/api/login/")
            else:
                username = request.user.username
                if not username:
                    username = None
                form = SignInForm()
                return render(request, 'login.html', {'form': form,'formu':formu,'username':username  })
        else:
            return HttpResponse('Bad Request', status=400)
    def get(self, request, format=None):
        username = request.user.username
        if not username:
            username = None
        formu = SignUpForm()
        form = SignInForm()
        return render(request, 'login.html', {'form': form,'formu':formu,'username':username  })

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class ResponseViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer



class LogoutView(APIView):
    def post(self, request, format=None):
        logout(request)
        return HttpResponseRedirect("/api/login/")