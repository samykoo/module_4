"""
Feature 1 Test: User Model & Schema
"""
# -*- coding: utf-8 -*-
import sys
import os

# Windows 인코딩 문제 해결
if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, '.')

def test_model_import():
    """모델 import 테스트"""
    print('=== 1. Model Import Test ===')
    try:
        from app.models import User
        print(f'✓ User model imported successfully')
        print(f'  Table name: {User.__tablename__}')
        print(f'  Columns: {list(User.__table__.columns.keys())}')
        return True
    except Exception as e:
        print(f'✗ Failed to import User model: {e}')
        return False

def test_schema_import():
    """스키마 import 테스트"""
    print('\n=== 2. Schema Import Test ===')
    try:
        from app.schemas import UserCreate, UserResponse, UserInDB
        print(f'✓ UserCreate imported')
        print(f'✓ UserResponse imported')
        print(f'✓ UserInDB imported')
        return True
    except Exception as e:
        print(f'✗ Failed to import schemas: {e}')
        return False

def test_schema_validation():
    """스키마 검증 테스트"""
    print('\n=== 3. Schema Validation Test ===')
    from app.schemas import UserCreate

    passed = 0
    failed = 0

    # 정상 데이터 테스트
    try:
        user_data = UserCreate(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        print(f'✓ Valid user data accepted')
        passed += 1
    except Exception as e:
        print(f'✗ Valid data rejected: {e}')
        failed += 1

    # 잘못된 이메일 테스트
    try:
        invalid_user = UserCreate(
            username='test',
            email='not-an-email',
            password='pass1234'
        )
        print(f'✗ Invalid email should have been rejected')
        failed += 1
    except Exception as e:
        print(f'✓ Email validation working (rejected invalid email)')
        passed += 1

    # 짧은 username 테스트
    try:
        short_username = UserCreate(
            username='ab',  # 3자 미만
            email='test@example.com',
            password='password123'
        )
        print(f'✗ Short username should have been rejected')
        failed += 1
    except Exception as e:
        print(f'✓ Username length validation working (min 3 chars)')
        passed += 1

    # 짧은 password 테스트
    try:
        short_password = UserCreate(
            username='testuser',
            email='test@example.com',
            password='pass'  # 8자 미만
        )
        print(f'✗ Short password should have been rejected')
        failed += 1
    except Exception as e:
        print(f'✓ Password length validation working (min 8 chars)')
        passed += 1

    print(f'\nValidation Tests: {passed} passed, {failed} failed')
    return failed == 0

def test_database_table():
    """데이터베이스 테이블 확인"""
    print('\n=== 4. Database Table Test ===')
    try:
        from app.database import engine
        from sqlalchemy import inspect

        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f'✓ Database tables: {tables}')

        if 'users' in tables:
            print(f'✓ users table exists')
            columns = inspector.get_columns('users')
            print(f'  Columns:')
            for col in columns:
                print(f'    - {col["name"]}: {col["type"]}')

            # 인덱스 확인
            indexes = inspector.get_indexes('users')
            print(f'  Indexes:')
            for idx in indexes:
                print(f'    - {idx["name"]}: {idx["column_names"]}')

            return True
        else:
            print(f'✗ users table not found')
            return False
    except Exception as e:
        print(f'✗ Database error: {e}')
        return False

def test_orm_operations():
    """ORM 기본 동작 테스트"""
    print('\n=== 5. ORM Operations Test ===')
    try:
        from app.database import SessionLocal
        from app.models import User
        from app.schemas import UserResponse

        db = SessionLocal()

        # 기존 테스트 데이터 삭제
        db.query(User).filter(User.username == 'orm_test_user').delete()
        db.commit()

        # 사용자 생성
        test_user = User(
            username='orm_test_user',
            email='orm_test@example.com',
            hashed_password='fake_hash_for_testing'
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f'✓ User created with ID: {test_user.id}')

        # 조회 테스트
        user = db.query(User).filter(User.username == 'orm_test_user').first()
        if user:
            print(f'✓ User retrieved: {user.email}')
        else:
            print(f'✗ User not found')
            return False

        # Pydantic 변환 테스트
        user_response = UserResponse.model_validate(user)
        response_dict = user_response.model_dump()

        if 'hashed_password' in response_dict:
            print(f'✗ hashed_password should not be in UserResponse')
            return False
        else:
            print(f'✓ UserResponse excludes hashed_password (security check passed)')

        print(f'  Response fields: {list(response_dict.keys())}')

        # 정리
        db.delete(test_user)
        db.commit()
        db.close()

        return True
    except Exception as e:
        print(f'✗ ORM error: {e}')
        import traceback
        traceback.print_exc()
        return False

def main():
    print('=' * 60)
    print('Feature 1 Test Suite: User Model & Schema')
    print('=' * 60)

    results = []

    results.append(('Model Import', test_model_import()))
    results.append(('Schema Import', test_schema_import()))
    results.append(('Schema Validation', test_schema_validation()))
    results.append(('Database Table', test_database_table()))
    results.append(('ORM Operations', test_orm_operations()))

    print('\n' + '=' * 60)
    print('Test Summary')
    print('=' * 60)

    for name, passed in results:
        status = '✓ PASS' if passed else '✗ FAIL'
        print(f'{status}: {name}')

    total = len(results)
    passed = sum(1 for _, p in results if p)

    print(f'\nTotal: {passed}/{total} tests passed')

    if passed == total:
        print('\n🎉 All tests passed!')
        return 0
    else:
        print(f'\n⚠️  {total - passed} test(s) failed')
        return 1

if __name__ == '__main__':
    exit(main())
