from localstack.utils.aws import aws_models
QzGtH=super
QzGtV=None
QzGtY=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  QzGtH(LambdaLayer,self).__init__(arn)
  self.cwd=QzGtV
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.QzGtY.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,QzGtY,env=QzGtV):
  QzGtH(RDSDatabase,self).__init__(QzGtY,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,QzGtY,env=QzGtV):
  QzGtH(RDSCluster,self).__init__(QzGtY,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,QzGtY,env=QzGtV):
  QzGtH(AppSyncAPI,self).__init__(QzGtY,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,QzGtY,env=QzGtV):
  QzGtH(AmplifyApp,self).__init__(QzGtY,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,QzGtY,env=QzGtV):
  QzGtH(ElastiCacheCluster,self).__init__(QzGtY,env=env)
class TransferServer(BaseComponent):
 def __init__(self,QzGtY,env=QzGtV):
  QzGtH(TransferServer,self).__init__(QzGtY,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,QzGtY,env=QzGtV):
  QzGtH(CloudFrontDistribution,self).__init__(QzGtY,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,QzGtY,env=QzGtV):
  QzGtH(CodeCommitRepository,self).__init__(QzGtY,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
