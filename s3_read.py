from __future__ import print_function
import json
import StringIO
import boto3

# future:
# this should be triggered by a file upload to this
# s3 bucket containing a url on each line:
s3 = boto3.resource('s3')
s3_object = s3.Object('clsbucket','urls.txt')
urls = s3_object.get()["Body"].read()
url_title = {}
buf = StringIO.StringIO(urls)
for url in buf.readlines():
  # invoke "fetch_title" lambda function for each url:
  url_title[url.strip()] = "some title"
  print(url.strip())

print(url_title)
for i,k in enumerate(url_title):
  print(i,k,url_title[k])

ut = json.dumps(url_title)
print(s3.Object('clsbucket', 'cls.txt').put(Body=ut))

# astring = "this is only a test\ntesting line 2"
# print(astring)
# print(s3.Object('clsbucket', 'cls.txt').put(Body=astring))
