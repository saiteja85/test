import boto3
import csv

def get_unattached_volumes():
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    csv_filename = "unattached_ebs_volumes.csv"

    with open(csv_filename, mode="w", newline="") as file:
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

    print(f"Report generated: {csv_filename}")

if __name__ == "__main__":
    get_unattached_volumes()



$$$$$$$$
import boto3
import csv

regions = ["us-east-1"]  # Change this if you want to check multiple regions

def get_aws_account_id():
    sts_client = boto3.client("sts")
    return sts_client.get_caller_identity()["Account"]

def get_unused_volumes(regions):
    account_id = get_aws_account_id()  # Fetch AWS Account ID
    all_volumes = []

    for region in regions:
        print(f"Checking region: {region} in account: {account_id}")
        ec2 = boto3.client("ec2", region_name=region)
        volumes = ec2.describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])["Volumes"]

        for volume in volumes:
            all_volumes.append({
                "Account ID": account_id,
                "VolumeId": volume["VolumeId"],
                "Size (GiB)": volume["Size"],
                "Region": region
            })

    # Save to CSV
    filename = "unused_ebs_volumes.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Account ID", "VolumeId", "Size (GiB)", "Region"])
        writer.writeheader()
        writer.writerows(all_volumes)

    print(f"CSV report generated: {filename}")

get_unused_volumes(regions)
