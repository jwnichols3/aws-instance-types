# TODO add logic to test if AWS (or AWS2) is installed
export AWS_REGION=`aws configure get region`
echo ALL INSTANCE TYPES FOR $AWS_REGION
aws ec2 describe-instance-type-offerings

echo CURRENT INSTANCE TYPES FOR $AWS_REGION
aws ec2 describe-instance-types  --filter Name=current-generation,Values=true