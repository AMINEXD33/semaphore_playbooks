#!/usr/bin/env bash
set -euo pipefail

F5_HOST="172.19.10.3"
F5_USER="your_backup_user"
UCS_NAME="backup_$(date +%Y%m%d_%H%M%S).ucs"
REMOTE_UCS_DIR="/var/local/ucs"
LOCAL_DEST="/path/to/local/backups"

# 1. Create the UCS backup on the F5 over SSH
ssh "${F5_USER}@${F5_HOST}" "tmsh save sys ucs ${UCS_NAME}"

# 2. Pull it via SFTP
sftp "${F5_USER}@${F5_HOST}" <<EOF
get ${REMOTE_UCS_DIR}/${UCS_NAME} ${LOCAL_DEST}/${UCS_NAME}
EOF

# 3. Verify it actually landed locally before deleting remote copy
if [[ -s "${LOCAL_DEST}/${UCS_NAME}" ]]; then
    ssh "${F5_USER}@${F5_HOST}" "rm ${REMOTE_UCS_DIR}/${UCS_NAME}"
    echo "Backup ${UCS_NAME} transferred and remote copy removed."
else
    echo "ERROR: local file missing or empty — NOT deleting remote backup." >&2
    exit 1
fi
