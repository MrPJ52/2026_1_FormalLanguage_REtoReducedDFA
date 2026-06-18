# TODO

현재 핵심 파이프라인(parser -> e-NFA -> DFA -> Reduced DFA -> scanner)은 구현 완료 상태이다.
아래는 남은 개선 항목 위주로 정리한 TODO이다.

## High Priority

1. `main.py` 출력 포맷을 제출 형식에 맞게 최종 점검
2. scanner accept/reject 메시지 규격(`TOKEN(...)` 등) 확정 및 반영
3. edge case 테스트(잘못된 연산자 배치, 괄호 오류, 빈 입력 등) 보강

## Output And UX

1. Reduced DFA 전이 출력을 NFA와 동일한 ASCII table 스타일로 통일
2. 단계별 출력에 section title/summary를 더 간결하게 정리
3. reject 시 dead transition 위치를 추가로 출력할지 결정

## Testing

1. 통합 시나리오 테스트 추가(`main.py` 기준 입력/출력 흐름)
2. 복잡한 regex 케이스(중첩 star/union/concat) 테스트 확장
3. 테스트 개수 및 커버리지 요약을 README에 반영

## Documentation

1. README에 실제 `nfa.py`, `dfa.py` 실행 예시 출력 추가
2. 알고리즘 설명 섹션(Thompson, subset construction, minimization) 보강
3. arc upper bound 정의와 exact arc count 계산 규칙 명시

## Optional

1. AST JSON export 형식 구체화
2. automaton JSON schema 정의
3. 추후 D3.js 시각화용 데이터 구조 분리
4. 상태 이름 정렬 규칙을 고정해 출력 재현성 높이기

## Completed (Reference)

1. parser/AST 구현
2. Thompson e-NFA 구현
3. subset construction 기반 DFA 구현
4. unreachable 제거 및 DFA 최소화 구현
5. Reduced DFA state renaming 구현
6. scanner(`scan`, `trace_scan`) 구현
7. `regex_parser.py` 단독 실행 + D3 시각화 구현
8. `nfa.py`, `dfa.py` 단독 실행 CLI 구현
