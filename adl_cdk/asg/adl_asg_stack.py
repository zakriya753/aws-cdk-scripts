from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_autoscaling as asg,
    aws_iam as iam, 
)

class Adl_Asg_Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    def asg_app(self, vpc, asg_name):
        asg_app= asg.AutoScalingGroup(self, f"asg-app{asg_name}",
            vpc=vpc['vpc'],
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=ec2.AmazonLinuxImage(),
            key_name="adl-keypair-dev-us-east-1",
            max_capacity=2
            update_type=asg.UpdateType.ROLLING_UPDATE
        )
        asg_app.add_to_role_policy(statement=iam.PolicyStatement(
          resources=["*"]
          actions=[s3:*]))
        return asg_app
