from localstack.utils.aws import aws_models
pGrFY=super
pGrFd=None
pGrFe=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  pGrFY(LambdaLayer,self).__init__(arn)
  self.cwd=pGrFd
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.pGrFe.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,pGrFe,env=pGrFd):
  pGrFY(RDSDatabase,self).__init__(pGrFe,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,pGrFe,env=pGrFd):
  pGrFY(RDSCluster,self).__init__(pGrFe,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,pGrFe,env=pGrFd):
  pGrFY(AppSyncAPI,self).__init__(pGrFe,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,pGrFe,env=pGrFd):
  pGrFY(AmplifyApp,self).__init__(pGrFe,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,pGrFe,env=pGrFd):
  pGrFY(ElastiCacheCluster,self).__init__(pGrFe,env=env)
class TransferServer(BaseComponent):
 def __init__(self,pGrFe,env=pGrFd):
  pGrFY(TransferServer,self).__init__(pGrFe,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,pGrFe,env=pGrFd):
  pGrFY(CloudFrontDistribution,self).__init__(pGrFe,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,pGrFe,env=pGrFd):
  pGrFY(CodeCommitRepository,self).__init__(pGrFe,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
