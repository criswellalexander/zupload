Script to handle large file uploads via Zenodo's API. Uploads via a series of small chunks to prevent temporary request/connection issues from causing a large upload to fail.

You will need:
- a Zenodo repository
- the ID for the Zenodo repo (e.g., for https://zenodo.org/records/7007630 this is 7007630)
- an access token (see https://developers.zenodo.org/#quickstart-upload for how to create this)
- a python virtual environment with the os, argparse, requests, and tqdm packages (you can use the environment.yml file included in this repo to create one via conda/mamba)

Usage: python zupload.py [filepath] --id [Zenodo ID] --token [Zenodo access token]

You can avoid specifying --token every time by copying your Zenodo access token into a file named access-token.txt and placing it in this directory.


Known Issues
At time of writing (08/2022; still present 08/25) there is a bug that newly-created depositions don't have a bucket at creation. As a workaround, if no bucket is found the code will create one by uploading a dummy file via the "old" api (see https://github.com/zenodo/zenodo/issues/2286). You will need to delete the file (dummy_file.txt) from the Zenodo record manually.
