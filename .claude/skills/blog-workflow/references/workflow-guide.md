# 블로그 워크플로우 단계별 가이드

## Phase 1: 수집 + 인사이트 추출 (자동)

### Step 1. 실행 초기화 + 소스 인덱싱

```bash
# 실행 디렉토리 생성
python3 scripts/init_run.py --base-dir blog

# 소스 인덱싱
python3 scripts/index_sources.py --run-dir blog/runs/{date} --source-dir .reference/contents
```

실행 후 `update_status.py`로 collect phase를 completed로 변경.

### Step 2. 인사이트 추출

`insight-extractor` 서브에이전트를 Task 도구로 호출:

```
Task(subagent_type="insight-extractor", prompt="run_dir: blog/runs/{date}")
```

에이전트가 `source-index.yaml`을 읽고 `insights/insights.yaml`을 생성.
완료 후 insight phase를 completed로 업데이트.

### Step 3. 인사이트 검토 (Human Checkpoint)

사용자에게 `/review-insights {date}` 실행을 안내.
사용자가 인사이트를 선택하면 `selected/selected.yaml`이 생성됨.
review_insights phase를 completed로 업데이트.

---

## Phase 2: 리서치 + 자막 분석 + 개요 작성 (자동)

### Step 4a. 리서치

`selected.yaml`의 각 토픽에 대해 `topic-researcher` 서브에이전트를 병렬 호출:

```
Task(subagent_type="topic-researcher", prompt="topic_slug: {slug}, run_dir: blog/runs/{date}")
```

각 에이전트가 `research/{slug}.yaml`을 생성.

### Step 4b. 자막 분석 (Step 4a와 동시 실행)

`selected.yaml`의 각 토픽에 대해 `transcript-analyzer` 서브에이전트를 병렬 호출:

```
Task(subagent_type="transcript-analyzer", prompt="topic_slug: {slug}, run_dir: blog/runs/{date}")
```

각 에이전트가 관련 영상의 자막에서 인용, 사례, 설명, 논점을 추출하여 `transcripts/{slug}.yaml`을 생성.

### Step 5. 개요 작성

리서치 + 자막 분석이 모두 완료된 각 토픽에 대해 `outline-writer` 서브에이전트를 호출:

```
Task(subagent_type="outline-writer", prompt="topic_slug: {slug}, run_dir: blog/runs/{date}")
```

각 에이전트가 리서치 결과와 자막 분석 결과를 종합하여 `outlines/{slug}.yaml`을 생성.

### Step 6. 개요 검토 (Human Checkpoint)

사용자에게 `/review-outlines {date}` 실행을 안내.
사용자 피드백이 `feedback/{slug}.yaml`로 저장됨.
review_outlines phase를 completed로 업데이트.

---

## Phase 3: 글 작성 (자동)

### Step 7. 최종 글 작성

승인된 각 토픽에 대해 `article-writer` 서브에이전트를 호출:

```
Task(subagent_type="article-writer", prompt="topic_slug: {slug}, run_dir: blog/runs/{date}")
```

에이전트가 `articles/{slug}.md`를 생성. opus 모델 사용.

---

## 상태 관리

모든 단계 전후로 `update_status.py` 실행:

```bash
# phase 시작
python3 scripts/update_status.py --run-dir blog/runs/{date} --phase research --status in_progress

# phase 완료
python3 scripts/update_status.py --run-dir blog/runs/{date} --phase research --status completed

# 토픽 등록
python3 scripts/update_status.py --run-dir blog/runs/{date} --add-topic ai-agent-guide --topic-title "AI 에이전트 가이드"
```

## 세션 복원

새 세션에서 이전 작업을 이어갈 때:

1. `list_runs.py`로 실행 목록 확인
2. `run.yaml` 읽어서 마지막 완료 phase 확인
3. 다음 phase부터 재개
