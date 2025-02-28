from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async
from .models import Admin, Subscribtion
from bson.objectid import ObjectId
import json
import datetime
# Create your views here.

@csrf_exempt
async def create_admin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            admin_id = data.get('admin_id')
            email = data.get('email')

            if not admin_id or not email:
                return JsonResponse({'Error':'admin and email are requird'}, status = 400)
            
            admin_data = Admin(admin_id=admin_id, email=email)
            
            await sync_to_async(admin_data.save)()
            return JsonResponse({'status':'Admin successfuly added'}, status = 200)
        except Exception as e:
            return JsonResponse({'Error':str(e)}, status = 500)
    else:
        return JsonResponse({'Error':'invalid request'}, status = 400)
    
@csrf_exempt
async def subscribe(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            plan_name = data.get('plan_name')
            admin_id = data.get('admin_id')
            plan_id = str(ObjectId())
            create_date_str = data.get('date_create')
            duration_date = data.get('duration_date')
            
            if not all([plan_name, admin_id, create_date_str, duration_date]):
                return JsonResponse({'Error':"all data's are requird"}, status = 400)
            
            create_date = datetime.datetime.strptime(create_date_str, '%Y-%m-%d').date()
            expiry_date = create_date + datetime.timedelta(days=int(duration_date))
            
            subscribtion_data = Subscribtion(
                admin_id = admin_id,
                plan_id = plan_id,
                plan_name = plan_name,
                create_date = create_date,
                duration_date = duration_date,
                expiry_date = expiry_date
            )
            
            await sync_to_async(subscribtion_data.save)()
            return JsonResponse({'status':'subscribtion  successfuly added'}, status = 200)
        except Exception as e:
            return JsonResponse({'Error':str(e)}, status = 500)
    else:
        return JsonResponse({'Error':'invalid request'}, status = 400)