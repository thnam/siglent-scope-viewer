#!/usr/bin/env bash

while true ; do
   lxi screenshot --address 192.168.1.119 --plugin siglent-sds scope.png
   sleep 0.5
done
