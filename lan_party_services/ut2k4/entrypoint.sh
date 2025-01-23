#!/bin/bash


cp -r /usr/src/System/* /usr/src/ut2004/System
chmod 777 /usr/src/ut2004/System/*
cp /ini/UT2004.ini /usr/src/ut2004/System/UT2004.ini
cp /usr/src/ut2004/System/UT2004.ini /usr/src/ut2004/System/UT2004.ini.tpl
cat /usr/src/ut2004/System/UT2004.ini.tpl
set -e

if [ "$1" = 'ucc-bin' ]; then
    # Put cdkey in place
    echo $CDKEY > cdkey
    if [ -f UT2004.ini.tpl ];
    then
        envtpl UT2004.ini.tpl
    fi
fi

exec "$@"
