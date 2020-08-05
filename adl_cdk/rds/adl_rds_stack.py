from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    core,
)

class AdlRDS_Cluster_Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, vpc, ec2sg, rds_type="AURORA", **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.rds_cluster(vpc, ec2sg, rds_type)
    def rds_cluster(self, vpc, ec2sg, rds_type, rds_param=None):
        postgres = rds.DatabaseCluster(
            self,
            "adl-" + rds_type,
            default_database_name= "adldb",
            engine= getattr(rds.DatabaseClusterEngine, rds_type),
            instance_props= rds.InstanceProps(
                vpc=vpc['vpc'],
                vpc_subnets= ec2.SubnetSelection(
                    subnet_type= ec2.SubnetType.PRIVATE),
                instance_type= ec2.InstanceType(instance_type_identifier="t3.medium")
                ),
            master_user= rds.Login(username="adldevuser"),
            backup= rds.BackupProps(retention=core.Duration.days(7), preferred_window='01:00-02:00'),
            parameter_group= rds_param,
            preferred_maintenance_window= "Sun:23:45-Mon:00:15",
            removal_policy= core.RemovalPolicy.DESTROY,
            storage_encrypted= True
        )
        postgres.connections.allow_from(ec2sg['ec2-sg'], ec2.Port.all_tcp())                        
        