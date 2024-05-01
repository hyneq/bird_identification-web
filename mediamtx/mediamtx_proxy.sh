#!/bin/bash

source "$(dirname "$0")/../vars"

export MTX_WEBRTCADDRESS=":$MEDIAMTX_WEBRTC_PORT"
export MTX_PATHS_PREDICTION_SOURCE="$REMOTE_STREAM_PATH"

exec "$mediamtx_dir/mediamtx" "$mediamtx_dir/mediamtx.yml"
