#!/bin/bash
echo "APPDIR=$(pwd)" >> .env

export APPDIR=$(pwd)
export PYTHONUNBUFFERED=1

mkdir -p $APPDIR/homedir
mkdir -p $APPDIR/logs/web
mkdir -p $APPDIR/logs/db
mkdir -p $APPDIR/logs/mq
mkdir -p $APPDIR/logs/ftp
mkdir -p $APPDIR/logs/worker
mkdir -p $APPDIR/logs/worker/tasks
mkdir -p $APPDIR/logs/executor

touch $APPDIR/logs/supervisord.log
touch $APPDIR/logs/ftp/ftp.log
touch $APPDIR/logs/ftp/err.log
touch $APPDIR/logs/worker/worker.log
touch $APPDIR/logs/worker/err.log

chmod 755 -R $APPDIR/homedir
chmod 755 -R $APPDIR/scripts
