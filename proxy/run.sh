#!/bin/sh

set -e
## how shell will plug in runtime
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'
