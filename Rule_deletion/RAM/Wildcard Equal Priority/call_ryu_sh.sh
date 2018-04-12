ryu-manager delete_same_priorityv3_sh.py  &


#ps aux | grep -ie ryu-manager | awk '{print $2}' | xargs kill -9

#APP_PID=$!
#sleep $(($(($1/2))+10))
sleep 90

PKTGEN=$(ps aux | grep pktgen-v4.py | head -n 1 | awk '{ print $2 }'); kill -9 $PKTGEN;
PKTGEN=$(ps aux | grep pktgen-v4.py | head -n 1 | awk '{ print $2 }'); kill -9 $PKTGEN;

RYUPROCESS=$(netstat -vantup | grep 6633 | grep LISTEN | awk '{ print $7 }' | cut -d '/' -f 1);kill -9 $RYUPROCESS

while [ $? -le 0 ]
do
        RYUPROCESS=$(netstat -vantup | grep 6633 | grep LISTEN | awk '{ print $7 }' | cut -d '/' -f 1); kill -9 $RYUPROCESS
done

