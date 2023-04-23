#Turn on hyperv for vagrant.
New-VMSwitch -SwitchName "NAT" -SwitchType Internal
New-NetIPAddress -IPAddress 192.168.10.1 -PrefixLength 24 -InterfaceAlias "vEthernet (NAT)"
New-NetNat -Name NAT -InternalIPInterfaceAddressPrefix 192.168.10.0/24
Enable-PSRemoting -Force  -SkipNetworkProfileCheck
Enable-WSManCredSSP -Role Server –Force
Enable-WSManCredSSP -Role Client -DelegateComputer * -Force
Start-service winrm
Set-Item "wsman:\localhost\client\trustedhosts" -Value "*" -Force
