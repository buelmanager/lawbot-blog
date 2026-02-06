---
description: 블로그 워크플로우 Step 2 - 인사이트 추출
allowed-tools: Read, Write, Glob, Grep, Bash(python3:*)
---

## Task

소스 인덱스에서 블로그 주제가 될 수 있는 인사이트를 추출한다.

### 실행 순서

1. 최신 run 디렉토리 확인:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/latest_run.py
   ```

2. 상태 업데이트:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/update_status.py --run-dir {run_dir} --phase insight --status in_progress
   ```

3. `{run_dir}/sources/source-index.yaml`을 읽는다

4. 각 영상의 summary 분석. summary가 없으면 `source_path`의 원본 파일에서 description 참조

5. 영상들 간 공통 주제, 트렌드, 독특한 관점을 교차 분석하여 5~10개 인사이트 추출

6. `{run_dir}/insights/insights.yaml`에 저장:
   ```yaml
   extracted_at: "ISO 8601 timestamp"
   source_count: 10
   insights:
     - id: "INS-001"
       title: "인사이트 제목"
       summary: "2-3문장 요약"
       sources:
         - video_id: "abc123"
           title: "영상 제목"
           relevance: "연결 설명"
       angles:
         - "관점 1"
         - "관점 2"
       tags: ["태그1", "태그2"]
   ```

7. 상태 업데이트:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/update_status.py --run-dir {run_dir} --phase insight --status completed
   ```

8. 결과 요약 + 다음 단계 안내: `/blog-review-insights`
