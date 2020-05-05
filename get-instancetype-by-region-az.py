import boto3
import sys
import getopt
import time

print("-----------------------------------------------------------------------------")
print("Sample code as a suggestion how to list out instance availability by AZ")
print("Do not use in production wthout reviewing -- for demonstration purposes only")
print("-----------------------------------------------------------------------------")
time.sleep(3)

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "h:r", ["region="])
except getopt.GetoptError:
    print('get-instancetype-by-region-az.py --region <region>')
    sys.exit(2)
if not argv:
    print("No parameters entered at runtime - use following parameters to run script")
    print('get-instancetype-by-region-az.py --region us-east-1')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print("Use following parameters to run script")
        print('get-instancetype-by-region-az.py - -region us-east-1')
        sys.exit()
    elif opt in ("-r", "--region"):
        region = arg

strFile = str("InstanceTypeByAZFor_"+region+".csv")

file = open(strFile, "a+")
file.write("InstanceType,AZ")
file.write("\n")

ec2 = boto3.client('ec2', region_name=region)
instancetypes = ec2.describe_instance_types()

arrinstancetypes = instancetypes[u'InstanceTypes']

for arrinstancetype in arrinstancetypes:
    instancetype = arrinstancetype['InstanceType']

    response = ec2.describe_instance_type_offerings(
        LocationType='availability-zone',
        Filters=[
            {
                'Name': 'instance-type',
                'Values': [
                    instancetype
                ]
            }
        ]
    )

    outputs = response[u'InstanceTypeOfferings']
    for output in outputs:
        AZ = output['Location']
        stroutline = str(instancetype + "," + AZ)
        print(instancetype + "," + AZ)
        file.write(stroutline)
        file.write("\n")

file.close()
