#!/usr/bin/env bash
LOCKDIR=/tmp/fetchScreenshot.kicker.lock
IP="192.168.30.87"

#Remove the lock directory
function cleanup {
   if rm -rf $LOCKDIR; then
      echo "Finished"
   else
      echo "Failed to remove lock directory '$LOCKDIR'"
      exit 1
   fi
}

if mkdir $LOCKDIR; then
   #Ensure that if we "grabbed a lock", we release it
   #Works for SIGTERM and SIGINT(Ctrl-C)
   trap "cleanup" EXIT
   echo "Acquired lock, running"

   while true ; do
      lxi screenshot --address $IP --plugin siglent-sds scope.png
      sleep 0.5
   done
else
   echo "Could not create lock directory '$LOCKDIR', is another instance of"
   echo "this script already running? If not, you can try again after manually"
   echo "removing the lockfile $LOCKDIR." 
   exit 1
fi

