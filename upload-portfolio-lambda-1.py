import json
import boto3
import zipfile
import mimetypes

def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    portfolio_bucket = s3.Bucket('portfolio.bouallag.rrdog.myinstance.com')
    build_bucket = s3.Bucket('portfoliobuild.bouallag')
    build_bucket.download_file('portfoliobuild.zip', '/tmp/portfoliobuild.zip')


    with zipfile.ZipFile('/tmp/portfoliobuild.zip') as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
    return 'Hello from Lambda'
