from localstack.utils.aws import aws_models
rFMYO=super
rFMYI=None
rFMYW=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  rFMYO(LambdaLayer,self).__init__(arn)
  self.cwd=rFMYI
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.rFMYW.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,rFMYW,env=rFMYI):
  rFMYO(RDSDatabase,self).__init__(rFMYW,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,rFMYW,env=rFMYI):
  rFMYO(RDSCluster,self).__init__(rFMYW,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,rFMYW,env=rFMYI):
  rFMYO(AppSyncAPI,self).__init__(rFMYW,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,rFMYW,env=rFMYI):
  rFMYO(AmplifyApp,self).__init__(rFMYW,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,rFMYW,env=rFMYI):
  rFMYO(ElastiCacheCluster,self).__init__(rFMYW,env=env)
class TransferServer(BaseComponent):
 def __init__(self,rFMYW,env=rFMYI):
  rFMYO(TransferServer,self).__init__(rFMYW,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,rFMYW,env=rFMYI):
  rFMYO(CloudFrontDistribution,self).__init__(rFMYW,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,rFMYW,env=rFMYI):
  rFMYO(CodeCommitRepository,self).__init__(rFMYW,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
