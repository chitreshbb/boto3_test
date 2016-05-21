# Boto3, Python, and AWS Lambda tutorial part 2

***

#### Install Boto3
```
sudo pip install boto3
ensure that there is a **[default]** profile for boto3 to find:
nano ~/.aws/credentials
```

#### Simple test
create/edit s3_buckets.py :
```
import boto3
s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
  print(bucket.name)
python s3_buckets.py … to a list of your S3 buckets
```

#### Try our lambda function from Part 1
* show code for invoke.py
* run/test in terminal: time ```python invoke.py```
* compare to running the function locally

#### A more realistic approach
While it’s ok to trigger a lambda function remotely and manually for testing purposes,
a more realistic usage would be to trigger a lambda function based on some event.
The AWS Lambda service offers lots of ways to trigger a function.
If we continue with our example function from part 1, we probably would want to create
a file of URLs whose title tags we want to fetch.  So the next step would be to upload
that file of URLs to a S3 bucket.  Anytime a new file appears in that S3 bucket it
would trigger our lambda function to execute.

> This is what we will work on in future episodes.

***
***
