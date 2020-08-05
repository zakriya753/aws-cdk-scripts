from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_iam as iam,
)
linux = ec2.MachineImage.generic_linux({
    "us-east-1": "ami-0ac80df6eff0e70b5"})

class AdlEC2Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, props_vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        role = iam.Role(self, "ec2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )   

        role.add_to_policy(iam.PolicyStatement(
            resources=["*"],
            actions=["s3:*"]
        ))
        
        ec2_security_group = ec2.SecurityGroup(
            self, "sg-ec2",
            vpc=props_vpc['vpc'],
            security_group_name= 'adl-ec2-sg'
        )
        bastion = ec2.Instance(
            self,
            "ubuntu-bastion",
            vpc=props_vpc['vpc'],
            machine_image=linux,
            key_name="adl-keypair-dev-us-east-1",
            instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"),
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            instance_name='adl-bastion-test',
            role=role,
            #security_group=ssh_security_group
        )

        # Connections
        bastion.add_security_group(ec2_security_group)
        bastion.connections.allow_from_any_ipv4(ec2.Port.tcp(22), 'Allow inbound SSH')
        bastion.connections.allow_from_any_ipv4(ec2.Port.tcp(8080), 'Allow inbound HTTP')
        for ssh_sg in bastion.connections.security_groups:
            ec2_security_group.connections.allow_from(ssh_sg, ec2.Port.all_tcp(), "SSH Access to EC2 Group")


         # Outputs
        props_ec2= {"namespace": "ec2_props"}
        self.output_props_ec2 = props_ec2.copy()
        self.output_props_ec2['ec2-sg'] = ec2_security_group

    @property
    def outputs_ec2(self):
        return self.output_props_ec2
