import json
import boto3
import logging
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def aws_create_tag(_aws_region, _instance_id: str, _key_name: str, _tag_value: str):
    try:
        client = boto3.client('ec2', region_name=_aws_region)
        client.create_tags(Resources=[_instance_id, ], Tags=[{'Key': _key_name, 'Value': _tag_value}, ])
        logging.info(f'successfuly created tag {_key_name} for instance {_instance_id}')
    except ClientError:
        logging.info(str(ClientError))
        return False
    return True


def lambda_handler(event, context):
    if 'detail' in event:
        try:
            if 'userIdentity' in event['detail']:
                map_casino_id = 'd-server-00a0b1flwu6pb1'
                map_app_id = 'infra-rubrik'
                if event['detail']['userIdentity']['type'] == 'AssumedRole':
                    user_name = str('Username: ' + event['detail']['userIdentity']['principalId'].split(':')[1] + ' with Role: ' + event['detail']['userIdentity']['sessionContext']['sessionIssuer']['userName'])
                elif event['detail']['userIdentity']['type'] == 'IAMUser':
                    user_name = event['detail']['userIdentity']['userName']
                elif event['detail']['userIdentity']['type'] == 'Root':
                    user_name = 'root'
                else:
                    logging.info('Could not determine username (unknown iam userIdentity) ')
                    user_name = ''
            else:
                logging.info('Could not determine username (no userIdentity data in cloudtrail')
                user_name = ''
        except Exception as e:
            logging.info('could not find username, exception: ' + str(e))
            user_name = ''
        try:
            instance_id = [x['instanceId'] for x in event['detail']['responseElements']['instancesSet']['items']]
        except Exception as e:
            instance_id = []
        aws_region = event['detail']['awsRegion']
        client = boto3.client('ec2', region_name=aws_region)
        if instance_id:
            for instance in instance_id:
                # Let's tag the instance
                instance_api = client.describe_instances(InstanceIds=[instance])
                # Get all ec2 instance tags
                if 'Tags' in instance_api['Reservations'][0]['Instances'][0]:
                    instance_tags = instance_api['Reservations'][0]['Instances'][0]['Tags']
                else:
                    instance_tags = []
                # Check if 'Name' tag is exist for ec2 instance
                # If not, feed the custom username for tracking who created the instance(s)
                if instance_tags:
                    instance_name = [x['Value'] for x in instance_tags if x['Key'] and x['Key'] == 'Name']
                    if instance_name:
                        instance_name = instance_name[0]
                else:
                    instance_name = user_name
                # Check if the MAP relevant tags exist in instance tags
                if instance_tags:
                    if not any(keys.get('Key') == 'map-migrated' for keys in instance_tags):
                        logging.info(f'Tag "map-migrated" does not exist for instance {instance}, creating...')
                        aws_create_tag(aws_region, instance, 'map-migrated', map_casino_id)
                    if not any(keys.get('Key') == 'map-migrated-app' for keys in instance_tags):
                        logging.info(f'Tag "map-migrated-app" does not exist for instance {instance}, creating...')
                        aws_create_tag(aws_region, instance, 'map-migrated-app', map_app_id)
                    else:
                        logging.info(f'All the required MAP tags already exist for instance {instance}')
                else:
                    logging.info(f'Instance {instance} has no tags, let\'s tag it with all the MAP relevant tags')
                    aws_create_tag(aws_region, instance, 'map-migrated', map_casino_id)
                    aws_create_tag(aws_region, instance, 'map-migrated-app', map_app_id)
                # Let's tag the instance volumes
                instance_volumes = [x['Ebs']['VolumeId'] for x in instance_api['Reservations'][0]['Instances'][0]['BlockDeviceMappings']]
                # Check if volume already has tags
                for volume in instance_volumes:
                    response = client.describe_volumes(VolumeIds=[volume])
                    volume_tags = [x['Tags'] for x in response['Volumes'] if 'Tags' in x]
                    if volume_tags:
                        if not any(keys.get('Key') == 'map-migrated' for keys in volume_tags[0]):
                            logging.info('Tag "map-migrated" does not exist, creating...')
                            aws_create_tag(aws_region, volume, 'map-migrated', map_casino_id)
                        if not any(keys.get('Key') == 'map-migrated-app' for keys in volume_tags[0]):
                            logging.info('Tag "map-migrated-app" does not exist, creating...')
                            aws_create_tag(aws_region, volume, 'map-migrated-app', map_app_id)
                        if not any(keys.get('Key') == 'AttachedInstance' for keys in volume_tags[0]):
                            logging.info('Tag "AttachedInstance" does not exist, creating...')
                            aws_create_tag(aws_region, volume, 'AttachedInstance', instance + ' created by ' + str(instance_name))
                    else:
                        logging.info(f'volume {volume} has no tags, let\'s tag it with all the MAP relevant tags')
                        aws_create_tag(aws_region, volume, 'map-migrated', map_casino_id)
                        aws_create_tag(aws_region, volume, 'map-migrated-app', map_app_id)
                        aws_create_tag(aws_region, volume, 'AttachedInstance', instance + ' created by ' + str(instance_name))
            return {
                'statusCode': 200,
                'body': json.dumps('All Done!')
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps('No Data!')
            }
