import boto3
print(boto3.client("ec2", region_name="us-east-1").describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])["Volumes"])
