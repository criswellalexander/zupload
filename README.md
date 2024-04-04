Script to handle large file uploads via Zenodo's API. Uploads via a series of small chunks to prevent temporary request/connection issues from causing a large upload to fail.

You will need:
- a Zenodo repository
- the ID for the Zenodo repo (e.g., for https://zenodo.org/records/7007630 this is 7007630)
- an access token (see https://developers.zenodo.org/#quickstart-upload for how to create this)
- a conda environment with the os, argparse, requests, and tqdm packages (you can use the environment.yml file included in this repo to create one)

Usage: python3 zupload.py [filepath] --id [Zenodo ID] --token [Zenodo access token]

You can avoid specifying --token every time by copying your Zenodo access token into a file named access-token.txt and placing it in this directory.


Known Issues
At time of writing (08/2022) there is a bug that newly-created depositions don't have a bucket at creation. You can create one by uploading any file via the "old" api (see https://github.com/zenodo/zenodo/issues/2286):

url = js['links']['files']
url_full = url + "?access_token=" + ACCESS_TOKEN
files = {'file':open("/path/to/small/test_file.txt",'rb')}
data = {'name':"test_file.txt"}
r = requests.post(url_full,data=data,files=files)

then delete the file from the repo manually.