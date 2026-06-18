# 2026_1_FormalLanguage_REtoReducedDFA

Formal Language 과목 과제를 위한 Python 프로젝트이다. 정규표현식을 입력받아 AST를 만들고, Thompson construction 기반 epsilon-NFA, subset construction 기반 DFA, 최소화된 Reduced DFA를 거쳐 scanner 방식으로 문자열을 판별한다.

## Current Status

- Parser/AST 구현 완료
- Thompson epsilon-NFA 생성 구현 완료
- NFA -> DFA(subset construction) 구현 완료
- DFA unreachable state 제거 구현 완료
- DFA 최소화(`minimize_dfa`) 구현 완료
- Reduced DFA 상태명 재할당(`rename_dfa_states`) 구현 완료
- Scanner(`scan`, `trace_scan`) 구현 완료
- `main.py` 전체 파이프라인 실행 가능
- `regex_parser.py` 단독 실행 + D3 AST 시각화 HTML 생성/오픈 지원
- 테스트 12개 동작(파서 6, NFA 4, DFA 2)

## Supported Regex Rules

- literal symbol: 영어 대소문자, 숫자 `0-9`
- union: `+`
- Kleene star: `*`
- concatenation: 입력에서는 생략되며 내부적으로 `·` 삽입
- grouping: `(`, `)`

우선순위:

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
	ast_tree.html
	tests/
		test_parser.py
		test_nfa.py
		test_dfa.py
```

## File Overview

### main.py

전체 파이프라인 CLI 진입점.

1. 정규표현식 입력
2. AST 생성/출력 + AST 메트릭 출력
3. epsilon-NFA 생성/출력
4. DFA 생성/출력
5. unreachable state 제거
6. DFA 최소화
7. Reduced DFA 상태명 재할당/출력
8. 입력 문자열 scanner trace 및 ACCEPT/REJECT 출력

### regex_parser.py

정규표현식 파서 모듈.

- `is_literal(ch)`
- `tokenize(regex)`
- `insert_concat(tokens)`
- `to_postfix(tokens)`
- `postfix_to_ast(postfix_tokens)`
- `parse_regex(regex)`
- `_ast_to_d3_tree(node)`
- `generate_d3_ast_html(ast, output_path)`

직접 실행 시 parser demo + D3 트리 시각화를 제공한다.

### ast_node.py

AST 노드 자료구조.

- `Node`
- `size()`
- `to_nested_list()`
- `count_thompson_states_arcs()`

### nfa.py

Thompson construction 구현.

- `NFA`
- `NFAFragment`
- `_build_fragment(nfa, ast)`
- `build_nfa_from_ast(ast)`

### dfa.py

DFA 관련 알고리즘 구현.

- `DFA`
- `epsilon_closure(nfa, states)`
- `move(nfa, states, symbol)`
- `nfa_to_dfa(nfa)`
- `remove_unreachable_states(dfa)`
- `minimize_dfa(dfa)`
- `rename_dfa_states(dfa)`

### scanner.py

Reduced DFA 기반 입력 스캔/추적.

- `scan(dfa, input_string)`
- `trace_scan(dfa, input_string)`

### printer.py

AST, NFA, DFA 출력 유틸리티.

### tests/

- `test_parser.py`: 파서 AST 결과 검증(6개)
- `test_nfa.py`: Thompson construction 구조 검증(4개)
- `test_dfa.py`: DFA 수용성/최소화 검증(2개)

## How To Run

Python 3.11 이상 기준.

프로젝트 루트에서:

```bash
python main.py
```

## Parser-Only + D3 Visualization

파서만 단독 실행하고 AST를 D3 트리로 시각화하려면:

```bash
python regex_parser.py
```

동작:

- 콘솔에서 정규표현식 입력
- AST nested list 출력
- `ast_tree.html` 생성
- 기본 브라우저 자동 오픈 시도

## How To Run Tests

```bash
python -m unittest discover -s tests -v
```

현재 테스트는 skeleton이 아니라 실제 검증 테스트이며, 최근 기준 12개가 통과한다.

## Example Parse Result

입력:

```text
aA+b+0c*
```

내부 접속 연산 삽입 개념:

```text
a·A+b+0·c*
```

AST nested list:

```text
['+', ['+', ['·', 'a', 'A'], 'b'], ['·', '0', ['*', 'c']]]
```

## Notes

- 괄호는 AST에서 별도 노드로 만들지 않고 결합 구조만 조정한다.
- 시각화 HTML은 D3 CDN(`https://d3js.org/d3.v7.min.js`)을 사용하므로 브라우저 네트워크 접근이 필요하다.

## Development Logging Rule

- 개발 이력은 [LOG.md](LOG.md)에 날짜 순으로 누적 기록한다.
- 이후 다른 채팅에서 작업하더라도 변경사항이 생길 때마다 즉시 [LOG.md](LOG.md)를 업데이트한다.
- 권장 기록 포맷:
  - 변경 목적
  - 수정 파일
  - 핵심 변경점
  - 검증 결과
