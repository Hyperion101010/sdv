#!/bin/bash

set -x

if [ $(id -u) -eq 0 ]
then
  echo "Performing Operations as Root"
else
  echo "I'm NOT ROOT"
  exit 0
fi

# First Stop services.
systemctl stop ksmtuned
systemctl stop ksm

# Disable so that it persists
systemctl disable ksmtuned
systemctl disable ksm
