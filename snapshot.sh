#!/bin/bash

export DEST_DIR=../lyric-lang

if [ -e "${DEST_DIR}/lyric-snapshot" ]; then
    echo "Destination directory already exists..."
    exit
fi

cp -vf README.md ${DEST_DIR}
cp -vf LICENSE ${DEST_DIR}
cp -vf GPL3 ${DEST_DIR}
cp -vf pyproject.toml ${DEST_DIR}
cp -vf build-deb.sh ${DEST_DIR}

mkdir -p ${DEST_DIR}/lyric-snapshot

echo "archiving lyric..."
git archive HEAD lyric | tar -x --strip-components=1 -C ${DEST_DIR}/lyric-snapshot
