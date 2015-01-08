from django.shortcuts import render, render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from contacts.models import Contact, UserProfile, Articles, Like, Comment
from contacts.forms import UserForm, PostArticleForm, CommentForm
from django.views.generic.edit import CreateView
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.utils.timezone import utc
import datetime
import time

class UserProfileDetailView(DetailView):
    """User Profile in detail view"""
    model = get_user_model()
    slug_field = "username"
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user

def landing(request):
    name = 'Foo Bar'
    t = get_template('landing.html')
    if request.user.is_authenticated():
        #html = t.render(Context({'name': request.user.username}))
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return render_to_response('landing.html')

def details(request, contact_id=1):
    return render_to_response('disp.html', {'contact': Contact.objects.get \
            (id=contact_id)})

def template(request):
    return render_to_response('template.html')

def login(request):
    c = {}
    c.update(csrf(request))
    if request.user.is_authenticated():
       return HttpResponseRedirect('/accounts/loggedin')
    else:
        return render_to_response('login.html', c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid')

def loggedin(request, personal_id=1):
    try:
        return render_to_response('loggedin.html',
                                    {'full_name': request.user.username,
                                    'location': UserProfile.objects.filter \
                                    (user=request.user).location,
                                    'reputation':UserProfile.objects.filter(user=request.user).reputation,})
    except:
        return render_to_response('loggedin.html',
                                    {'full_name': request.user.username,
                                    'location': 'NA'})

def invalid_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('landing.html')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')

    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    return render_to_response('register.html', args)

def register_success(request):
    return render_to_response('register_success.html')

def personal_info(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/index')
        else:
            print form.errors
    else:
         form = PersonalForm()
    return render_to_response('personal_form.html', {'form': form}, context)

class UserProfileEditView(UpdateView):

    model = UserProfile
    form_class = UserForm
    template_name = 'user_edit.html'

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return HttpResponseRedirect('accounts/loggedin/')

def article_view(request):
    model = Articles
    posts = Articles.objects.all()
    score_dict = {}
    for post in posts:
        diff = post.time_stamp - datetime.datetime.utcnow().replace(tzinfo=utc)
        t = abs((diff.days)) * 24 + diff.seconds/3600
        """ranking"""
        score = (post.votes-1)/((t+2)**1.8)
        post.score = score
    for w in sorted(score_dict, key=score_dict.get, reverse=True):
        score_dict[w]
    print type(posts)
    if request.method == 'GET':
        pass
    return render_to_response('articles.html', {'posts':posts, 'full_name':request.user.username,},
            context_instance=RequestContext(request))

def post_article_view(request):
    model = Articles
    template_name = 'post_articles.html'

    if request.method == 'POST':
        form = PostArticleForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.uploader = request.user
            temp.time_stamp = datetime.datetime.now()
            temp.save()
            return HttpResponseRedirect('/accounts/loggedin/')
        else:
            print form.errors
    else:
        form = PostArticleForm()
    return render_to_response(template_name, {'form':form}, \
                                RequestContext(request))

def like_article(request, article_id):
    new_like, created = Like.objects.get_or_create(user=request.user, \
                                                    article_id=article_id)
    if not created:
        pass
    else:
        pass
    a = Articles.objects.get(id=article_id)
    a.votes = a.like_set.all().count()
    rep_user = a.uploader
    if created:
        b = UserProfile.objects.get(user=rep_user)
        b.reputation += 10
        print b.reputation
        b.save()
    a.save()
    return HttpResponse(a.votes)

def add_comment(request, article_id):
    """Add a new comment."""
    template = "comment.html"
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            temp.date = datetime.datetime.now()
            temp.article_id = article_id
            temp.save()
            return HttpResponseRedirect('/accounts/loggedin/')
        else:
            print form.errors
    else:
        form = CommentForm()
    try:
        comments = Comment.objects.filter(article_id=article_id)
        return render_to_response(template, {"form":form, "comments":comments},\
                                 RequestContext(request))
    except:
        return render_to_response(template, {"form":form},\
                                     RequestContext(request))