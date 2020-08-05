from aws_cdk import (
    aws_ec2 as ec2,
    core,
)

class AdlVPCStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, props_vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        subnet1 = ec2.SubnetConfiguration(
            name='public-subnet',
            subnet_type=ec2.SubnetType.PUBLIC,
            cidr_mask=24)
        subnet2 = ec2.SubnetConfiguration(
            name='private-subnet',
            subnet_type=ec2.SubnetType.PRIVATE,
            cidr_mask=20
        )    
        vpc = ec2.Vpc(
            self,
            "adl-test-vpc",
            cidr='10.0.0.0/16',
            enable_dns_hostnames=True,
            enable_dns_support=True,
            max_azs=2,
            nat_gateway_provider=ec2.NatProvider.gateway(),
            nat_gateways=2,
            subnet_configuration=[subnet1,subnet2]
        )
        core.CfnOutput(self, "vpcid",
        value=vpc.vpc_id)

        # Outputs 
        self.output_props_vpc = props_vpc.copy()
        self.output_props_vpc['vpc'] = vpc
        self.output_props_vpc['subnets'] = vpc.public_subnets

    @property
    def outputs_vpc(self):
        return self.output_props_vpc
    




        