#!/bin/bash

# from https://github.com/hyneq/STINBankSystem/blob/main/manage.sh

source "$(dirname "$0")"/activate

exec $app_dir/manage.py "$@"
