#!/usr/bin/env python3

from aws_cdk import core

from adl_cdk.vpc.adl_vpc_stack import AdlVPCStack
from adl_cdk.ec2.adl_ec2_stack import AdlEC2Stack 
from adl_cdk.rds.adl_rds_stack import AdlRDS_Cluster_Stack
#from adl_cdk.rds.adl_rds_stack import AdlRDS_Param_Group
from adl_cdk.rds.adl_rds_param_group_stack import AdlRDS_Param_Group 
from adl_cdk.alb.adl_alb_stack import Adl_Alb_Stack

app = core.App()
props_vpc = {'namespace': 'vpc_stack'}
vpc_stack = AdlVPCStack(app, "adl-vpc", props_vpc, env={'region': 'us-east-1'}, tags={'productCode': 'adl'})
ec2_stack = AdlEC2Stack(app, "adl-ec2", vpc_stack.outputs_vpc, env={'region': 'us-east-1'}, tags={'productCode': 'adl'})
# RDS_Aurora_PSQL - Uncomment lines to launch RDS
rds_param_psql = AdlRDS_Param_Group(app, 'adl-rds-psql', vpc_stack.outputs_vpc, ec2_stack.outputs_ec2, env={'region': 'us-east-1'}, tags={'productCode': 'adl'} )
rds_param_psql.rds_cluster(vpc_stack.outputs_vpc, ec2_stack.outputs_ec2, "AURORA_POSTGRESQL", rds_param_psql.rds_aurora_postgres_11_6())
# RDS_Aurora_MYSQL
#rds_param_msql = AdlRDS_Param_Group(app, 'adl-rds-msql', vpc_stack.outputs_vpc, ec2_stack.outputs_ec2, env={'region': 'us-east-1'}, tags={'productCode': 'adl'} )
#rds_param_msql.rds_cluster(vpc_stack.outputs_vpc, ec2_stack.outputs_ec2, "AURORA_MYSQL", rds_param_msql.rds_aurora_mysql_2_08_1())
# Simple Aurora
#rds_stack_aurora = AdlRDS_Cluster_Stack(app, "adl-rds-aurora", vpc_stack.outputs_vpc, ec2_stack.outputs_ec2, 'AURORA', env={'region': 'us-east-1'}, tags={'productCode': 'adl'})

alb = Adl_Alb_Stack(app, "adl-alb", env={'region': 'us-east-1'}, tags={'productCode': 'adl'})
alb_app= alb.alb_app(vpc_stack.outputs_vpc)
alb_listner= alb.alb_listener(alb_app, vpc_stack.outputs_vpc, alb_port=80)
app.synth() 
