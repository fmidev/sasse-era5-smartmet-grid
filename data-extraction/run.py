# -*- coding: utf-8 -*-
import sys, os, boto3, time, logging
import datetime as dt
from datetime import timedelta
from urllib.parse import urlparse

template_url = "https://fmi-sasse-cloudformation.s3-eu-west-1.amazonaws.com/timeseries_cloudformation.template"
instance_limit = 40

def add_month(dt0):
    dt1 = dt0.replace(day=1)
    dt2 = dt1 + timedelta(days=32)
    dt3 = dt2.replace(day=1)
    return dt3

def get_instance_count():
    client = boto3.client('ec2')

    custom_filter = [
    {
    'Name':'tag:type',
    'Values': ['sasse-timeseries']
    },
    {
    'Name': 'instance-state-name',
    'Values': ['running']
    }
    ]

    response = client.describe_instances(Filters=custom_filter)
    return len(response['Reservations'])

def terminate_stopped():
    logging.info('Terminating stopped instances...')
    ec2 = boto3.resource('ec2')
    custom_filter = [
    {
    'Name':'tag:type',
    'Values': ['sasse-timeseries']
    },
    {
    'Name': 'instance-state-name',
    'Values': ['stopped']
    }
    ]
    ec2.instances.filter(Filters=custom_filter).terminate()

def delete_complete_stacks():
    logging.info('Deleting stacks...')
    statuses = ['ROLLBACK_COMPLETE', 'CREATE_COMPLETE', 'UPDATE_COMPLETE']
    client = boto3.client('cloudformation')
    cfn = boto3.resource('cloudformation')
    stacks = [stack for stack in cfn.stacks.all() if stack.stack_status in statuses]
    count = 0
    for s in stacks:
        response = client.delete_stack(StackName=s.name)

        # we expect a response, if its missing on non 200 then show response
        if 'ResponseMetadata' in response and \
            response['ResponseMetadata']['HTTPStatusCode'] < 300:
            count += 1
        else:
            logging.critical("There was an Unexpected error. response: {0}".format(json.dumps(response)))

    logging.info('...removed {} stacks'.format(count))


def run(start, end):
    cfn = boto3.client('cloudformation')
    #current_ts = datetime.now().isoformat().split('.')[0].replace(':','-')
    stackname = 'sasse-ts-{}-{}-{}'.format(start.strftime('%Y-%m'), end.strftime('%Y-%m'), os.getpid())
    logging.info('Running stack {}...'.format(stackname))
    capabilities = ['CAPABILITY_IAM', 'CAPABILITY_AUTO_EXPAND']
    try:
        template_params = [{
            "ParameterKey": "ERA5DataYear",
            "ParameterValue": str(start.year)
        },
        {
            "ParameterKey": "ERA5DataMonth",
            "ParameterValue": start.strftime('%m')
        },
        {
            "ParameterKey": "StartTime",
            "ParameterValue": start.strftime('%Y-%m-%dT%H:%M:%S')
        },
        {
            "ParameterKey": "EndTime",
            "ParameterValue": end.strftime('%Y-%m-%dT%H:%M:%S')
        }
        ]
        #print(template_params)
        stackdata = cfn.create_stack(
        StackName=stackname,
        DisableRollback=True,
        TemplateURL=template_url,
        Parameters=template_params,
        Capabilities=capabilities)
    except Exception as e:
        print(str(e))
    return stackdata

def main():
    logging.basicConfig(format=("[%(levelname)s] %(asctime)s %(filename)s:%(funcName)s:%(lineno)s %(message)s"),
                        level=logging.INFO)

    starttime = dt.datetime.strptime('2010-01-01T00:00:00', "%Y-%m-%dT%H:%M:%S")
    endtime = dt.datetime.strptime('2019-01-01T00:00:00', "%Y-%m-%dT%H:%M:%S")

    jobs = []

    start = starttime
    while start < endtime:
        end = add_month(start)
        jobs.append((start, end))
        start = end

    delete_complete_stacks()

    while len(jobs) > 0:
        instance_count = get_instance_count()
        if instance_count < instance_limit:
            logging.info('{}/{} instances running, working...'.format(instance_count, instance_limit))
            terminate_stopped()
            s, e = jobs.pop()
            run(s, e)
            #run(dt.datetime.strptime('2011-03-01T00:00:00', "%Y-%m-%dT%H:%M:%S"),
            #    dt.datetime.strptime('2011-03-31T00:00:00', "%Y-%m-%dT%H:%M:%S"))
        else:
            logging.info('{}/{} instances running, sleeping...'.format(instance_count, instance_limit))
            time.sleep(10*60)

    logging.info('All done. Sleeping 12 hours and cleaning up...')
    time.sleep(60*60*12)
    delete_complete_stacks()
    terminate_stopped()

if __name__ =='__main__':
    main()
