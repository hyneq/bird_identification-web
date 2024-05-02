#!/bin/bash

source "$(dirname "$0")/../vars"

export MTX_RTSP=no
export MTX_RTMP=no
export MTX_HLS=no
export MTX_SRT=no

export MTX_WEBRTCADDRESS=":$mediamtx_webrtc_port"

export MTX_PATHS_PREDICTION_SOURCE="$REMOTE_STREAM_PATH"
export MTX_PATHS_PREDICTION_SOURCEONDEMAND=yes

exec "$mediamtx_dir/mediamtx"
