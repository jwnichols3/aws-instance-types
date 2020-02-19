Import-Module AWSPowerShell.NetCore

$region       = Read-Host "Enter Region: "
$instanceType = Read-Host "Enter Instance Type: "
Write-Host ""
Write-Host "Grabbing region/instance info..." -Foregroundcolor Yellow
Write-Host ""

$filter = @{
    'name' = 'instance-type'
    'values' = $instanceType
}

#$results = Get-EC2InstanceTypeOffering -LocationType availability-zone -Region $region
$results = Get-EC2InstanceTypeOffering -LocationType availability-zone -Region $region -Filter $filter

Write-Host "AZ Availability for "$instanceType":"
ForEach($result in $results)
{
    $result.Location
}