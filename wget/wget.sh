#!/bin/bash

for var in "$@"
do
    wget $var
done

sha256sum *