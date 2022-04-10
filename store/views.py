from store.forms import MyUserCreationForm
from .models import Category,Product,User
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('store')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password,email=email)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'store/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('store')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'store/register.html', {'form': form})


def store(request):
    search = request.GET.get('search') if request.GET.get('search') != None else ''
    products = Product.objects.filter(
        Q(available = True,category__slug__icontains=search) |
        Q(available = True,name__icontains=search) |
        Q(available = True,seller__username__icontains=search))

                        
    categories = Category.objects.all()
    context = {'categories':categories,'products':products}
    return render(request,'store/store.html', context)

def product_detail(request,uuid):
    categories = Category.objects.all()
    product = get_object_or_404(Product,id=uuid,available=True)
    context = {'product':product,'categories':categories}
    return render(request,'store/product_detail.html',context)

