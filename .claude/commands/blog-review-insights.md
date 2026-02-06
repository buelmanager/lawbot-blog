---
description: 블로그 워크플로우 Step 3 - 인사이트 검토 및 주제 선택 (human checkpoint)
allowed-tools: Read, Write, Bash(python3:*)
---

## Task

1. 최신 run 디렉토리 확인:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/latest_run.py
   ```

2. `{run_dir}/insights/insights.yaml` 파일을 읽는다

3. 각 인사이트를 다음 형식으로 번호와 함께 표시한다:

   ```
   ### [번호] INS-{id}: {title}
   {summary}

   **출처 영상**: {sources 목록}
   **가능한 관점**:
   - {angle 1}
   - {angle 2}
   **태그**: {tags}
   ```

4. 사용자에게 선택을 요청한다:
   - 어떤 인사이트로 블로그 글을 쓸지 번호로 선택
   - 각 선택한 인사이트에 대해 선호하는 angle 지정 가능
   - 추가 메모가 있으면 입력

5. 사용자의 선택을 `{run_dir}/selected/selected.yaml`에 저장한다:

   ```yaml
   selected_at: "ISO 8601 timestamp"
   topics:
     - insight_id: "INS-001"
       slug: "제목-기반-slug"
       title: "선택된 인사이트 제목"
       angle: "사용자가 선택한 관점"
       user_note: "사용자 추가 메모"
   ```

   slug는 제목을 영문 소문자 kebab-case로 변환하여 생성한다.

6. 상태 업데이트 + 토픽 등록:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/update_status.py --run-dir {run_dir} --phase review_insights --status completed
   python3 .claude/skills/blog-workflow/scripts/update_status.py --run-dir {run_dir} --add-topic {slug} --topic-title "{title}"
   ```

7. 다음 단계 안내: `/blog-research`
