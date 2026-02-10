# Login 기능 개발 계획

## 개요
사용자 인증 및 로그인 기능을 구현하기 위한 feature 단위 개발 계획

---

## Feature 1: 사용자 모델 및 데이터베이스 설정

### BE
- [ ] User 모델 생성 (`backend/app/models/user.py`)
  - id, username, email, hashed_password, created_at 필드
- [ ] 데이터베이스 마이그레이션 설정
- [ ] User 스키마 생성 (`backend/app/schemas/user.py`)
  - UserCreate, UserResponse, UserInDB

### FE
- 해당 없음

### Kernel
- 해당 없음

---

## Feature 2: 비밀번호 해싱 및 보안

### BE
- [ ] 비밀번호 해싱 유틸리티 구현 (`backend/app/utils/security.py`)
  - bcrypt 또는 passlib 사용
  - `hash_password()`, `verify_password()` 함수
- [ ] 환경변수 설정 (SECRET_KEY, ALGORITHM)
- [ ] .env 파일 구성

### FE
- 해당 없음

### Kernel
- 해당 없음

---

## Feature 3: JWT 토큰 시스템

### BE
- [ ] JWT 토큰 생성/검증 함수 구현 (`backend/app/utils/jwt.py`)
  - `create_access_token()`, `verify_token()`
- [ ] 토큰 의존성 함수 생성 (`get_current_user`)
- [ ] 토큰 만료 시간 설정 (ACCESS_TOKEN_EXPIRE_MINUTES)
- [ ] 토큰 스키마 생성 (Token, TokenData)

### FE
- 해당 없음

### Kernel
- 해당 없음

---

## Feature 4: 회원가입 API

### BE
- [ ] 회원가입 엔드포인트 구현 (`/auth/register`)
  - POST /api/auth/register
  - 중복 사용자 검증
  - 비밀번호 해싱 후 저장
- [ ] 회원가입 라우터 생성 (`backend/app/routers/auth.py`)
- [ ] 에러 핸들링 (이미 존재하는 사용자)

### FE
- [ ] 회원가입 페이지 생성 (`frontend/src/app/register/page.tsx`)
- [ ] 회원가입 폼 컴포넌트
  - username, email, password, confirm password 입력
- [ ] 폼 유효성 검증 (클라이언트 측)
- [ ] 회원가입 API 호출 함수

### Kernel
- 해당 없음

---

## Feature 5: 로그인 API

### BE
- [ ] 로그인 엔드포인트 구현 (`/auth/login`)
  - POST /api/auth/login
  - 사용자 인증 (username/email + password)
  - JWT 토큰 발급
- [ ] 로그인 실패 처리 (잘못된 자격증명)
- [ ] OAuth2PasswordRequestForm 사용

### FE
- 해당 없음

### Kernel
- 해당 없음

---

## Feature 6: 로그인 UI 구현

### BE
- 해당 없음

### FE
- [ ] 로그인 페이지 생성 (`frontend/src/app/login/page.tsx`)
- [ ] 로그인 폼 컴포넌트
  - username/email 입력
  - password 입력
  - "로그인 유지" 체크박스 (선택)
- [ ] 로그인 버튼 및 회원가입 링크
- [ ] Tailwind CSS로 스타일링
- [ ] 로딩 상태 및 에러 메시지 표시

### Kernel
- 해당 없음

---

## Feature 7: 인증 상태 관리

### BE
- [ ] 현재 사용자 정보 조회 API (`/auth/me`)
  - GET /api/auth/me
  - JWT 토큰 검증 후 사용자 정보 반환

### FE
- [ ] 로그인 API 연동 (`frontend/src/lib/api/auth.ts`)
  - login(), register(), getCurrentUser() 함수
- [ ] 토큰 저장 (localStorage 또는 cookie)
- [ ] 인증 컨텍스트 생성 (`frontend/src/contexts/AuthContext.tsx`)
  - useAuth 훅 구현
  - 로그인/로그아웃 상태 관리
- [ ] API 요청 시 Authorization 헤더 자동 추가

### Kernel
- 해당 없음

---

## Feature 8: 보호된 라우트 구현

### BE
- [ ] 보호된 엔드포인트 예시 생성
  - 인증 필요한 API에 `Depends(get_current_user)` 적용

### FE
- [ ] 보호된 라우트 컴포넌트 (`frontend/src/components/ProtectedRoute.tsx`)
  - 인증되지 않은 사용자는 로그인 페이지로 리다이렉트
- [ ] 네비게이션 가드 구현
- [ ] 미들웨어 또는 HOC 패턴 적용
- [ ] 보호된 페이지 예시 생성 (대시보드 등)

### Kernel
- 해당 없음

---

## Feature 9: 로그아웃 기능

### BE
- [ ] 로그아웃 엔드포인트 구현 (`/auth/logout`)
  - POST /api/auth/logout
  - 토큰 블랙리스트 관리 (선택적)

### FE
- [ ] 로그아웃 버튼 구현
- [ ] 로그아웃 시 토큰 삭제
- [ ] 로그아웃 후 로그인 페이지로 리다이렉트
- [ ] 전역 상태 초기화
- [ ] 헤더/네비게이션에 로그인 상태 표시

### Kernel
- 해당 없음

---

## Feature 10: 에러 처리 및 보안 강화 (선택)

### BE
- [ ] Rate limiting 구현 (로그인 시도 제한)
- [ ] CORS 설정 검토
- [ ] HTTPS 강제 설정
- [ ] 비밀번호 복잡도 검증
- [ ] 에러 로깅

### FE
- [ ] 전역 에러 바운더리
- [ ] 네트워크 에러 처리
- [ ] 토큰 자동 갱신 (Refresh Token, 선택)
- [ ] 비밀번호 표시/숨김 토글

### Kernel
- [ ] (선택) 로그인 시도 로깅 (보안 감사)
- [ ] (선택) 비정상 접근 패턴 탐지

---

## 개발 순서 권장

1. Feature 1 → Feature 2 → Feature 3 (BE 기반 설정)
2. Feature 4 → Feature 5 (인증 API 구현)
3. Feature 6 → Feature 7 (FE 기본 UI 및 연동)
4. Feature 8 → Feature 9 (보호 기능 및 로그아웃)
5. Feature 10 (선택적 보안 강화)

---

## 의존성 추가 필요

### Backend
```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

### Frontend
```bash
npm install jwt-decode
# 또는 상태관리 라이브러리 (zustand, redux 등)
```

---

## 참고사항

- JWT 토큰은 httpOnly 쿠키 또는 localStorage에 저장 (보안 고려)
- HTTPS 환경에서만 프로덕션 배포
- 환경변수는 `.env` 파일에 저장하고 `.gitignore`에 추가
- 비밀번호는 절대 평문으로 저장하지 않음
