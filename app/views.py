from django.shortcuts import render
from .models import Posts
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
# posts= [
#     {
#         'author': 'CoreyMS',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27,2018'
#     },
#     {
#         'author': 'John Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'September 30,2018'
#     }
# ]


# def home(request):
#     postList=Posts.objects.all()
#     return render(request,'app/home.html',{'posts':postList})


class PostListView(ListView):
    model=Posts
    #default view name <app>/<model>_<viewtype>.html
    template_name='app/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5
    
class UserPostListView(ListView):
    model=Posts   
     #default view name <app>/<model>_<viewtype>.html
    template_name='app/user_posts.html'
    context_object_name='posts'
    paginate_by=5
    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model=Posts
def about(request):
    return render(request,'app/about.html',{'title':'About'})

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Posts
    fields=['title', 'content']
    
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Posts
    fields=['title','content']
    
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Posts
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    
    
