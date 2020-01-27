import boto3

ec2 = boto3.client('ec2')

# Retrieves all regions/endpoints that work with EC2
response = ec2.describe_regions()
print('Regions:', response['Regions'])

# Retrieves availability zones only for region of the ec2 object
response = ec2.describe_availability_zones()
print('Availability Zones:', response['AvailabilityZones'])

response = ec2.describe_instance_type_offerings()
print('Instance Type Offerings: ')
print(response)
#print('Instance Type Offerins:', response['InstanceTypeOffering'])
