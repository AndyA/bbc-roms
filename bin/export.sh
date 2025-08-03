#!/bin/bash

set -e

find BBC_ROMS \( -iname '*.ssd' -o -iname '*.dsd' \) | while read -r img; do
  name="$( basename "$img" )"
  mkdir -p "$name"
  dfsimage export "$img" -o "$name/"
done

# vim:ts=2:sw=2:sts=2:et:ft=sh

