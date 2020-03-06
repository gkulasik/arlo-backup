#!/bin/bash
set -uo pipefail

date_formatted=$(date +'%Y.%m.%d')
echo "Backup starting for date: $date_formatted"

# Make directory for python script to use
echo "Creating /videos directory if not exists..."
mkdir -p videos

echo "Installing needed python packages if not exists..."
pip install -r ${REQUIREMENTS_FILE};

echo "Starting python script"
python3 arlo-backup.py -u $ARLO_USERNAME -p $ARLO_PASSWORD || exit 1

echo "Starting transfer to ${ARLO_BACKUP_USER}@${ARLO_BACKUP_IP}:${ARLO_BACKUP_DIR_PATH}/${date_formatted}..."
ssh ${ARLO_BACKUP_USER}@${ARLO_BACKUP_IP} mkdir -p ${ARLO_BACKUP_DIR_PATH}/${date_formatted} || exit 1
rsync --remove-source-files -av videos/ ${ARLO_BACKUP_USER}@${ARLO_BACKUP_IP}:${ARLO_BACKUP_UPLOAD_PATH}/${date_formatted} || exit 1

echo "Backup completed"