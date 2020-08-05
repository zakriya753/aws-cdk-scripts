from aws_cdk import (
    aws_rds as rds,
    core,
)

from .adl_rds_stack import AdlRDS_Cluster_Stack

class AdlRDS_Param_Group(AdlRDS_Cluster_Stack):
    def __init__(self, scope: core.Construct, id: str, vpc, ec2sg, **kwargs) -> None:
        super().__init__(scope, id, vpc, ec2sg, **kwargs)
        
    def rds_aurora_postgres_11_6(self):
        rds_aurora_postgres_11_6= rds.ParameterGroup(
            self,
            "rds-auroraParamGrp-pg-11-6",
            engine= rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_11_6)
            )
        rds_aurora_postgres_11_6.add_parameter("client_encoding", "UTF8")
        return rds_aurora_postgres_11_6

    def rds_aurora_mysql_2_08_1(self):
        rds_aurora_mysql_2_08_1= rds.ParameterGroup(
            self,
            "rds-auroraParamGrp-2-08-01",
            engine= rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_2_08_1)
            )
        rds_aurora_mysql_2_08_1.add_parameter("character_set_client", "utf8")
        return rds_aurora_mysql_2_08_1
        