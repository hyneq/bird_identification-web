#!/bin/bash

# from https://github.com/hyneq/STINBankSystem/blob/main/manage.sh

source "$(dirname "$0")"/vars

exec $app_dir/manage.py "$@"
