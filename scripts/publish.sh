#!/bin/bash
# 워크플로우에서 생성된 글을 배포 디렉토리로 복사
# 사용법: ./scripts/publish.sh blog/runs/2026-02-06/articles/

SOURCE_DIR="${1:?Usage: publish.sh <source-articles-dir>}"
TARGET_DIR="src/content/articles"

mkdir -p "$TARGET_DIR"
cp "$SOURCE_DIR"/*.md "$TARGET_DIR/"
echo "Published $(ls -1 "$SOURCE_DIR"/*.md | wc -l | tr -d ' ') articles to $TARGET_DIR"
