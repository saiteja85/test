import boto3
print(boto3.client("ec2", region_name="us-east-1").describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])["Volumes"])

ec2_client = boto3.client("ec2", region_name="us-east-1")
regions = [r['RegionName'] for r in ec2_client.describe_regions()['Regions']]
for region in regions:
    volumes = boto3.client("ec2", region_name=region).describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])["Volumes"]
    print(f"Region: {region}, Unattached Volumes: {volumes}")




$$$$$$$$$$

import boto3
import csv

region = "us-east-1"  # Change this to your desired region

def get_unused_volumes(region):
    ec2 = boto3.client("ec2", region_name=region)
    volumes = ec2.describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])["Volumes"]

    all_volumes = []
    for volume in volumes:
        all_volumes.append({
            "VolumeId": volume["VolumeId"],
            "Size (GiB)": volume["Size"],
            "Region": region
        })

    # Save to CSV
    with open(f"unused_ebs_volumes_{region}.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["VolumeId", "Size (GiB)", "Region"])
        writer.writeheader()
        writer.writerows(all_volumes)

    print(f"CSV report generated: unused_ebs_volumes_{region}.csv")

get_unused_volumes(region)
