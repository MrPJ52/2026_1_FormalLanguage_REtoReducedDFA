# Development Log

이 문서는 프로젝트의 개발 변경 이력을 시간 순서대로 기록한다.

## 2026-06-17

### 초기 프로젝트 골격 구축

- 모듈 분리 구조 생성:
  - `main.py`
  - `ast_node.py`
  - `regex_parser.py`
  - `nfa.py`
  - `dfa.py`
  - `scanner.py`
  - `printer.py`
  - `tests/test_parser.py`
  - `tests/test_nfa.py`
  - `tests/test_dfa.py`
- `main.py`에 단계별 CLI 실행 흐름 구성.
- 미구현 단계는 `NotImplementedError`와 `[PENDING]` 메시지로 명확히 표시.

### 파서 및 AST 기반 기능

- `ast_node.py`:
  - `Node` 데이터 구조 정의.
  - `size()`, `to_nested_list()`, `count_thompson_states_arcs()` 구현.
- `regex_parser.py`:
  - 토큰화, concatenation 삽입, shunting-yard postfix 변환, postfix->AST 변환 구현.
  - `parse_regex()` 동작 가능 상태로 구현.

### 문서/계획 정리

- `README.md` 작성:
  - 프로젝트 개요, 실행법, 파일 역할, 현재 상태 정리.
- `TODO.md` 작성:
  - 구현 우선순위 및 권장 순서 정리.

## 2026-06-18

### parser 테스트 고정

- `tests/test_parser.py`를 skip 기반 골격에서 실제 assert 테스트로 전환.
- 아래 입력 케이스 검증 추가:
  - `a`
  - `a+b`
  - `ab`
  - `a*`
  - `a(b+c)*`
  - `aA+b+0c*`

### Thompson NFA 구현

- `nfa.py`:
  - `_build_fragment()` 재귀 방식 구현 (literal, union, concat, star).
  - `build_nfa_from_ast()` 완성.

### NFA 테스트 고정

- `tests/test_nfa.py`를 실제 테스트로 전환.
- literal/union/concat/star 구조 검증 추가.

### subset construction 구현

- `dfa.py`:
  - `epsilon_closure()` 구현.
  - `move()` 구현.
  - `nfa_to_dfa()` 구현.

### DFA 테스트 고정

- `tests/test_dfa.py`를 실제 acceptance/rejection 테스트로 전환.
- `a(b+c)*`에 대해 다수 accept/reject 케이스 검증 추가.

### unreachable state 제거 구현

- `dfa.py`:
  - `remove_unreachable_states()` 구현.
  - 시작 상태에서 BFS로 도달 가능한 상태만 유지하도록 필터링.

### DFA 최소화 구현

- 변경 목적:
  - Reduced DFA 생성을 위한 최소화 단계 구현.
- 수정 파일:
  - `dfa.py`
  - `tests/test_dfa.py`
- 핵심 변경점:
  - `minimize_dfa()`에 partition refinement 기반 최소화 알고리즘 구현.
  - 최소화 전 unreachable 상태를 먼저 제거하도록 구성.
  - 부분 전이 DFA에서도 동치 분할이 안정적으로 동작하도록 누락 전이를 동일 시그니처 요소로 처리.
  - 최소화 전후 언어 보존 + 상태 수 감소를 검증하는 테스트 추가.
- 검증 결과:
  - `python -m unittest tests.test_dfa -v` 통과.
  - `python -m unittest discover -s tests -v` 통과.

### Main.py 낸 패느라인 완성

- 변경 목적:
  - Parser -> NFA -> DFA -> minimize -> rename -> scanner 전 단계를 고차 통합한 main.py CLI 완성.
- 수정 파일:
  - `main.py`
- 핵심 변경점:
  - 계단 3과 9로 번호 순처비. (8간 중복 제거)
  - Scanner 단계를 상태넀(0 또는 skip 공동)로 처리.
  - trace_scan 반환값으로 ACCEPT/REJECT 출력.
- 검증 결과:
  - `python test_main_e2e.py`로 전 패느라인 E2E 테스트 성공.
  - 정규식 "a", 스캠른 값 "ac" 테스트 결과: "REJECT" 정상 동작.
  - `python -m unittest discover -s tests -v` 전체 12개 테스트 통과.

### DFA 상태명 재할당 구현

- 변경 목적:
  - Reduced DFA 상태를 D0, D1, D2 형태로 재할당해 읽기 쉬운 출력 제공.
- 수정 파일:
  - `dfa.py`
