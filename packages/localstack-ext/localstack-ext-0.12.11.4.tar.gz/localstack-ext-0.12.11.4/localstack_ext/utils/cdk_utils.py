#!/usr/bin/env python

import re
import os
import sys
import glob
import json
from localstack.utils.aws import aws_stack
from localstack.utils.common import load_file
from localstack.utils.testutil import create_zip_file


def read_templates():
    files = glob.glob('*.template.json')
    main_file = [f for f in files if 'nested.' not in f][0]
    nested_file = ([f for f in files if 'nested.' in f] or [None])[0]
    print('Loading files: %s' % files)
    main_template = json.loads(load_file(main_file))
    nested_template = json.loads(load_file(nested_file)) if nested_file else {}
    return main_template, nested_template


def deploy_stack(main_template, nested_template):
    assets = {}
    stack_params = {}
    cdk_bucket = 'cdk-assets-1'
    s3_client = aws_stack.connect_to_service('s3')
    cf_client = aws_stack.connect_to_service('cloudformation')
    s3_client.create_bucket(Bucket=cdk_bucket)

    params = main_template.get('Parameters', {})
    for param, details in params.items():
        desc = details.get('Description') or ''
        asset_id = re.sub(r'.*for asset (version )?"?([^"]+)"?', r'\2', desc).strip(' "')
        assets[asset_id] = assets.get(asset_id) or {}
        if 'S3 key for asset' in desc:
            stack_params[param] = 'assets/||%s.zip' % asset_id
            asset_dir = 'asset.%s' % asset_id
            if os.path.exists(asset_dir):
                # upload asset as zip file
                asset_content = create_zip_file(asset_dir, get_content=True)
            else:
                # assuming for now that his refers to the nested template file itself
                asset_content = json.dumps(nested_template)
            s3_client.put_object(Bucket=cdk_bucket, Key='assets/%s.zip' % asset_id, Body=asset_content)
        if 'S3 bucket for' in desc:
            stack_params[param] = cdk_bucket

    params = [{'ParameterKey': k, 'ParameterValue': v} for k, v in stack_params.items()]
    response = cf_client.create_stack(StackName='cf-stack1',
        TemplateBody=json.dumps(main_template), Parameters=params)
    print('Deployed new stack ID:', response['StackId'])


def deploy_cdk_stack():
    root_path = os.path.realpath(os.path.join(os.path.realpath(os.path.dirname(__file__)), '..', '..'))
    sys.path.append(root_path)
    main_template, nested_template = read_templates()
    deploy_stack(main_template, nested_template)


def main():
    args = sys.argv[1:]
    if not args:
        print('Add "deploy" argument to deploy a CDK stack from within a "cdk.out" folder')
    elif args[0] == 'deploy':
        deploy_cdk_stack()


if __name__ == '__main__':
    main()
