""" 
check-instance-type-availability.py --instance-type instance_type --az availability_zone --profile profile_name  

example
python check-instance-type-availability.py \
    --instance-type t3.micro \
    --az us-east-1d \
    --profile default  

Goal: Returns True if instance type is available

DONE: parameterize the command inputs.
DONE: variables in the Filter of describe_instance_type_offerings
DONE: search the response for the correspond instance type.
DONE: validate input against a valid set of regions and availability zones
TODO: check for environment variable, re default region if region is not provided
TODO: Add debug option with logging (https://docs.python.org/3/howto/logging.html)
"""
from boto3 import Session
from botocore.exceptions import ClientError
import argparse
import sys

parser = argparse.ArgumentParser(prog='PROG',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='Return true or false if an instance type is available in a specific availability zone',
                                 epilog='''\
    This will return: 
        0 if the instance type is found in the region and AZ 
        1 if the instance type is not found in the region and AZ
        2 if there is an error with either the region or AZ being incorrectly specified
                                          ''')
parser.add_argument('--az', default='us-east-1a',
                    help='Specific availability zone')
parser.add_argument('--instancetype', '-i', default='t2.micro',
                    help='Specific instance type, e.g. t2.micro')
parser.add_argument('--region', '-r', default='us-east-1',
                    help='The AWS region, e.g. us-east-1')
parser.add_argument('--profile', '-p', help='AWS Profile name')

args = parser.parse_args()
az = args.az.lower()
instancetype = args.instancetype.lower()
region = args.region.lower()
profile = args.profile

if not (region):
    region = 'us-east-1'

# The region name is hard coded here to allow the program to retreive region names.
# There is a second sess and ec2 call that uses the region passed on the command line
sess = Session(profile_name=profile, region_name='us-east-1')
ec2 = sess.client('ec2')

# ERROR CHECKING INPUT
# Retrieves all regions/endpoints and checks against input value region
region_list = ec2.describe_regions()['Regions']
region_names = []
for i in region_list:
    region_names.append(i['RegionName'])

if not region in region_names:
    print('Error: region ' + region + ' not a valid AWS region')
    sys.exit(2)

sess = Session(profile_name=profile, region_name=region)
ec2 = sess.client('ec2')

# Retrieves availability zones for the region specified on the command line
# Confirms the availability zone is in the specified region
az_list = ec2.describe_availability_zones()['AvailabilityZones']
az_names = []
for i in az_list:
    az_names.append(i['ZoneName'])

if not az in az_names:
    print('Error: availability zone ' + az +
          ' is not available in AWS region ' + region)
    print('If you are receiving this you may have left off the --region parameter.')
    sys.exit(2)

# The AZ Location is not filtering the response to just the specified AZ.
# The payload has a list of all AZs where the instance is available.
# This results in a set of logic later in the script.
response = ec2.describe_instance_type_offerings(
    LocationType='availability-zone',
    Filters=[
        {
            'Name': 'location',
            'Values': [
                az,
            ],
            'Name': 'instance-type',
            'Values': [
                instancetype,
            ]
        },
    ],
)

# Extract the DICT to a LIST and make the code more readable
instance_offerings = response['InstanceTypeOfferings']

# Populate a list to search. Because the filter in the describe_instance_type_offerings call
# returns all AZs, a second logic check is required.
instance_list = []
for i in instance_offerings:
    if i['Location'] == az:
        instance_list.append(i['InstanceType'])

if instancetype in instance_list:
    print('Yes, ' + instancetype + ' is available in ' +
          az + ' in the ' + region + ' region.')
    sys.exit(0)
else:
    print('No, ' + instancetype + ' is NOT available in ' +
          az + ' in the ' + region + ' region.')
    sys.exit(1)
