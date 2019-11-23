import os
import random
import time

import dropbox

from prarxivate.utils import Config


def get_envs():
    envs = {}
    envs['ACCESS_TOKEN'] = os.environ['ACCESS_TOKEN']
    envs['DB_PATH'] = os.environ['DB_PATH']
    envs['REPORT_PATH'] = os.environ['REPORT_PATH']
    envs['wait_time'] = 3
    return envs


def download_db():
    envs = get_envs()
    dbx = dropbox.Dropbox(envs['ACCESS_TOKEN'])
    with open(Config.db_path, 'wb') as f:
        _, resp = dbx.files_download(path=envs['DB_PATH'])
        f.write(resp.content)
    print('success to download')


def upload_db():
    envs = get_envs()
    dbx = dropbox.Dropbox(envs['ACCESS_TOKEN'])
    dst = envs['DB_PATH']
    with open(Config.db_path, 'rb') as f:
        dbx.files_upload(f.read(), dst, mode=dropbox.files.WriteMode.overwrite)
    print('success to upload')


def upload_report():
    envs = get_envs()
    dbx = dropbox.Dropbox(envs['ACCESS_TOKEN'])
    
    reports = os.listdir(Config.report_path)
    assert len(reports) > 1, 'no html files for uploading'
    reports = [r for r in reports if 'html' in r]
    
    for report in reports:
        src = os.path.join(Config.report_path, report)
        dst = envs['REPORT_PATH'] + report
        with open(src, 'rb') as f:
            dbx.files_upload(f.read(), dst, mode=dropbox.files.WriteMode.overwrite)
        print('upload complete {}'.format(report))
        print('Sleeping for {} seconds'.format(envs['wait_time']))
        time.sleep(envs['wait_time'] + random.uniform(0, 3))
