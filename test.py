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
