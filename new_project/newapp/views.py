from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Post
from bson.objectid import ObjectId
import json

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
def create_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        add = data.get('add')
        print(f'data  : {data}')
        if name and add:
            post = Post(name=name, add=add)
            post.save()
            return JsonResponse({'message': 'Post created successfully!'}, status=201)
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_all(request):
    if request.method == 'GET':
        try:
            posts = Post.objects.all()
            
            list_data = [
                {
                    'Id':str(post.id),
                    'name':post.name,
                    'add':post.add
                }
                for post in posts
            ]                
            if not list_data:
                return JsonResponse({'error': 'no data available'})
            else:
                return JsonResponse({'Get all data success':list_data,}, status = 200)
        except Exception as e:
            return JsonResponse({'error':str(e)}, status = 400)
        
def get_one_data(request):
    if request.method == 'GET':
        user_id = request.GET.get('_id', None)
        if not user_id:
            return JsonResponse({'error':'missing _id parameter'}, status  = 400)
        try:
            id_get = Post.objects.get(id=ObjectId(user_id))
            
            data_one =[
                {'id': str(id_get.id),
                'name':id_get.name,
                'add':id_get.add}
            ]
            return JsonResponse({"Message":'data get success','get_one data':data_one}, status = 200)
        except Post.DoesNotExist:
            return JsonResponse({'error':'data not found'}, status = 404)
        except Exception as e:
            return JsonResponse({'erroe': str(e)}, status = 500)
    return JsonResponse({'Error':'Invalid request method'})

def update_data(request):
    if request.method == 'PUT':
        user_id = request.GET.get('_id', None)
        try:
            data = json.loads(request.body)
            name = data.get('name')
            add = data.get('add')
            
            get_id = Post.objects.get(id = ObjectId(user_id))
            
            if not (name or add):
                return JsonResponse({'Error': 'Invalid data provied name and address!'}, status=400)
            if name:
                get_id.name = name
            if add:
                get_id.add = add
            
            get_id.save()
                
            return JsonResponse({'Message': 'updated succesfully!'}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'Error':'data not found'})
        except Exception as e:
            return JsonResponse({'error': str(e)},satus = 500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def delete_one(request):
    if request.method == 'DELETE':
        try:
            user_id = request.GET.get('_id', None)
            if not user_id:
                return JsonResponse({'Error':'user Id is required '}, status = 400)
            get_dataid = Post.objects.get(id = ObjectId(user_id))
            
            get_dataid.delete()
            return JsonResponse({'Message':'Data Deleted successfullt'}, status =  200)
        except Post.DoesNotExist:
            return JsonResponse({'Error':'user not found'}, status = 404)
        except Exception as e:
            return JsonResponse({'Error': str(e)}, status = 500)
    return JsonResponse({'Error':'Invalid request method '}, status = 405) 

def delete_all_data(request):
    if request.method == 'DELETE':
        try:
            all_data_get = Post.objects.delete()
            return JsonResponse({'messge':'AllData deleted successfully'}, status = 200)
        except Exception as e:
            return JsonResponse({'Error': str(e)}, status = 500)
    return JsonResponse({'Error':'Invalid request method'}, status = 404)


