""" 
check-instance-type-availability.py --instance-type instance_type --az availability_zone --profile profile_name  

example
python check-instance-type-availability.py \
    --instance-type t3.micro \
    --az us-east-1d \
    --profile default  

Goal: Returns True if instance type is available

TODO: parameterize the command inputs.
TODO: variables in the Filter of describe_instance_type_offerings
TODO: search the response for the correspond instance type.
"""
from boto3 import Session
from botocore.exceptions import ClientError
import argparse

sess = Session(profile_name='default', region_name='us-east-1')
ec2 = sess.client('ec2')

parser = argparse.ArgumentParser(prog='PROG',
                                 description='Return true or false if an instance type is available in a specific availability zone')
parser.add_argument('--az', default='us-east-1a',
                    help='Specific availability zone')
parser.add_argument('--instancetype', '-i', default='t2.micro',
                    help='Specific instance type, e.g. t2.micro')
parser.add_argument('--profile', '-p', help='AWS Profile name')

args = parser.parse_args()
az = args.az
instancetype = args.instancetype

# It looks like the AZ Location is not filtering the response, so the payload has a list of all AZs where the instance is available.
# This results in a double filter later in the script.
response = ec2.describe_instance_type_offerings(
    DryRun=False,
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

# Extract the DICT to a LIST
instanceofferings = response['InstanceTypeOfferings']

# Populate a list to search. Because the filter in the describe_instance_type_offerings call
# Does not seem to work, a second logic check is required.
instancelist = []
for i in instanceofferings:
    if i['Location'] == az:
        instancelist.append(i['InstanceType'])

if instancetype in instancelist:
    print('Yes, ' + instancetype + ' is available in ' + az)
else:
    print('Yes, ' + instancetype + ' is NOT available in ' + az)
