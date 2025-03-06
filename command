import boto3
print(boto3.client("ec2", region_name="us-east-1").describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])["Volumes"])

ec2_client = boto3.client("ec2", region_name="us-east-1")
regions = [r['RegionName'] for r in ec2_client.describe_regions()['Regions']]
for region in regions:
    volumes = boto3.client("ec2", region_name=region).describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])["Volumes"]
    print(f"Region: {region}, Unattached Volumes: {volumes}")



import boto3
import csv

# Set your S3 bucket name (if uploading to S3)
S3_BUCKET = "your-s3-bucket-name"
CSV_FILENAME = "unattached_ebs_volumes.csv"

def get_unattached_volumes():
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    s3_client = boto3.client("s3")
    
    # Get list of all AWS regions
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    
    with open(CSV_FILENAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Region", "Volume ID", "Size (GiB)", "Volume Type", "Availability Zone", "State", "Tags"])
        
        for region in regions:
            ec2 = boto3.client("ec2", region_name=region)
            response = ec2.describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])
            
            for volume in response["Volumes"]:
                tags = volume.get("Tags", "None")
                writer.writerow([
                    region,
                    volume["VolumeId"],
                    volume["Size"],
                    volume["VolumeType"],
                    volume["AvailabilityZone"],
                    volume["State"],
                    tags
                ])

    print(f"CSV report saved: {CSV_FILENAME}")

    # Upload to S3 (optional)
    try:
        s3_client.upload_file(CSV_FILENAME, S3_BUCKET, CSV_FILENAME)
        print(f"CSV file uploaded to s3://{S3_BUCKET}/{CSV_FILENAME}")
    except Exception as e:
        print(f"S3 upload failed: {e}")

if __name__ == "__main__":
    get_unattached_volumes()
