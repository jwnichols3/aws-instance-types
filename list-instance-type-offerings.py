""" 
list-instance-type-offerings.py --region region_name --instancetype instance_type --profile profile_name  

example
python list-instance-type-offerings.py \
    --instance-type t3.micro \
    --region us-east-1 \
    --profile default  

Goal: Lists the availability of a specific type in each availability zone within the given region

    Availability of t3.micro in the us-east-1 region:
    t3.micro us-east-1a Yes
    t3.micro us-east-1b Yes
    t3.micro us-east-1c Yes
    t3.micro us-east-1d Yes
    t3.micro us-east-1e No


TODO: check for environment variable, re default region if region is not provided
TODO: Add debug option with logging (https://docs.python.org/3/howto/logging.html)
TODO: Add test suite using a framework like PyTest
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
parser.add_argument('--instancetype', '-i', default='t2.micro',
                    help='Specific instance type, e.g. t2.micro')
parser.add_argument('--region', '-r', default='us-east-1',
                    help='The AWS region, e.g. us-east-1')
parser.add_argument('--profile', '-p', help='AWS Profile name')

args = parser.parse_args()
instancetype = args.instancetype.lower()
region = args.region.lower()
profile = args.profile

if not (region):
    region = 'us-east-1'


'''
############################################################
################## USER DEFINED FUNCTIONS ##################
############################################################
'''


def check_region(region):
    '''
    check_region(region) returns True if the region is valid, False if the region is invalid.
    '''
    sess = Session(profile_name=profile, region_name='us-east-1')
    ec2 = sess.client('ec2')

    # ERROR CHECKING INPUT
    # Retrieves all regions/endpoints and checks against input value region
    region_list = ec2.describe_regions()['Regions']
    region_names = []
    for i in region_list:
        region_names.append(i['RegionName'])

    if not region in region_names:
        return False
    else:
        return True


def get_az_list(region):
    '''
    get_az_list(region) returns a list of availability zones in the specified region
    '''
    sess = Session(profile_name=profile, region_name=region)
    ec2 = sess.client('ec2')

    local_az_list = ec2.describe_availability_zones()['AvailabilityZones']
    local_az_names = []
    for i in local_az_list:
        local_az_names.append(i['ZoneName'])

    return local_az_names


def get_instance_list(instancetype, region):
    '''
    get_instance_list(instancetype, region) returns a list of AZs that have that instance
    '''
    # The AZ Location is not filtering the response to just the specified AZ.
    # The payload has a list of all AZs where the instance is available.
    # This results in a set of logic later in the script.
    sess = Session(profile_name=profile, region_name=region)
    ec2 = sess.client('ec2')

    local_response = ec2.describe_instance_type_offerings(
        LocationType='availability-zone',
        Filters=[
            {
                'Name': 'instance-type',
                'Values': [
                    instancetype,
                ]
            },
        ],
    )

    # Extract the DICT to a LIST and make the code more readable
    instance_offerings = local_response['InstanceTypeOfferings']

    # Populate a list to search. Because the filter in the describe_instance_type_offerings call
    # returns all AZs, a second logic check is required.
    local_instance_list = []
    for i in instance_offerings:
        local_instance_list.append(i['Location'])

    return local_instance_list


def list_intersection(lst1, lst2):
    '''
    list_intersection(list1, list2) returns a list with the common elements between the two lists
    '''
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def list_diff(li1, li2):
    '''
    list_diff(list1, list2) returns a list with the elements that are not in both lists
    '''
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


'''
############################################################
################## USER DEFINED FUNCTIONS ##################
############################################################
'''

if not check_region(region):
    print('Error: region ' + region + ' not a valid AWS region')
    sys.exit(2)

# Get a list of AZs in REGION
az_list = get_az_list(region)

# Get the list of AZs that have a defined instance type
az_instancetype_list = get_instance_list(instancetype, region)

instance_found = list_intersection(az_list, az_instancetype_list)
instance_not_found = list_diff(az_list, az_instancetype_list)

print('The instance type ' + instancetype +
      ' is found in the following AZs in region ' + region + ':')
print(*instance_found, sep='\n')
print('The instance type ' + instancetype +
      ' is NOT found in the following AZs in region ' + region + ':')
print(*instance_not_found, sep='\n')
