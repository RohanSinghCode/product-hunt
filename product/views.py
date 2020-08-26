from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import product
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


# Create your views here.


class home(ListView):
    model = product
    context_object_name = 'pr'
    template_name = 'product/home.html'



@login_required(login_url='/accounts/login')
def create(request):

    if request.method == "POST":
        if request.POST['title'] and request.POST['url'] and request.POST['body']:
            pr = product()
            pr.title = request.POST['title']
            pr.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                pr.url =  request.POST['url']
            else:
                pr.url = 'http://' +  request.POST['url']

            if request.POST['image']:
                pr.image = request.FILES['image']

            pr.pub_date =  timezone.datetime.now()
            pr.hunter = request.user
            pr.save()
            return redirect('/product/'+str(pr.id))
        else:
            return render(request,'product/create.html',{'error':'*ALL FIELDS ARE REQUIRED'})

    else:
        return render(request,'product/create.html')



class ProductDetail(DetailView):
    model = product



@login_required(login_url='/accounts/signup')
def upvote(request,product_id):
    if request.method=="POST":
        pr = get_object_or_404(product,pk=product_id)
        pr.votes_total +=1
        pr.save()
        return redirect('/product/'+str(product_id))


class myHunt(LoginRequiredMixin,ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    model = product
    context_object_name = 'hunts'
    template_name = 'product/myHunt.html'
    def get_queryset(self):
        return product.objects.filter(hunter=self.request.user)