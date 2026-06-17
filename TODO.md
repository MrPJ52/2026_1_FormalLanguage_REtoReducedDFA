# TODO

현재 프로젝트는 parser 중심 골격까지 준비된 상태이다. 아래 항목을 순서대로 구현하면 전체 과제를 무리 없이 확장할 수 있다.

## High Priority

1. `nfa.py`의 Thompson construction 구현
2. `printer.py`에서 NFA transition table 출력 형식 정리
3. `tests/test_nfa.py`에 literal, union, concat, star 검증 추가
4. `dfa.py`의 `epsilon_closure()` 구현
5. `dfa.py`의 `move()` 구현
6. `dfa.py`의 `nfa_to_dfa()` 구현
7. `tests/test_dfa.py`에 subset construction 기반 accept/reject 검증 추가
8. `dfa.py`의 `remove_unreachable_states()` 구현
9. `dfa.py`의 `minimize_dfa()` 구현
10. `dfa.py`의 `rename_dfa_states()` 구현
11. `scanner.py`의 `scan()` 구현
12. `scanner.py`의 `trace_scan()` 구현

## Parser Follow-up

1. `tests/test_parser.py`를 실제 assert 기반 테스트로 전환
2. 잘못된 괄호 입력, 잘못된 연산자 배치 등 예외 케이스 추가
3. `insert_concat()` 결과를 직접 검증하는 단위 테스트 추가
4. 필요하면 `.` 입력도 concatenation으로 허용할지 결정

## Output And UX

1. AST 출력 포맷을 과제 제출용 표기와 최대한 맞추기
2. NFA/DFA transition table을 열 기반 표 형식으로 개선
3. 단계별 출력에 section title과 summary를 더 명확히 추가
4. accept 시 `TOKEN(REGEX_TOKEN, "입력문자열")` 형식 정확히 맞추기
5. reject 시 실패 위치 또는 dead transition 정보 출력 여부 결정

## Documentation

1. README에 실제 NFA/DFA 예시 출력 추가
2. 구현 완료 후 알고리즘 설명 섹션 보강
3. minimization 방법이 확정되면 해당 절차 문서화

## Optional

1. AST JSON export 형식 구체화
2. automaton JSON schema 정의
3. 추후 D3.js 시각화용 데이터 구조 분리
4. 상태 이름 정렬 규칙을 고정해 출력 재현성 높이기

## Suggested Implementation Order

1. parser 테스트 고정
2. Thompson NFA 구현
3. NFA 테스트 작성
4. subset construction 구현
5. DFA acceptance 테스트 작성
6. unreachable 제거 및 minimization 구현
7. scanner 구현
8. 출력 포맷 정리
