---
description: 블로그 워크플로우 Step 4 - 선정된 주제 리서치
allowed-tools: Read, Write, WebSearch, WebFetch, Bash(python3:*)
---

## Task

선정된 주제들에 대해 웹 리서치를 수행한다.

### 실행 순서

1. 최신 run 디렉토리 확인:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/latest_run.py
   ```

2. 상태 업데이트:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/update_status.py --run-dir {run_dir} --phase research --status in_progress
   ```

3. `{run_dir}/selected/selected.yaml`을 읽어서 선정된 토픽 목록 확인

4. 각 토픽에 대해:
   - 한국어 검색 2-3회 + 영어 검색 2-3회 수행 (WebSearch)
   - 유용한 소스는 WebFetch로 상세 내용 확인
   - 최신 트렌드, 전문가 의견, 통계, 반론 수집
   - `{run_dir}/research/{topic-slug}.yaml`에 저장:
     ```yaml
     topic: "{slug}"
     researched_at: "ISO 8601 timestamp"
     queries:
       - query: "검색어"
         language: "ko"
     findings:
       trends:
         - point: "트렌드"
           source: "출처"
       expert_opinions:
         - who: "전문가"
           opinion: "의견"
       statistics:
         - stat: "수치"
           source: "출처"
       counterpoints:
         - point: "반론"
           source: "출처"
     ```

5. 상태 업데이트:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/update_status.py --run-dir {run_dir} --phase research --status completed
   ```

6. 결과 요약 + 다음 단계 안내: `/blog-outline`
