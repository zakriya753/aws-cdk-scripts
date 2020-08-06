from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_autoscaling as asg,
)

class Adl_Asg_Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    def asg_app(self, vpc):
        asg_app= asg.AutoScalingGroup(self, "asg-app",
            vpc=vpc['vpc'],
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=ec2.AmazonLinuxImage(),
            key_name="adl-keypair-dev-us-east-1",
            max_capacity=2
            update_type=asg.UpdateType.ROLLING_UPDATE
        )
        return asg_app
