import boto3

s3 = boto3.client('s3',
                    aws_access_key_id='AKIAS64VQUZTEAL4F3PX',
                    aws_secret_access_key= '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'
                     )
BUCKET_NAME='blockchain-identity'

def upload_file(file_name, bucket):
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response

def show_image(bucket):
    s3_client = boto3.client('s3')
    public_urls = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 100)
            public_urls.append(presigned_url)
    except Exception as e:
        pass
    # print("[INFO] : The contents inside show_image = ", public_urls)
    return public_urls