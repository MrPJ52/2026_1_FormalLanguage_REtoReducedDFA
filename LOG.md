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

## 현재 상태 요약

완료:

- Parser/AST
- Thompson NFA
- NFA -> DFA(subset construction)
- unreachable state 제거
- parser/NFA/DFA 기본 테스트

미완료:

- DFA 최소화 (`minimize_dfa`)
- Reduced DFA 상태명 변환 (`rename_dfa_states`)
- scanner (`scan`, `trace_scan`)
- 출력 형식 고도화

## 운영 규칙

- 이후 모든 채팅/작업에서 코드 또는 문서 변경이 발생하면 이 파일에 새 항목을 추가한다.
- 항목은 날짜 기준으로 누적한다.
- 각 항목은 다음 구조를 유지한다:
  - 변경 목적
  - 수정 파일
  - 핵심 변경점
  - 검증 결과
