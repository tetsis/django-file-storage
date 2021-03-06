from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from model.models import GCP_File, AWS_File
from google.cloud import storage
import boto3
import os
from datetime import datetime, timedelta
 
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

def list_objects(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    object_list = []
    for key in bucket.objects.all():
        object_list.append(key.key)

    return object_list

def dict_objects(bucket_name, files):
    object_list = []
    s3_client = boto3.client('s3', region_name='ap-northeast-1')
    for file in files:
        url = s3_client.generate_presigned_url(
            ClientMethod = 'get_object',
            Params = {'Bucket' : bucket_name, 'Key' : file.name},
            ExpiresIn = 3600,
            HttpMethod = 'GET'
        )
        object_list.append({'key': file.name, 'url': url})

    return object_list

def get_presigned_url(bucket_name, key):
    s3_client = boto3.client('s3', region_name='ap-northeast-1')
    url = s3_client.generate_presigned_url(
        ClientMethod = 'get_object',
        Params = {'Bucket' : bucket_name, 'Key' : key},
        ExpiresIn = 3600,
        HttpMethod = 'GET'
    )

    return url

def upload_object(bucket_name, source_file_name, destination_objcet_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    
    # ファイル拡張子からContent-typeを指定する
    # boto3を使ったアップロードでは自動でContent-typeを指定してくれない
    ext = os.path.splitext(source_file_name)[1][1:]
    content_type = 'binary/octet-stream'
    if ext == 'jpg' or ext == 'jpeg':
       content_type = 'image/jpeg'
    elif ext == 'png' or ext == 'gif':
        content_type = 'image/' + ext

    expires = datetime.now() + timedelta(days=7)
    bucket.upload_file(source_file_name, destination_objcet_name, ExtraArgs={'ContentType': content_type, 'Expires': expires})

def gcp_index(request):
    files = GCP_File.objects.all()

    bucket_name = os.environ.get('BUCKET_NAME', 'bucket_name')
    #file_list = list_blobs(bucket_name)

    context = {
        'files': files,
        #'file_list': file_list,
        'bucket_name': bucket_name,
    }
    return render(request, 'gcp_index.html', context)

def gcp_upload(request):
    return render(request, 'gcp_upload.html')

def gcp_upload_api(request):
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
            new_file = GCP_File(name=file_name, upload_time=datetime.now())
            new_file.save()

            # ファイルを削除
            os.remove(file_path)

            return JsonResponse({'data': 'success'})
        except:
            return JsonResponse({'data': 'failed'})

def aws_index(request):
    files = AWS_File.objects.all()

    bucket_name = os.environ.get('AWS_BUCKET_NAME', 'aws_bucket_name')
    object_list = list_objects(bucket_name)
    object_dict = dict_objects(bucket_name, files)

    context = {
        'files': files,
        'bucket_name': bucket_name,
        'object_list': object_list,
        'object_dict': object_dict,
    }
    return render(request, 'aws_index.html', context)

def aws_upload(request):
    return render(request, 'aws_upload.html')

def aws_upload_api(request):
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

            # S3にアップロード
            bucket_name = os.environ.get('AWS_BUCKET_NAME', 'aws_bucket_name')
            upload_object(bucket_name, file_path, file_name)

            # DBに登録
            new_file = AWS_File(name=file_name, upload_time=datetime.now())
            new_file.save()

            # ファイルを削除
            os.remove(file_path)

            return JsonResponse({'data': 'success'})
        except:
            return JsonResponse({'data': 'failed'})

def aws_media(request, file):
    bucket_name = os.environ.get('AWS_BUCKET_NAME', 'aws_bucket_name')
    pre_signed_url = get_presigned_url(bucket_name, file)

    return redirect(pre_signed_url)
