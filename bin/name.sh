#!/bin/bash

set -e

find . -iname '\!ReadMe' | while read -r readme; do
  echo "$readme"
  dir="$( dirname "$readme" )"
  cat "$readme" | while read -r ln; do
    echo "  $ln"
  done
done

# vim:ts=2:sw=2:sts=2:et:ft=sh

