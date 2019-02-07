import json
import boto3
import zipfile
import mimetypes

def lambda_handler(event, context):

    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:390072403864:portfolio-topic')
    try:
        s3 = boto3.resource('s3')
        portfolio_bucket = s3.Bucket('portfolio.bouallag.rrdog.myinstance.com')
        build_bucket = s3.Bucket('portfoliobuild.bouallag')
        build_bucket.download_file('portfoliobuild.zip', '/tmp/portfoliobuild.zip')



        with zipfile.ZipFile('/tmp/portfoliobuild.zip') as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
        return 'Portfolio updated: pushed to prod S3'
        topic.publish(Message='Your Portfolio has been successfully updated', Subject='Portfolio update')
    except:
        topic.publish(Message='Failed to deploy your portfolio', Subject='Portfolio update')
        raise
