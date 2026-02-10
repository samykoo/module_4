# Progress Log

## 2026-02-10: Login 기능 개발 시작

### Feature 1: 사용자 모델 및 데이터베이스 설정 ✅

**목적**: 사용자 인증 시스템의 기반이 되는 데이터베이스 모델과 Pydantic 스키마 구현

#### 구현 내용

##### 1. User 모델 생성 (`backend/app/models/user.py`)
- SQLAlchemy ORM 모델 생성
- 필드 구성:
  - `id`: Integer, Primary Key
  - `username`: String(50), unique, nullable=False, indexed
  - `email`: String(100), unique, nullable=False, indexed
  - `hashed_password`: String(255), nullable=False
  - `created_at`: DateTime, 자동 생성 (server_default)
- 기존 Example 모델 패턴 준수

##### 2. User 스키마 생성 (`backend/app/schemas/user.py`)
- **UserCreate**: 회원가입 입력 스키마
  - username (3-50자), email (EmailStr), password (8-100자)
  - Pydantic Field 검증 적용
- **UserResponse**: API 응답 스키마
  - id, username, email, created_at 포함
  - **비밀번호 필드 완전 제외** (보안)
- **UserInDB**: 내부 로직용 스키마
  - 모든 필드 포함 (hashed_password 포함)
  - 외부 노출 금지

##### 3. 패키지 구조 업데이트
- `backend/app/models/__init__.py`: User 모델 export 추가
- `backend/app/schemas/__init__.py`: User 스키마 3개 export 추가

##### 4. 의존성 설치
- `pydantic[email]` 패키지 설치 (EmailStr 타입 지원)

#### 생성된 파일
- `backend/app/models/user.py`
- `backend/app/schemas/user.py`

#### 수정된 파일
- `backend/app/models/__init__.py`
- `backend/app/schemas/__init__.py`

#### 데이터베이스 변경
- `users` 테이블 자동 생성 (main.py의 `Base.metadata.create_all()`)
- 인덱스 생성: `ix_users_id`, `ix_users_username`, `ix_users_email`
- Unique 제약: username, email

#### 검증 완료
- ✓ SQLite 테이블 생성 확인
- ✓ Unique 제약 조건 동작 확인
- ✓ Pydantic 이메일 검증 동작 확인
- ✓ UserResponse에서 비밀번호 제외 확인
- ✓ ORM → Pydantic 변환 정상 작동
- ✓ FastAPI 서버 정상 시작

#### 보안 원칙
- 비밀번호는 `hashed_password` 필드로만 저장
- API 응답(`UserResponse`)에서 비밀번호 완전 제외
- username, email 중복 방지 (unique 제약)

#### 다음 단계
- Feature 2: 비밀번호 해싱 및 보안 (`backend/app/utils/security.py`)
- Feature 3: JWT 토큰 시스템
- Feature 4: 회원가입 API (`/auth/register`)

---
