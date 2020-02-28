# Examples of Using EC2 Describe Instance Type Offerings

Listing AWS Instance Type Offerings by Region and AZ.
[Blog Post](https://aws.amazon.com/blogs/compute/it-just-got-easier-to-discover-and-compare-ec2-instance-types/)

## Prereq

This assumes you have either:

- the AWS CLI installed and configured
  or
- Python installed and configured to use AWS (for .py scripts)
- Powershell installed and configured to use AWS (for .ps1 scripts)

TODO add link to quick starts in the above

## Use Cases

- use case 0: return a list of instances offerings by region (check-instance-type-by-region.py / .ps1)
- Use case 2: pass a specific instance type with region / AZ with and return a true/false if not available (check-instance-type-available.py)
- Use case 3: pass a specific instance type with a region and return a list of AZs (list-instance-type-offering.py)

TODO Stretch Goal

- Create a website that shows the use cases.

## References

### AWS CLI

[CLI Docs](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instance-type-offerings.html)

### API

[API Docs](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstanceTypeOfferings.html)
