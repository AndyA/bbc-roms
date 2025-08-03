#!/bin/bash

set -e

find incoming -iname '*.zip' | while read -r zip; do
  dir="$( dirname "$zip" )"
  name="$( basename "$zip" )"
  out="$zip.contents"
  [[ -d $out ]] && continue
  tmp="$zip.tmp"
  rm -rf "$tmp"
  mkdir -p "$tmp"
  pushd "$tmp"
  unzip "../$name" || mv "../$name" "../$name.error"
  popd
  mv "$tmp" "$out"
done

# vim:ts=2:sw=2:sts=2:et:ft=sh

