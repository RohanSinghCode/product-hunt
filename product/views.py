from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.edit import CreateView
from .models import product
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic.detail import DetailView


# Create your views here.


def home(request):
    pr = product.objects
    return render(request,'product/home.html',{'pr':pr})



@login_required(login_url='/accounts/signup')
def create(request):

    if request.method == "POST":
        if request.POST['title'] and request.POST['url'] and request.FILES['image'] and request.FILES['icon'] and request.POST['body']:
            pr = product()
            pr.title = request.POST['title']
            pr.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                pr.url =  request.POST['url']
            else:
                pr.url = 'http://' +  request.POST['url']

            pr.icon = request.FILES['icon']
            pr.image = request.FILES['image']

            pr.pub_date =  timezone.datetime.now()
            pr.hunter = request.user
            pr.save()
            return redirect('/product/'+str(product_id))
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

