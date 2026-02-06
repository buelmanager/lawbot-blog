---
name: blog-workflow
description: 유튜브 채널에서 수집한 컨텐츠를 기반으로 블로그 글을 생성하는 워크플로우. 사용자가 (1) 블로그 주제 찾기/글 쓰기를 요청하거나, (2) 수집된 영상에서 인사이트를 추출하거나, (3) 블로그 워크플로우를 진행할 때 사용. "블로그 글 쓸 주제 찾아줘", "블로그 글 작성해줘", "인사이트 추출해줘" 등의 요청에 트리거됨.
---

# Blog Workflow

유튜브 컨텐츠 기반 블로그 글 생성 7단계 파이프라인.

## 데이터 경로

```
blog/runs/{YYYY-MM-DD}/     # 실행별 디렉토리
├── run.yaml                 # 상태 추적
├── sources/source-index.yaml
├── insights/insights.yaml
├── selected/selected.yaml
├── research/{slug}.yaml
├── transcripts/{slug}.yaml
├── outlines/{slug}.yaml
├── feedback/{slug}.yaml
└── articles/{slug}.md
```

소스 데이터: `.reference/contents/` (youtube-collector가 수집)

## 워크플로우

### Phase 1: 수집 → 인사이트 (자동 체이닝)

1. **초기화**: `scripts/init_run.py` → `scripts/index_sources.py` 순서로 실행
2. **인사이트 추출**: `insight-extractor` 서브에이전트를 Task 도구로 호출
   ```
   Task(subagent_type="insight-extractor", prompt="run_dir: blog/runs/{date}")
   ```
3. 완료 후 사용자에게 안내: `/review-insights {date}` 실행 요청

### Phase 2: 리서치 → 개요 (자동 체이닝)

사용자가 리서치/개요 작성을 요청하면:

4a. **리서치**: `selected.yaml`에서 토픽별로 `topic-researcher` 서브에이전트 병렬 호출
   ```
   Task(subagent_type="topic-researcher", prompt="topic_slug: {slug}, run_dir: blog/runs/{date}")
   ```
4b. **자막 분석**: `transcript-analyzer` 서브에이전트 병렬 호출 (4a와 동시 실행)
   ```
   Task(subagent_type="transcript-analyzer", prompt="topic_slug: {slug}, run_dir: blog/runs/{date}")
   ```
5. **개요 작성**: 리서치 + 자막 분석 완료 후 `outline-writer` 서브에이전트 호출 (토픽별)
   ```
   Task(subagent_type="outline-writer", prompt="topic_slug: {slug}, run_dir: blog/runs/{date}")
   ```
6. 완료 후 사용자에게 안내: `/review-outlines {date}` 실행 요청

### Phase 3: 글 작성

사용자가 글 작성을 요청하면:

7. **글 작성**: 승인된 토픽별로 `article-writer` 서브에이전트 호출 (opus 모델)
   ```
   Task(subagent_type="article-writer", prompt="topic_slug: {slug}, run_dir: blog/runs/{date}", model="opus")
   ```

## 상태 관리

각 단계 전후로 `scripts/update_status.py`로 `run.yaml` 업데이트:

```bash
python3 scripts/update_status.py --run-dir blog/runs/{date} --phase {phase} --status {in_progress|completed}
```

토픽 등록:
```bash
python3 scripts/update_status.py --run-dir blog/runs/{date} --add-topic {slug} --topic-title "제목"
```

## 세션 복원

새 세션에서 이어가기: `scripts/list_runs.py`로 상태 확인 후 `run.yaml`의 마지막 완료 phase 다음부터 재개.

## 참고 자료

- **데이터 스키마**: [references/data-schema.md](references/data-schema.md) - 모든 YAML 파일 형식
- **단계별 가이드**: [references/workflow-guide.md](references/workflow-guide.md) - 상세 실행 지침
- **글 템플릿**: [assets/article-template.md](assets/article-template.md) - 최종 글 마크다운 형식
