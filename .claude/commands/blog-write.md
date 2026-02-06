---
description: 블로그 워크플로우 Step 7 - 최종 블로그 글 작성
allowed-tools: Read, Write, Bash(python3:*)
---

## Task

개요와 피드백을 기반으로 최종 블로그 글을 작성한다.

### 실행 순서

1. 최신 run 디렉토리 확인:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/latest_run.py
   ```

2. 상태 업데이트:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/update_status.py --run-dir {run_dir} --phase write --status in_progress
   ```

3. 승인된 토픽 확인: `{run_dir}/feedback/` 에서 `decision: "approved"` 또는 `decision: "revision_requested"` 인 토픽만 대상

4. 각 토픽에 대해 다음 파일들을 읽기:
   - `{run_dir}/outlines/{slug}.yaml` - 글 개요
   - `{run_dir}/feedback/{slug}.yaml` - 사용자 피드백
   - `{run_dir}/research/{slug}.yaml` - 리서치 결과
   - `{run_dir}/selected/selected.yaml` - 주제 컨텍스트

5. 피드백의 수정 요청사항 반영하여 본문 작성

6. `{run_dir}/articles/{slug}.md`에 저장:
   ```markdown
   ---
   title: "블로그 글 제목"
   date: "YYYY-MM-DD"
   tags: [태그1, 태그2]
   description: "메타 설명"
   ---

   # 제목

   (본문)

   ---

   *이 글은 유튜브 채널 컨텐츠를 기반으로 작성되었습니다.*

   **참고 영상:**
   - [영상 제목](URL)
   ```

7. 글 작성 가이드라인:
   - 전문적이지만 친근한 대화체
   - 개요 구조를 충실히 따르되 자연스러운 전환
   - 리서치의 통계/전문가 의견 인용
   - 반론도 공정하게 다루기
   - 문단은 3-4문장 내외로 간결하게

8. 상태 업데이트:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/update_status.py --run-dir {run_dir} --phase write --status completed
   ```

9. 최종 글 파일 경로 안내
