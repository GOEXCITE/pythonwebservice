#!/bin/sh

DWORK=.
WORKER=httpserver/listener.py
PORT=8081
HOST=0.0.0.0

usage() {
    echo ""
    echo "Usage: $0 [start|stop|restart] "
}

start() {
    if [ `ps -ef|grep -w ${WORKER}|grep -v grep|wc -l` -eq 0 ]; then
        if [ -f $DWORK/$WORKER ]; then
            cd $DWORK
            python $WORKER $PORT $HOST >& server.log &
            cd - >& /dev/null
            echo "${WORKER} running at: `date`"
        else
            echo "$DWORK/$WORKER not exists"
        fi
    else
        echo "${WORKER} is running already!!!"
    fi
    ps -ef | grep -w ${WORKER} | grep -wv grep
}

stop() {
    echo "stop ${WORKER}"
    if [ `ps -ef|grep -w ${WORKER}|grep -v grep|wc -l` -ne 0 ]; then
        kill `ps -ef|grep -w ${WORKER}|grep -v grep|awk '{print $2}'`
    else
        echo "${WORKER} is not on service, no need to stop"
    fi
}

restart() {
    stop
    sleep 1
    start
}

case $(echo $1 | tr [a-z] [A-Z]) in
    START|--START)
        start ;;
    STOP|--STOP)
        stop ;;
    HELP|-H|--HELP)
        usage ;;
    *)
        restart ;;
esac
