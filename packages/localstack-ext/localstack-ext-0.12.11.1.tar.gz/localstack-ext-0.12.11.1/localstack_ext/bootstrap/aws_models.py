from localstack.utils.aws import aws_models
zfSWY=super
zfSWk=None
zfSWX=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  zfSWY(LambdaLayer,self).__init__(arn)
  self.cwd=zfSWk
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.zfSWX.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,zfSWX,env=zfSWk):
  zfSWY(RDSDatabase,self).__init__(zfSWX,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,zfSWX,env=zfSWk):
  zfSWY(RDSCluster,self).__init__(zfSWX,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,zfSWX,env=zfSWk):
  zfSWY(AppSyncAPI,self).__init__(zfSWX,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,zfSWX,env=zfSWk):
  zfSWY(AmplifyApp,self).__init__(zfSWX,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,zfSWX,env=zfSWk):
  zfSWY(ElastiCacheCluster,self).__init__(zfSWX,env=env)
class TransferServer(BaseComponent):
 def __init__(self,zfSWX,env=zfSWk):
  zfSWY(TransferServer,self).__init__(zfSWX,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,zfSWX,env=zfSWk):
  zfSWY(CloudFrontDistribution,self).__init__(zfSWX,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,zfSWX,env=zfSWk):
  zfSWY(CodeCommitRepository,self).__init__(zfSWX,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
