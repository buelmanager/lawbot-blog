---
description: 블로그 워크플로우 Step 5 - 글 개요 작성
allowed-tools: Read, Write, Bash(python3:*)
---

## Task

리서치 결과를 기반으로 블로그 글 개요를 작성한다.

### 실행 순서

1. 최신 run 디렉토리 확인:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/latest_run.py
   ```

2. 상태 업데이트:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/update_status.py --run-dir {run_dir} --phase outline --status in_progress
   ```

3. 각 토픽에 대해 다음 파일들을 읽기:
   - `{run_dir}/selected/selected.yaml` - 주제 정보
   - `{run_dir}/research/{slug}.yaml` - 리서치 결과
   - `{run_dir}/insights/insights.yaml` - 원본 인사이트

4. 자료를 종합하여 글 개요를 설계하고 `{run_dir}/outlines/{slug}.yaml`에 저장:
   ```yaml
   topic: "{slug}"
   title: "블로그 글 제목"
   created_at: "ISO 8601 timestamp"
   hook: "서두 1-2문장"
   sections:
     - heading: "섹션 제목"
       key_points:
         - point: "핵심 포인트"
           evidence: "근거"
       subsections:
         - heading: "소제목"
           key_points:
             - point: "포인트"
               evidence: "근거"
   conclusion:
     summary: "핵심 메시지"
     call_to_action: "독자 행동 유도"
   seo:
     suggested_title: "SEO 제목"
     meta_description: "160자 이내"
     keywords: ["키워드1", "키워드2"]
   estimated_length: "2500-3000자"
   ```

5. 상태 업데이트:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/update_status.py --run-dir {run_dir} --phase outline --status completed
   ```

6. 결과 요약 + 다음 단계 안내: `/blog-review-outlines`
