# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 15:11:18 2022

@author: Alexander Criswell <alexander.criswell@ligo.org>

Quick script to upload files to Zenodo because the Zenodo api is garbage

Chunking with the tqdm progressbar helps avoid connection/request issues.

Usage: python3 zupload.py [filepath] --id [Zenodo ID] --token [Zenodo access token]

If only the filepath is provided, zupload will try to grab the access token from access-token.txt in the current directory.
"""

import os
import argparse
import requests
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper





if __name__ == '__main__':
    
    ## set up argparser
    parser = argparse.ArgumentParser(description='Run zupload.py')
    parser.add_argument('filepath', type=str, help='/path/to/data/file/for/upload.ext')
    parser.add_argument('--id', type=str, help='Zenodo deposit ID, e.g. 7007630 if your Zenodo deposit url is https://zenodo.org/api/deposit/depositions/7007630/', default='7007630') # default is my paper repo b/c I'm lazy
    parser.add_argument('--token', type=str, help='Zenodo access token. If unspecified, will be loaded from access-token.txt in the current directory.', default=None)
    args = parser.parse_args()
    if args.token is None:
        if not os.path.isfile('access-token.txt'):
            raise ValueError("Must either provide access token as string at the command line or within access-token.txt file in current directory.")
        with open('access-token.txt',"r") as tf:
            ACCESS_TOKEN = tf.read()
    else:
        ACCESS_TOKEN = args.token
    
    ## set file path
    filepath = args.filepath
    ## separate out filename
    filename = filepath.split('/')[-1]
    
    ## set access token in params dict
    params={'access_token': ACCESS_TOKEN}

    ## grab Zenodo deposits and select correct deposition
    zlist = requests.get('https://zenodo.org/api/deposit/depositions',params=params)
    js = None
    for deposit in zlist.json():
        if str(deposit['id']) == args.id:
            js = deposit
            break
    if js is None:
        raise ValueError("No deposits exist with provided ID.")
    
    ## get bucket
    ## at time of writing there is a bug that newly-created depositions don't have a bucket at creation
    ## you can create one by uploading any file via the "old" api:
    ## (see https://github.com/zenodo/zenodo/issues/2286)
    ## url = js['links']['files']
    ## url_full = url + "?access_token=" + ACCESS_TOKEN
    ## files = {'file':open("/path/to/small/test_file.txt",'rb')}
    ## data = {'name':"test_file.txt"}
    ## r = requests.post(url_full,data=data,files=files)
    ## then delete the file manually
    
    ## anyway. get the bucket!
    bucket = js['links']['bucket']
    
    ## get file size (for progress bar/chunking)
    file_size = os.stat(filepath).st_size
    
    ## do the thing! this uploads by chunks while providing a readable progress bar
    with open(filepath,"rb") as fp:
        with tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
            wrapped_file = CallbackIOWrapper(t.update, fp, "read")
            r = requests.put("%s/%s" % (bucket,filename), data=wrapped_file, params=params)
    
    print("Done!")



































