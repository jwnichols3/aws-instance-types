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
from botocore.exceptions import ClientError
from boto3 import Session
import argparse

sess = Session(profile_name='default', region_name='us-east-1')
ec2 = sess.client('ec2')

parser = argparse.ArgumentParser(
    description='Return true or false if an instance type is available in a specific availability zone')
parser.add_argument('--az', '-a', help='Specific availability zone')
parser.add_argument('--instancetype', '-i',
                    help='Specific instance type, e.g. t2.micro')
parser.add_argument('--profile', '-p', help='AWS Profile name')


response = ec2.describe_instance_type_offerings(
    DryRun=False,
    LocationType='availability-zone',
    Filters=[
        {
            'Name': 'location',
            'Values': [
                'us-east-1d',
            ]
        },
    ],
)
print('Instance Type Offerings: ')
print(response)
