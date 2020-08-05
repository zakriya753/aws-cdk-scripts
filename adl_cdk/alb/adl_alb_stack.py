from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
)

class Adl_Alb_Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
    def alb_app(self, vpc, alb_name="adl_lb"):
        alb_app= elbv2.ApplicationLoadBalancer(
            self,
            "alb" + alb_name,
            http2_enabled= True,
            vpc= vpc['vpc'],
            deletion_protection= False,
            internet_facing= True,
            load_balancer_name= alb_name,
            vpc_subnets= ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            )
        )
        return alb_app 
        
    def alb_listener(self, alb, vpc, alb_port, alb_cert=None):
        alb_listener= elbv2.ApplicationListener(
            self,
            "alb-listener",
            load_balancer= alb,
            certificate_arns= alb_cert,
            open= True,
            default_target_groups= [elbv2.ApplicationTargetGroup(
                self,
                "alb-default-tg",
                port= alb_port,
                vpc= vpc['vpc']
                )],
            port= alb_port
        )
        return alb_listener

    def alb_tg(self, vpc, alb_tg_port=None, targets=None, adl_tg_name=None):
        alb_tg= elbv2.ApplicationTargetGroup(
            self,
            "alb-tg" + adl_tg_name,
            port= alb_tg_port,
            target_group_name= adl_tg_name,
            vpc= vpc['vpc'],
            targets= targets
        )
        return alb_tg
    
