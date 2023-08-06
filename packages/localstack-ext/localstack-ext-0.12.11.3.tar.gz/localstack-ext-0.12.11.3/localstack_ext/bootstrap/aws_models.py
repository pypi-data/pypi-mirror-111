from localstack.utils.aws import aws_models
yzJEG=super
yzJEr=None
yzJEN=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  yzJEG(LambdaLayer,self).__init__(arn)
  self.cwd=yzJEr
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.yzJEN.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,yzJEN,env=yzJEr):
  yzJEG(RDSDatabase,self).__init__(yzJEN,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,yzJEN,env=yzJEr):
  yzJEG(RDSCluster,self).__init__(yzJEN,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,yzJEN,env=yzJEr):
  yzJEG(AppSyncAPI,self).__init__(yzJEN,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,yzJEN,env=yzJEr):
  yzJEG(AmplifyApp,self).__init__(yzJEN,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,yzJEN,env=yzJEr):
  yzJEG(ElastiCacheCluster,self).__init__(yzJEN,env=env)
class TransferServer(BaseComponent):
 def __init__(self,yzJEN,env=yzJEr):
  yzJEG(TransferServer,self).__init__(yzJEN,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,yzJEN,env=yzJEr):
  yzJEG(CloudFrontDistribution,self).__init__(yzJEN,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,yzJEN,env=yzJEr):
  yzJEG(CodeCommitRepository,self).__init__(yzJEN,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
