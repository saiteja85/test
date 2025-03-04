import boto3
import csv
import io
import os

# S3 bucket name (update this with your bucket name)
S3_BUCKET = "your-s3-bucket-name"
CSV_FILENAME = "unattached_ebs_volumes.csv"

def lambda_handler(event, context):
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    s3_client = boto3.client("s3")
    
    # Get list of all regions
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    
    output = io.StringIO()
    csv_writer = csv.writer(output)
    
    # CSV Header
    csv_writer.writerow(["Region", "Volume ID", "Size (GiB)", "Volume Type", "Availability Zone", "State", "Tags"])
    
    # Iterate through each AWS region
    for region in regions:
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])
        
        for volume in response["Volumes"]:
            tags = volume.get("Tags", "None")
            csv_writer.writerow([
                region,
                volume["VolumeId"],
                volume["Size"],
                volume["VolumeType"],
                volume["AvailabilityZone"],
                volume["State"],
                tags
            ])
    
    # Move to the beginning of the stream
    output.seek(0)
    
    # Upload CSV to S3
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=CSV_FILENAME,
        Body=output.getvalue(),
        ContentType="text/csv"
    )
    
    return {
        "statusCode": 200,
        "body": f"Report successfully saved to s3://{S3_BUCKET}/{CSV_FILENAME}"
    }
