from multiprocessing import context
from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required    
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from . forms import PaymentForm




def store(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'store/store.html', context)


def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)


def buy_item(request, name):
    product = get_object_or_404(Product, name=name)
    PAYSTACK_PUBLIC_KEY = settings.PAYSTACK_PUBLIC_KEY
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    context = {}
    context['product'] = product
    context['PAYSTACK_PUBLIC_KEY'] = PAYSTACK_PUBLIC_KEY
    context['PAYSTACK_SECRET_KEY'] = PAYSTACK_SECRET_KEY
    return render(request, 'store/buy_item.html', context)


# def deposit(request):
    
#     if request.is_ajax():
#         order_cost = request.POST.get('amount', False)
#         transaction_id =  request.POST.get('ref', False)
#         customer = request.user
#         if request.user.is_authenticated:
#             deposit = Ordered.objects.create(order_cost=order_cost,transaction_id=transaction_id,customer=customer,)
#             deposit.verified = True
#             deposit.save()
#             deposited = True
#             messages.success(request, 'Success, Deposit Successful')   
#             if deposited == True:
                
#                 messages.success(request, 'Deposit, Successful')
                 
#                 return JsonResponse({'deposited':deposited})



# def deposit_complete(request):
#     ref = request.GET.get('ref')
#     try:
#         paid = Ordered.objects.get(ref=ref,user=request.user) 
#         context={
#             'paid':paid
#         }
#         return render(request, 'includes/deposit_complete.html', context)
#     except(Ordered.DoesNotExist):
#         return redirect('store')


def initiate_payment(request: HttpRequest) ->HttpResponse:
    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid:
            payment = payment_form.save()
            return render(request, 'store/make_payment.html', {'payment': payment, "paystack_public_key":settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form = PaymentForm()
    return render(request, 'store/initiate_payment.html', {'payment_form': payment_form, "paystack_public_key":settings.PAYSTACK_PUBLIC_KEY})



def verify_payment(request: HttpRequest, ref: str):
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "Verification Successful")
    else:
        messages.error(request, "verification failed")
    return redirect('initiate-payment')

