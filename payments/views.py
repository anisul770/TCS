from django.shortcuts import redirect
from rest_framework import status
from sslcommerz_lib import SSLCOMMERZ 
from django.conf import settings as main_settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from order.models import Order

# Create your views here.

@api_view(['POST'])
def initiate_payment(request):
    user = request.user
    amount = request.data.get('amount') 
    order_id = request.data.get('orderId')
    num_items = request.data.get('numItems')
  
    settings = { 'store_id': 'tcs69a7588756618', 'store_pass': 'tcs69a7588756618@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"txn_{order_id}"
    post_body['success_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/success/"
    post_body['fail_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/fail/"
    post_body['cancel_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = f"{user.email}"
    post_body['cus_phone'] = "user.phone_number"
    post_body['cus_add1'] = "customer address"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = num_items
    post_body['product_name'] = "Home Service"
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    if response.get('status') == 'SUCCESS':
      return Response({'payment_url': response['GatewayPageURL']})
    # Need to redirect user to response['GatewayPageURL']
    return Response({"error":"Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['POST'])
def payment_success(request):
  order_id = request.data.get("tran_id").split('_')[1]
  order = Order.objects.get(id = order_id)
  order.status = 'Pending'
  order.save()
  return redirect(f'{main_settings.FRONTEND_URL}/dashboard/bookings/{order_id}')

@api_view(['POST']) 
def payment_cancel(request):
  order_id = request.data.get("tran_id").split('_')[1]
  return redirect(f'{main_settings.FRONTEND_URL}/dashboard/bookings/{order_id}')

@api_view(['POST']) 
def payment_fail(request):
  order_id = request.data.get("tran_id").split('_')[1]
  return redirect(f'{main_settings.FRONTEND_URL}/dashboard/bookings/{order_id}')