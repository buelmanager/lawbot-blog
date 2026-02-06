---
description: 블로그 워크플로우 Step 1 - 실행 초기화 및 소스 인덱싱
allowed-tools: Bash(python3:*)
---

## Task

블로그 워크플로우의 첫 단계: 오늘 날짜로 실행 디렉토리를 생성하고 YouTube 소스 데이터를 인덱싱한다.

### 실행 순서

1. 실행 디렉토리 초기화:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/init_run.py --base-dir blog
   ```

2. 출력된 JSON에서 `run_path` 확인 후, 소스 인덱싱:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/index_sources.py --run-dir {run_path} --source-dir .reference/contents
   ```

3. 상태 업데이트:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/update_status.py --run-dir {run_path} --phase collect --status completed
   ```

4. 결과 요약:
   - 인덱싱된 영상 수
   - 다음 단계 안내: `/blog-insight`
