from localstack.utils.aws import aws_models
BrIsV=super
BrIsK=None
BrIsa=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  BrIsV(LambdaLayer,self).__init__(arn)
  self.cwd=BrIsK
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.BrIsa.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,BrIsa,env=BrIsK):
  BrIsV(RDSDatabase,self).__init__(BrIsa,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,BrIsa,env=BrIsK):
  BrIsV(RDSCluster,self).__init__(BrIsa,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,BrIsa,env=BrIsK):
  BrIsV(AppSyncAPI,self).__init__(BrIsa,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,BrIsa,env=BrIsK):
  BrIsV(AmplifyApp,self).__init__(BrIsa,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,BrIsa,env=BrIsK):
  BrIsV(ElastiCacheCluster,self).__init__(BrIsa,env=env)
class TransferServer(BaseComponent):
 def __init__(self,BrIsa,env=BrIsK):
  BrIsV(TransferServer,self).__init__(BrIsa,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,BrIsa,env=BrIsK):
  BrIsV(CloudFrontDistribution,self).__init__(BrIsa,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,BrIsa,env=BrIsK):
  BrIsV(CodeCommitRepository,self).__init__(BrIsa,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
