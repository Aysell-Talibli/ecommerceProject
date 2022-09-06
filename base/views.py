from audioop import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Product, Product_Companies,Profile,Cart,CustomUser,Order_product
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

def home(request):
    products=Product.objects.all()
    product_companies=Product_Companies.objects.all()
    profiles=Profile.objects.all()
    
    context={'products':products, 'product_companies':product_companies,
    'profiles':profiles,}
    return render(request,'home.html',context)
    
def register(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.user_type = form.cleaned_data.get('user_type')
            user.save()
            return redirect('login')
    else:
        form=RegisterForm()
    return render(request,'register.html',{'form':form})

class Price(LoginRequiredMixin, CreateView):
    model=Product_Companies
    fields=['price','product_id']
    success_url=reverse_lazy('home')
    def form_valid(self, form):
        form.instance.company_id=self.request.user
        return super().form_valid(form)
def product_detail(request,pk):
    product=Product.objects.get(id=pk)
    context={'product':product}
    return render(request,'detail.html',context)

def add_to_cart(request,pk):
    product = get_object_or_404(Product_Companies, pk=pk)
    created = Cart.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False)
    return redirect('home')

class Cart_product(LoginRequiredMixin,DetailView):
    model=Cart
    template_name='cart.html'
    context_object_name='carts'
    def get_object(self, **kwargs):
        user=get_object_or_404(CustomUser,username=self.kwargs.get('username'))
        return Cart.objects.filter(user=self.request.user)
    

class Order(LoginRequiredMixin, CreateView):
    model=Order_product
    fields=['name','address','phone','ordered']
    template_name='order.html'
    success_url=reverse_lazy('home')
    context_object_name='ordered_products'
    success_message='your order succesfull'
    def form_valid(self, form):
        form.instance.user=self.request.user
        form.instance.product_id=self.kwargs['pk']
        return super().form_valid(form)
