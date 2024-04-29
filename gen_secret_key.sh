#!/bin/bash

# Generates secret key for the Django app
# based on https://github.com/hyneq/STINBankSystem/blob/main/gen_secret_key.sh

# Set up environment
source "$(dirname $0)/vars"
secret_dir="$app_dir/secret"
secret_key="$secret_dir/django_secret.key"

# Create directory for secrets if not exists
mkdir -p "$secret_dir"
chmod 750 "$secret_dir"

# Run Python code to get a secret key and save it to a file
python3 << EOF > "$secret_key"
from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()
print(secret_key)
EOF
chmod 640 "$secret_key"
