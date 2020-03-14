# Arlo Backup

## Motivation
I pay for Arlo Smart/Premium but wish I could access my videos more than 30 days in the past. 
I have tried using the plugged in USB drive in the back of the hub but the way videos are 
loaded onto the drive is unusable compared to the web UI (no proper file names, no way to 
know which video came from which camera, what triggered the recording, etc.).

I don't expect Arlo to provide more free storage. I understand storage of video costs money so
I am using this repo to download **my** videos and save them locally to my NAS.

## Attribution
This project wouldn't be possible without https://github.com/jeffreydwalter/arlo.

## Setup

### Environment
Required environment variables:
- REQUIREMENTS_FILE - Path to the requirements.txt file on the system (usually just set to 'requirements.txt')
- ARLO_USERNAME - Arlo account username to login with
- ARLO_PASSWORD - Arlo account password to login with
- ARLO_BACKUP_USER - Name of user of the server that videos will be saved to
- ARLO_BACKUP_IP - Local IP of the server that videos will be saved to
- ARLO_BACKUP_DIR_PATH - The path that a new video directory should be created at
- ARLO_BACKUP_UPLOAD_PATH - The base path that the videos should be uploaded to
- GIT_URL - Required **only if** using Jenkins and pulling the repo on each run

Note: ARLO_BACKUP_DIR_PATH and ARLO_BACKUP_UPLOAD_PATH will likely be the same. 
If using a Synology or other consumer NAS they may be different paths.

### Python
- Written using Python 3 (3.8). This is not guaranteed to work on python 2 or future python versions.
- Required python libraries are listed in requirements.txt

### SSH/Rsync
This repo uses sshkey based authentication to allow server to server communication without requiring inputting passwords.

### Jenkins setup
This repo is being used with a Jenkins instance for ease of use and traceability. Jenkins is not required to run this repo.

1. Setup a Jenkins pipeline
2. Set the project as 'parameterized'
3. Add in the environment variables above as parameters (string/password parameters)
4. Set the build trigger to 'Build periodically'. Set your appropriate cron schedule.
5. Set the pipeline to pull from Git via SCM. Use this repo or your forked repo for the URL.

Test and adjust.

### Cron
This repo can be run using only cron by setting a schedule to trigger the arlo_backup.bash 
file and setting the appropriate ENV variables.

## Troubleshooting
- If SSH or rsync is failing be sure you have the necessary packages installed on each machine (the machine pulling the data and the machine receiving the data)
- If SSH or rsync is failing after both sides are setup you should enable passwordless SSH via ssh keys. There are plenty of guides online to setup sshkey login.
- This repo likely cannot be run within a docker container due to the ssh/passwordless requirements.