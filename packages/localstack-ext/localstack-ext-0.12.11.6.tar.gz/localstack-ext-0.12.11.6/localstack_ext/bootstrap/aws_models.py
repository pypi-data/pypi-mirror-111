from localstack.utils.aws import aws_models
IOpYg=super
IOpYF=None
IOpYL=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  IOpYg(LambdaLayer,self).__init__(arn)
  self.cwd=IOpYF
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.IOpYL.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,IOpYL,env=IOpYF):
  IOpYg(RDSDatabase,self).__init__(IOpYL,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,IOpYL,env=IOpYF):
  IOpYg(RDSCluster,self).__init__(IOpYL,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,IOpYL,env=IOpYF):
  IOpYg(AppSyncAPI,self).__init__(IOpYL,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,IOpYL,env=IOpYF):
  IOpYg(AmplifyApp,self).__init__(IOpYL,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,IOpYL,env=IOpYF):
  IOpYg(ElastiCacheCluster,self).__init__(IOpYL,env=env)
class TransferServer(BaseComponent):
 def __init__(self,IOpYL,env=IOpYF):
  IOpYg(TransferServer,self).__init__(IOpYL,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,IOpYL,env=IOpYF):
  IOpYg(CloudFrontDistribution,self).__init__(IOpYL,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,IOpYL,env=IOpYF):
  IOpYg(CodeCommitRepository,self).__init__(IOpYL,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
