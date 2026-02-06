#!/usr/bin/env python3
"""
.reference/contents/의 YouTube 데이터를 경량 인덱스로 변환

Usage:
    python index_sources.py --run-dir blog/runs/2026-02-06 [--source-dir .reference/contents] [--channels aiDotEngineer,otherChannel]

Output:
    JSON 형식으로 인덱싱 결과 출력
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print(json.dumps({"error": "pyyaml 미설치", "install": "pip install pyyaml"}))
    sys.exit(1)


def list_channels(source_dir: str, channels_yaml: str = ".reference/channels.yaml") -> dict:
    """등록된 채널 목록과 각 채널의 영상 수를 반환"""
    source_path = Path(source_dir)
    channels_path = Path(channels_yaml)

    result = []

    if channels_path.exists():
        with open(channels_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        registered = {c.get("handle", "").lstrip("@"): c.get("name", "") for c in data.get("channels", [])}
    else:
        registered = {}

    if not source_path.exists():
        return {"channels": [], "error": f"소스 디렉토리 없음: {source_dir}"}

    for channel_dir in sorted(source_path.iterdir()):
        if not channel_dir.is_dir():
            continue
        handle = channel_dir.name
        video_count = len(list(channel_dir.glob("*.yaml")))
        result.append({
            "handle": handle,
            "name": registered.get(handle, handle),
            "video_count": video_count,
        })

    return {"channels": result}


def index_sources(source_dir: str, run_dir: str, channels: list[str] | None = None) -> dict:
    source_path = Path(source_dir)
    run_path = Path(run_dir)

    if not source_path.exists():
        return {"error": f"소스 디렉토리 없음: {source_dir}", "indexed": 0}

    sources = []

    # 채널별 폴더 순회
    for channel_dir in sorted(source_path.iterdir()):
        if not channel_dir.is_dir():
            continue

        channel_handle = channel_dir.name

        # 채널 필터링: 지정된 채널만 인덱싱
        if channels and channel_handle not in channels:
            continue

        for yaml_file in sorted(channel_dir.glob("*.yaml")):
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)

                if not data or "video_id" not in data:
                    continue

                # 경량 인덱스: transcript.text 전문 제외, preview만 포함
                transcript_text = (data.get("transcript", {}).get("text") or "")
                entry = {
                    "video_id": data.get("video_id"),
                    "title": data.get("title"),
                    "channel": channel_handle,
                    "published_at": data.get("published_at"),
                    "url": data.get("url"),
                    "duration": data.get("duration"),
                    "has_transcript": data.get("transcript", {}).get("available", False),
                    "transcript_preview": transcript_text[:500] or None,
                    "summary": data.get("summary", {}).get("content") if data.get("summary") else None,
                    "source_path": str(yaml_file),
                }
                sources.append(entry)

            except Exception as e:
                # 읽기 실패한 파일은 건너뛰기
                continue

    # 발행일 기준 최신순 정렬
    sources.sort(key=lambda x: x.get("published_at") or "", reverse=True)

    # source-index.yaml 저장
    index_data = {"indexed_at": str(__import__("datetime").date.today()), "count": len(sources), "sources": sources}

    index_path = run_path / "sources" / "source-index.yaml"
    index_path.parent.mkdir(parents=True, exist_ok=True)

    with open(index_path, "w", encoding="utf-8") as f:
        yaml.dump(index_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    return {"index_path": str(index_path), "indexed": len(sources), "status": "success"}


def main():
    parser = argparse.ArgumentParser(description="YouTube 소스 데이터 인덱싱")
    parser.add_argument("--run-dir", help="실행 디렉토리 경로")
    parser.add_argument("--source-dir", default=".reference/contents", help="소스 디렉토리 (기본: .reference/contents)")
    parser.add_argument("--channels", help="인덱싱할 채널 목록 (쉼표 구분, 예: aiDotEngineer,otherChannel)")
    parser.add_argument("--list-channels", action="store_true", help="등록된 채널 목록 출력")
    args = parser.parse_args()

    if args.list_channels:
        result = list_channels(args.source_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if not args.run_dir:
        print(json.dumps({"error": "--run-dir 필수 (--list-channels 제외)"}))
        sys.exit(1)

    channels = [c.strip() for c in args.channels.split(",")] if args.channels else None
    result = index_sources(args.source_dir, args.run_dir, channels=channels)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
