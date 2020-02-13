""" 
check-instance-type-availability.py --instance-type instance_type --az availability_zone --profile profile_name  

example
python check-instance-type-availability.py \
    --instance-type t3.micro \
    --az us-east-1d \
    --profile default  

Goal: Returns True if instance type is available

#TODO: parameterize the command inputs.
TODO: variables in the Filter of describe_instance_type_offerings
TODO: search the response for the correspond instance type.
"""

from boto3 import Session
from botocore.exceptions import ClientError
from pprint import pprint
import sys
import getopt

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(
        argv, "hi:r:", ["instancetype=", "region="])
except getopt.GetoptError:
    print('check-instance-type-availability.py -i <instancetype> -r <region>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('check-instance-type-availability.py -i <instancetype> -r <region>')
        sys.exit()
    elif opt in ("-i", "--instancetype"):
        instancetype = arg
    elif opt in ("-r", "--region"):
        region = arg

sess = Session(profile_name='default', region_name=region)
ec2 = sess.client('ec2')

response = ec2.describe_instance_type_offerings(
    LocationType='availability-zone',
    Filters=[
        {
            'Name': 'instance-type',
            'Values': [
                #'t3.medium'
                instancetype
            ]
        }
    ]
)

outputs = response[u'InstanceTypeOfferings']
print(instancetype + " available in following Availability Zones:")
for output in outputs:
    Loc = output['Location']
    print(Loc)

#print('Instance Type Offerings: ')
#pprint(response)