- 핵심 변경점:
  - `rename_dfa_states()`에 BFS 기반 결정론적 상태명 할당 구현.
  - 시작 상태를 항상 D0으로 설정.
  - 알파벳 순서로 정렬된 심볼을 따라 BFS 탐색해 D1, D2, ... 순서대로 할당.
  - 매번 같은 입력에 대해 동일한 이름 매핑 보장(결정론적).
- 검증 결과:
  - `a(b+c)*` 예제에서 minimize → rename 파이프라인 통과.
  - 최종 상태명: D0(시작), D1(최종) 확인.
  - `python -m unittest discover -s tests -v` 전체 12개 테스트 통과.

### Scanner 구현

- 변경 목적:
  - Reduced DFA로 입력 문자열을 스캐닝할 scanner 구현.
- 수정 파일:
  - `scanner.py`
- 핵심 변경점:
  - `scan()`: DFA 상태 싱크 입력 스캔, accept/reject 반환.
  - `trace_scan()`: 각 단계의 전이 상태 출력, ACCEPT 시 TOKEN(REGEX_TOKEN, "값") 형식 출력.
- 검증 결과:
  - 간단한 정규식 `a` 문제에서:
    - `scan('a'): True`, `scan('b'): False` 확인.
    - trace_scan 출력 정상.
  - `python -m unittest discover -s tests -v` 전체 12개 테스트 통과.

### Main.py 완 파이프라인 완성

- 변경 목적:
  - Parser -> NFA -> DFA -> minimize -> rename -> scanner 전 단계를 고차 통합한 main.py CLI 완성.
- 수정 파일:
  - `main.py`
- 핵심 변경점:
  - 단계 3과 9로 번호 순정. (8번 중복 제거)
  - Scanner 단계를 상태선택(0 또는 skip 공동)으로 처리.
  - trace_scan 반환값으로 ACCEPT/REJECT 출력.
- 검증 결과:
  - `python test_main_e2e.py`로 전 파이프라인 E2E 테스트 성공.
  - 정규식 "a", 스캔 값 "ac" 테스트 결과: "REJECT" 정상 동작.
  - `python -m unittest discover -s tests -v` 전체 12개 테스트 통과.

### Parser D3 AST 시각화 추가

- 변경 목적:
  - 과제 요구사항에 맞춰 parser 단독 실행 시 D3 tree 형태 AST 시각화 제공.
- 수정 파일:
  - `regex_parser.py`
- 핵심 변경점:
  - `_ast_to_d3_tree()` 추가: AST를 D3 hierarchy JSON 구조로 변환.
  - `generate_d3_ast_html()` 추가: `ast_tree.html` 자동 생성.
  - `main()` 실행 시 AST 출력 후 시각화 HTML 생성 및 기본 브라우저 자동 오픈.
  - 브라우저 자동 오픈 실패 시 수동 오픈 안내 메시지 출력.
- 검증 결과:
  - `"a(b+c)*" | python regex_parser.py` 실행.
  - AST nested list 출력 확인.
  - `ast_tree.html` 생성 확인.
  - 기본 브라우저 자동 오픈 확인.

### README 최신 상태 동기화

- 변경 목적:
  - 실제 구현 상태와 README 문서 간 불일치 해소.
- 수정 파일:
  - `README.md`
  - `LOG.md`
- 핵심 변경점:
  - `main.py` 전체 파이프라인 완성 상태 반영.
  - `regex_parser.py` 단독 실행 + D3 시각화(`ast_tree.html`) 반영.
  - NFA/DFA/scanner 설명을 TODO 중심에서 구현 완료 중심으로 수정.
  - 테스트 섹션을 skeleton 안내에서 실제 12개 검증 상태로 수정.
- 검증 결과:
  - README 내용과 현재 코드(`main.py`, `regex_parser.py`, `nfa.py`, `dfa.py`, `scanner.py`, `tests/*`) 대조 확인.

## 현재 상태 요약

완료:

- Parser/AST
- Thompson NFA
- NFA -> DFA(subset construction)
- unreachable state 제거
- DFA 최소화
- Reduced DFA 상태명 변환
- Scanner
- main.py 완 파이프라인
- parser D3 AST 시각화
- parser/NFA/DFA/scanner 기본 테스트

미완료:

- 출력 형식 고도화
- 추가 edge case 테스트

## 운영 규칙

- 이후 모든 채팅/작업에서 변경사항이 생길 때마다 즉시 이 파일에 새 항목을 추가한다.
- 항목은 날짜 기준으로 누적한다.
- 각 항목은 다음 구조를 유지한다:
  - 변경 목적
  - 수정 파일
  - 핵심 변경점
  - 검증 결과
