# Boto3, Python, AWS Lambda tutorial part 2, 3, and 4

> Code and instructions for part 2, 3, and 4:
> https://github.com/cleesmith/boto3_test
>
> For part 1 see:
> https://github.com/cleesmith/get_html_head_title_tag

***

## Part 2

#### Install Boto3
```
sudo pip install boto3
```
* ensure that there is a **[default]** profile for boto3 to find:
```
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
* review code in ```invoke.py```
* run/test in terminal: ```time python invoke.py```
* compare to running the function locally

#### A more realistic approach
While it’s ok to trigger a lambda function remotely and manually for testing purposes,
a more realistic usage would be to trigger a lambda function based on some **event**.
The AWS Lambda service offers lots of ways to trigger a function.
If we continue with our example function from part 1, we probably would want to create
a file of URLs whose title tags we want to fetch.  So the next step would be to upload
that file of URLs to a S3 bucket.  Anytime a new file appears in that S3 bucket it
would trigger our lambda function to execute.

> This is what we will work on in future episodes.

***

## Part 3

#### Use boto3 to invoke another lambda function

#### Calling other lambda functions
```
edit lambda_invoker.py
use IAM to update the “fetch_title_role”
zip -9 bundle.zip lambda_invoker.py
aws lambda create-function --region us-east-1 --function-name lambda_invoker --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/fetch_title_role --handler lambda_invoker.lambda_handler --runtime python2.7 --profile pylambs --zip-file fileb://bundle.zip
```

#### testing
* use Lambda console to test lambda_invoker
* use command line to test lambda_invoker

#### conclusion
It’s easy to invoke the fetch_title lambda function we created in part 1 using our new lambda_invoker function.
Note that both of these lambda functions are using the InvocationType of RequestResponse,
so we are not taking advantage of Lambda’s ability to perform functions asynchronously.
We would have to use the InvocationType of Event in order to perform many fetch_title functions in parallel.
But that would also require us to handle the responses differently.
This is where using S3 and DynamoDB come into play … as we will see in future episodes.

***

## Part 4

#### Update lambda function to detect/use a SQS queue
```
see: https://github.com/cleesmith/get_html_head_title_tag
use IAM to update the “fetch_title_role” and attach the AmazonSQSFullAccess policy
... to update and re-deploy:
source env/bin/activate
echo $VIRTUAL_ENV ... to show where python stuff is
edit fetch_title.py ... alter code
rm bundle.zip
zip -9 bundle.zip fetch_title.py
cd $VIRTUAL_ENV/lib/python2.7/site-packages
zip -r9 ~/aws_lambda_python/get_html_head_title_tag/bundle.zip *
cd ~/aws_lambda_python/get_html_head_title_tag
aws lambda update-function-code --function-name fetch_title --profile pylambs --zip-file fileb://bundle.zip --publish
```

#### added fetch_title_via_sqs.py
This new program does the following:
* uses uuid to create an uniquely named SQS queue
* invokes the lambda function fetch_title but asynchronously as an Event
* waits/retrieves/deletes messages from the SQS queue
* deletes the SQS queue … as we are all done

#### test everything works
use a terminal:
```
cd boto3_test
python fetch_title_via_sqs.py
```
view the results

#### conclusion
While everything works as expected, we are not achieving parallelism because of how we are
invoking the lambda function.  In the future we will explore using the threading and multiprocessing
libraries in order to achieve parallelism.
Also, we may explore using a csv/tsv file of URLs to trigger a lambda function from an S3 bucket.

***
***
