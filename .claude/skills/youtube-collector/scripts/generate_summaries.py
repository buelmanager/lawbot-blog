#!/usr/bin/env python3
"""
summary가 없는 영상 YAML에 description 기반 요약을 일괄 생성

Usage:
    python generate_summaries.py --source-dir .reference/contents
    python generate_summaries.py --source-dir .reference/contents --channels moelkorea
    python generate_summaries.py --source-dir .reference/contents --channels moelkorea,aiDotEngineer

Output:
    JSON 형식으로 처리 결과 출력
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print(json.dumps({"error": "pyyaml 미설치", "install": "pip install pyyaml"}))
    sys.exit(1)


def extract_summary_from_description(description: str, title: str = "") -> dict | None:
    """description 텍스트에서 구조화된 요약을 추출하여 summary dict 반환"""
    if not description or len(description.strip()) < 30:
        return None

    lines = description.strip().split('\n')

    # 의미 있는 라인만 필터 (빈줄, 구분선 제거)
    content_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if all(c in '-─═•·' for c in stripped) and len(stripped) > 3:
            continue
        content_lines.append(stripped)

    if not content_lines:
        return None

    # 핵심 포인트 추출
    key_points = []
    intro_lines = []
    warning_lines = []

    section_type = "intro"  # intro, key, warning, timeline, etc.

    for line in content_lines:
        lower = line.lower()

        # 섹션 감지
        if any(kw in line for kw in ['핵심 요약', '핵심 내용', '핵심 포인트', '영상 요약', '영상 핵심']):
            section_type = "key"
            continue
        if any(kw in line for kw in ['타임라인', '⏰', '00:00']):
            section_type = "timeline"
            continue
        if any(kw in line for kw in ['주의사항', '⚠️', '주의:']):
            section_type = "warning"
            continue
        if any(kw in line for kw in ['상담 문의', '전화 문의', '이메일 문의', '📞', '📠', '📧', '📍', '사무실:']):
            section_type = "contact"
            continue
        if any(kw in line for kw in ['이런 분들', '꼭 보세요', '꼭 시청', '필독']):
            section_type = "target"
            continue

        # 타임라인/연락처는 건너뛰기
        if section_type in ("timeline", "contact"):
            continue

        # 타임코드 패턴 건너뛰기 (00:00 형식)
        if re.match(r'^\d{2}:\d{2}\s', line):
            continue

        # 포인트 추출
        clean_line = line

        # 이모지/마커 제거
        clean_line = re.sub(r'^[✅📌📢💡🔑▶👉⚠️🚨\s]+', '', clean_line)

        # 번호 매기기 패턴: "1.", "1)", "1. ", etc.
        numbered = re.match(r'^(\d+)[\.\)]\s*(.+)', clean_line)
        if numbered:
            clean_line = numbered.group(2).strip()

        # 불릿 포인트: "•", "·", "*", "-" 로 시작
        bullet = re.match(r'^[•·\*\-]\s*(.+)', clean_line)
        if bullet:
            clean_line = bullet.group(1).strip()

        # 빈 내용 건너뛰기
        if len(clean_line) < 5:
            continue

        # 굵은 마크다운 제거
        clean_line = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', clean_line)
        # 작은따옴표 두 개 제거
        clean_line = clean_line.replace("''", "'")

        if section_type == "intro":
            intro_lines.append(clean_line)
        elif section_type == "key":
            key_points.append(clean_line)
        elif section_type == "warning":
            warning_lines.append(clean_line)
        elif section_type == "target":
            # 대상자 정보도 핵심 포인트로 포함
            key_points.append(clean_line)

    # 요약 구성
    summary_parts = []

    # 서론: 제목 + 도입부
    summary_parts.append("## 서론")
    # 제목에서 @ 이후 제거
    clean_title = re.sub(r'@\S+', '', title).strip()
    if clean_title:
        summary_parts.append(f"- {clean_title}")
    for line in intro_lines[:2]:
        if len(line) > 10 and line != clean_title:
            summary_parts.append(f"- {line[:200]}")

    # 본론: 핵심 포인트
    summary_parts.append("## 본론")
    if key_points:
        for point in key_points[:8]:
            summary_parts.append(f"- {point[:200]}")
    else:
        # 핵심 포인트가 없으면 도입부에서 추가 추출
        for line in intro_lines[2:7]:
            if len(line) > 10:
                summary_parts.append(f"- {line[:200]}")

    # 결론: 주의사항 또는 마무리
    summary_parts.append("## 결론")
    if warning_lines:
        for line in warning_lines[:2]:
            summary_parts.append(f"- {line[:200]}")
    else:
        summary_parts.append(f"- {clean_title} 관련 핵심 정보 정리")

    content = '\n'.join(summary_parts) + '\n'

    return {
        "source": "description",
        "content": content
    }


def process_channel(source_dir: str, channel: str) -> dict:
    """채널 디렉토리의 모든 YAML을 처리"""
    channel_dir = Path(source_dir) / channel
    result = {"channel": channel, "processed": 0, "skipped": 0, "errors": []}

    if not channel_dir.exists():
        result["errors"].append(f"디렉토리 없음: {channel_dir}")
        return result

    for yaml_file in sorted(channel_dir.glob("*.yaml")):
        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data or "video_id" not in data:
                continue

            # 이미 summary가 있으면 건너뛰기
            if data.get("summary") is not None:
                result["skipped"] += 1
                continue

            # description에서 요약 생성
            description = data.get("description", "")
            title = data.get("title", "")
            summary = extract_summary_from_description(description, title)

            if summary is None:
                result["errors"].append(f"{data['video_id']}: description이 너무 짧거나 없음")
                continue

            # summary 필드 업데이트하여 저장
            data["summary"] = summary

            with open(yaml_file, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

            result["processed"] += 1

        except Exception as e:
            result["errors"].append(f"{yaml_file.name}: {str(e)}")

    return result


def main():
    parser = argparse.ArgumentParser(description="영상 YAML에 description 기반 요약 일괄 생성")
    parser.add_argument("--source-dir", default=".reference/contents", help="소스 디렉토리 (기본: .reference/contents)")
    parser.add_argument("--channels", help="처리할 채널 (쉼표 구분, 미지정 시 전체)")
    args = parser.parse_args()

    source_path = Path(args.source_dir)
    if not source_path.exists():
        print(json.dumps({"error": f"소스 디렉토리 없음: {args.source_dir}"}))
        sys.exit(1)

    # 대상 채널 결정
    if args.channels:
        channels = [c.strip() for c in args.channels.split(",")]
    else:
        channels = [d.name for d in sorted(source_path.iterdir()) if d.is_dir()]

    all_results = {
        "total_processed": 0,
        "total_skipped": 0,
        "channels": []
    }

    for channel in channels:
        result = process_channel(args.source_dir, channel)
        all_results["total_processed"] += result["processed"]
        all_results["total_skipped"] += result["skipped"]
        all_results["channels"].append(result)

    print(json.dumps(all_results, ensure_ascii=False, indent=2))

    if all_results["total_processed"] == 0 and not any(r["errors"] for r in all_results["channels"]):
        # 모든 영상이 이미 summary가 있음
        pass


if __name__ == "__main__":
    main()
