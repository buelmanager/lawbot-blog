---
description: 블로그 워크플로우 Step 1 - 실행 초기화 및 소스 인덱싱
allowed-tools: Bash(python3:*), AskUserQuestion
---

## Task

블로그 워크플로우의 첫 단계: 오늘 날짜로 실행 디렉토리를 생성하고 YouTube 소스 데이터를 인덱싱한다.

### 실행 순서

1. 등록된 채널 목록 조회:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/index_sources.py --list-channels
   ```

2. 출력된 채널 목록을 사용자에게 보여주고 **AskUserQuestion 도구**로 두 가지를 질문한다:

   **질문 1: 채널 선택**
   - 각 채널의 이름(name), 핸들(handle), 영상 수(video_count)를 표시
   - 옵션: 개별 채널들 + "전체 채널" 옵션
   - multiSelect: true (복수 선택 가능)
   - 사용자가 "전체 채널"을 선택하면 --channels 옵션 없이 실행

   **질문 2: 목표 글 개수**
   - "블로그 글을 몇 편 생성할까요?"
   - 옵션: "1편", "2편 (Recommended)", "3편", "5편"
   - multiSelect: false
   - 이 값에 따라 분석 규모가 조절됨:
     - 인사이트 추출 개수 = article_count * 3 (선택 여지 확보)
     - 깊이 분석할 영상 수 = article_count * 5

3. 실행 디렉토리 초기화 (사용자가 선택한 article_count 전달):
   ```bash
   python3 .claude/skills/blog-workflow/scripts/init_run.py --base-dir blog --article-count {article_count}
   ```

4. 출력된 JSON에서 `run_path` 확인 후, 선택된 채널로 소스 인덱싱:
   - 특정 채널 선택 시:
     ```bash
     python3 .claude/skills/blog-workflow/scripts/index_sources.py --run-dir {run_path} --source-dir .reference/contents --channels {comma_separated_handles}
     ```
   - 전체 채널 선택 시:
     ```bash
     python3 .claude/skills/blog-workflow/scripts/index_sources.py --run-dir {run_path} --source-dir .reference/contents
     ```

5. 상태 업데이트:
   ```bash
   python3 .claude/skills/blog-workflow/scripts/update_status.py --run-dir {run_path} --phase collect --status completed
   ```

6. 결과 요약:
   - 선택된 채널명
   - 인덱싱된 영상 수
   - 목표 글 개수 (article_count)
   - 분석 규모: 인사이트 {article_count * 3}개 추출 예정, 영상 {article_count * 5}개 심층 분석 예정
   - 다음 단계 안내: `/blog-insight`
