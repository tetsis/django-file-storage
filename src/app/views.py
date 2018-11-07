from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from model.models import File
from google.cloud import storage
import os
from datetime import datetime
 
def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix='media/')

    return blobs

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

def index(request):
    files = File.objects.all()

    bucket_name = os.environ.get('BUCKET_NAME', 'bucket_name')
    #file_list = list_blobs(bucket_name)

    context = {
        'files': files,
        #'file_list': file_list,
        'bucket_name': bucket_name,
    }
    return render(request, 'index.html', context)

def upload(request):
    return render(request, 'upload.html')

def upload_api(request):
    if request.method == 'POST':
        # ファイルを取得
        try:
            # アップロードファイルの取得
            file = request.FILES['file']
        except KeyError:
            return JsonResponse({'data': 'failed'})

        try:
            file_name = datetime.now().strftime('%Y%m%d-%H%M%S-') + file.name
            file_path = os.path.join('/tmp', file_name)
            destination = open(file_path, 'wb')

            # ファイルを一時保存
            for chunk in file.chunks():
                destination.write(chunk)

            # GCSにアップロード
            bucket_name = os.environ.get('BUCKET_NAME', 'bucket_name')
            upload_blob(bucket_name, file_path, 'media/' + file_name)

            # DBに登録
            new_file = File(name=file_name, upload_time=datetime.now())
            new_file.save()

            # ファイルを削除
            os.remove(file_path)

            return JsonResponse({'data': 'success'})
        except:
            return JsonResponse({'data': 'failed'})