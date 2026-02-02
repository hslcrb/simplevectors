# Security Policy

## Supported Versions

Currently, the following versions of SimpleVectors are supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| v0.0.x  | ✅ Yes            |
| < v0.0.0| ❌ No             |

## Reporting a Vulnerability

We take the security of SimpleVectors seriously. If you find a security vulnerability, please do NOT open a public issue. Instead, follow these steps:

1. **Email us**: Send a detailed report to `security@rhee.kr` (Placeholder - Replace with actual contact).
2. **Details**: Include a description of the vulnerability, steps to reproduce, and potential impact.
3. **Response**: We will acknowledge your report within 48 hours and provide a timeline for a fix.

## Security Practices

- **Dependency Scanning**: We use automated tools to scan for vulnerable dependencies in our `requirements.txt`.
- **Sandboxing**: When running in Docker, we recommend using non-root users where possible.
- **Data Privacy**: SimpleVectors is a local-first application. Your vector files are processed entirely on your machine and are never uploaded to our servers unless you explicitly share them.

---

# 보안 정책 (Security Policy)

## 지원되는 버전

현재 다음 버전의 SimpleVectors 가 보안 업데이트를 지원받습니다:

| 버전    | 지원 여부          |
| ------- | ------------------ |
| v0.0.x  | ✅ 지원 중         |
| < v0.0.0| ❌ 지원 안 함      |

## 취약점 보고 방법

SimpleVectors의 보안을 중요하게 생각합니다. 보안 취약점을 발견한 경우 공개적인 이슈를 생성하지 마시고 다음 절차를 따라주세요:

1. **이메일 보고**: `security@rhee.kr` (실제 연락처로 변경 필요)로 상세 보고서를 보내주세요.
2. **상세 내용**: 취약점 설명, 재현 방법, 예상되는 영향력을 포함해 주세요.
3. **대응**: 48시간 이내에 보고 내용을 확인하고 해결 일정을 안내해 드립니다.

## 보안 관리 방식

- **의존성 검사**: `requirements.txt`에 명시된 라이브러리들의 취약점을 정기적으로 검사합니다.
- **데이터 프라이버시**: SimpleVectors는 로컬 중심 애플리케이션입니다. 모든 벡터 파일 처리는 사용자의 기기에서 이루어지며, 명시적으로 공유하지 않는 한 서버로 전송되지 않습니다.
