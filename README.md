# 2026_1_FormalLanguage_REtoReducedDFA

Formal Language 과목 과제를 위한 Python 프로젝트이다. 목표는 정규표현식을 입력받아 AST를 만들고, Thompson construction 기반의 epsilon-NFA, subset construction 기반 DFA, 최소화된 Reduced DFA를 거쳐 최종적으로 scanner 방식으로 문자열을 판별하는 것이다.

현재 저장소는 전체 알고리즘을 바로 완성한 상태가 아니라, 이후 단계별 구현을 쉽게 진행할 수 있도록 파일 구조, 핵심 클래스, 함수 시그니처, CLI 흐름, 테스트 골격을 먼저 잡아 둔 상태이다.

## Current Status

- 프로젝트 파일 구조가 분리되어 있다.
- AST 노드 구조와 nested list 출력이 구현되어 있다.
- 정규표현식 파서는 현재 기본 동작한다.
- 접속 연산 생략 입력을 내부적으로 명시적 연산자 `·`로 바꿀 수 있다.
- shunting-yard 방식으로 postfix 변환 후 AST를 만든다.
- AST size와 Thompson 상태 수, arc 수의 추정치 출력이 가능하다.
- NFA, DFA, Reduced DFA, scanner 단계는 아직 구현 전이며 `NotImplementedError`와 `TODO`로 골격만 준비되어 있다.
- 테스트 파일은 현재 `skip` 기반 골격이다.

## Supported Regex Rules

- literal symbol: 영어 대소문자, 숫자 `0-9`
- union: `+`
- Kleene star: `*`
- concatenation: 입력에서는 생략되며 내부적으로 `·`를 삽입
- grouping: `(`, `)`

우선순위는 다음과 같다.

1. `*`
2. concatenation
3. `+`

`+`와 concatenation은 좌결합으로 처리한다.

## Project Structure

```text
2026_1_FormalLanguage_REtoReducedDFA/
	main.py
	regex_parser.py
	ast_node.py
	nfa.py
	dfa.py
	scanner.py
	printer.py
	tests/
		test_parser.py
		test_nfa.py
		test_dfa.py
```

## File Overview

### main.py

CLI 진입점이다. 전체 파이프라인을 단계별로 호출하고, 아직 구현되지 않은 단계는 `[PENDING]` 메시지와 함께 중단한다.

현재 흐름은 다음과 같다.

1. 정규표현식 입력
2. AST 생성 및 출력
3. AST size, Thompson 상태 수 및 arc 수 출력
4. epsilon-NFA 생성 시도
5. DFA 생성 시도
6. Reduced DFA 생성 시도
7. scanner trace 시도

### ast_node.py

정규표현식 AST 노드 자료구조를 정의한다.

- `Node`
- `size()`
- `to_nested_list()`
- `count_thompson_states_arcs()`

### regex_parser.py

정규표현식 문자열을 AST로 변환한다.

- `is_literal(ch)`
- `tokenize(regex)`
- `insert_concat(tokens)`
- `to_postfix(tokens)`
- `postfix_to_ast(postfix_tokens)`
- `parse_regex(regex)`

현재 프로젝트에서 가장 먼저 동작하는 핵심 모듈이다.

### nfa.py

AST를 Thompson construction으로 epsilon-NFA로 바꾸기 위한 골격이다.

- `NFA`
- `NFAFragment`
- `build_nfa_from_ast(ast)`
- `new_state()`
- `add_transition(src, symbol, dst)`

현재는 자료구조만 준비되어 있고 핵심 알고리즘은 TODO 상태이다.

### dfa.py

subset construction, 도달 불가능 상태 제거, DFA 최소화, 보기 좋은 상태명 재할당을 담당할 예정인 골격이다.

- `DFA`
- `epsilon_closure(nfa, states)`
- `move(nfa, states, symbol)`
- `nfa_to_dfa(nfa)`
- `remove_unreachable_states(dfa)`
- `minimize_dfa(dfa)`
- `rename_dfa_states(dfa)`

### scanner.py

Reduced DFA를 사용해 입력 문자열을 scanner 방식으로 추적 출력할 골격이다.

- `scan(dfa, input_string)`
- `trace_scan(dfa, input_string)`

### printer.py

AST, NFA, DFA를 콘솔에 보기 좋게 출력하는 유틸리티 모듈이다. 향후 D3.js 시각화를 위한 JSON export 함수 자리도 미리 만들어 두었다.

### tests/

현재는 구현 순서를 잡기 위한 테스트 골격만 있다.

- `test_parser.py`: parser expected AST TODO
- `test_nfa.py`: Thompson construction TODO
- `test_dfa.py`: DFA acceptance TODO

## How To Run

Python 3.11 이상 기준이다.

프로젝트 루트에서 실행한다.

```bash
python main.py
```

예시 입력:

```text
aA+b+0c*
```

현재 기준 예상 동작:

- AST nested list 출력
- AST size 출력
- Thompson 상태 수, arc 수 추정치 출력
- NFA 단계에서 아직 미구현 메시지 출력 후 종료

## How To Run Tests

```bash
python -m unittest discover -s tests -v
```

현재 테스트는 skeleton이므로 대부분 `skipped`로 표시되는 것이 정상이다.

## Example Parse Result

입력:

```text
aA+b+0c*
```

내부 접속 연산 삽입 후 개념적으로는 다음과 같다.

```text
a·A+b+0·c*
```

현재 parser가 만드는 nested list 결과:

```text
['+', ['+', ['·', 'a', 'A'], 'b'], ['·', '0', ['*', 'c']]]
```

## Notes

- 괄호는 AST에서 별도 노드로 만들지 않고 결합 구조만 조정한다.
- NFA 이후 단계는 아직 intentionally incomplete 상태이다.
- 앞으로 구현 순서는 [TODO.md](TODO.md)를 기준으로 진행하면 된다.
