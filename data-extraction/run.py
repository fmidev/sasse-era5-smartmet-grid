# -*- coding: utf-8 -*-
import sys, os, boto3, time, logging
import datetime as dt
from datetime import timedelta
from urllib.parse import urlparse

template_url = "https://fmi-sasse-cloudformation.s3-eu-west-1.amazonaws.com/timeseries_cloudformation.template"
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
        "ParameterValue": str(start.month)
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

    while len(jobs) > 0:
        if get_instance_count() < 10:
            logging.info('Under 10 instances running, working...')
            terminate_stopped()
            s, e = jobs.pop()
            run(s, e)
        else:
            logging.info('10 or more instances running, sleeping...')
            time.sleep(10*60)


if __name__ =='__main__':
    main()
