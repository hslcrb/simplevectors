# SimpleVectors v0.0.0

A powerful and modular vector graphics editor capable of opening, saving, converting, and modifying vector files (SVG, EPS).

[![CI/CD Pipeline](https://github.com/hslcrb/simplevectors/actions/workflows/pipeline.yml/badge.svg)](https://github.com/hslcrb/simplevectors/actions/workflows/pipeline.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

SimpleVectors provides a clean, modular interface for managing vector assets. It is designed for both quick format conversions and detailed element-level editing.

## 🚀 Key Features
- **Open & Save**: Full support for industry-standard SVG and EPS formats.
- **Image Tracing**: Transform bitmap images (PNG, JPG) into clean SVG vector paths with smart presets.
- **Professional Editing Tools**:
  - **Grouping & Ungrouping**: Manage complex hierarchies with ease.
  - **Live Color Picker**: Instantly update element fill and stroke colors.
  - **Intelligent Deletion**: Remove individual objects or entire groups.
  - **History Management**: Full Undo/Redo support (`Ctrl+Z` / `Ctrl+Shift+Z`).
- **Modern Interactive Interface**:
  - **High-Performance Canvas**: Supports smooth zooming and panning.
  - **Area Selection**: Select multiple items by dragging or using Modifier-clicks.
  - **Smart Context Menu**: Quick access to all transformation tools via right-click.
- **Advanced Export**: Save work as SVG, PDF, or EPS, including individual element exports.
- **Bilingual Interface**: Seamlessly switch between English and Korean (Automatic detection).

## 🛠 Project Structure
```text
simplevectors/
├── src/
│   ├── core/          # Business logic: SVG parsing, Image tracing
│   ├── ui/            # Graphical interface: Canvas, Main Window
│   └── assets/        # Resources: i18n, icons
├── .github/           # Automation: CI/CD Workflows
├── Dockerfile         # Container orchestration
└── run.sh             # Unified entry point
```

## 📦 Deployment & Releases
- **Standalone Binaries**: Pre-compiled executables for **Windows (.exe)**, **Linux**, and **macOS** are automatically generated on every update.
  - 🔗 [Download Latest Releases](https://github.com/hslcrb/simplevectors/releases)
- **Dockerized Environment**: Run SimpleVectors in a consistent environment.
  ```bash
  docker pull ghcr.io/hslcrb/simplevectors:latest
  ```
- **Automated Versioning**: Versions follow `v0.0.x` format, incrementing every 10 commits.

## 📚 Documentation
For detailed guides and tutorials, visit our **[Project Wiki](https://github.com/hslcrb/simplevectors/wiki)**.

## 🏁 Getting Started
### Local Execution
Ensure you have Python 3.12+ installed, then run:
```bash
./run.sh
```

### Development
1. Create a virtual environment: `python -m venv venv`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch: `python -m src.main`

---

# SimpleVectors (심플벡터) v0.0.0

SVG, EPS 등 벡터 파일을 열고, 저장하고, 변환하며 정밀하게 편집할 수 있는 강력한 모듈형 벡터 그래픽 편집기입니다.

[![CI/CD Pipeline](https://github.com/hslcrb/simplevectors/actions/workflows/pipeline.yml/badge.svg)](https://github.com/hslcrb/simplevectors/actions/workflows/pipeline.yml)

SimpleVectors는 벡터 에셋 관리를 위한 직관적이고 모듈화된 인터페이스를 제공합니다. 단순한 형식 변환부터 세밀한 요소별 편집까지 지원합니다.

## 🚀 주요 기능
- **열기 및 저장**: SVG 및 EPS 형식을 완벽하게 지원합니다.
- **이미지 추적 (Image Trace)**: 비트맵 이미지(PNG, JPG)를 고품질 SVG 벡터 패스로 자동 변환합니다.
- **전문적인 편집 도구**:
  - **그룹화 및 해제**: 복잡한 요소 계층을 손쉽게 관리할 수 있습니다.
  - **실시간 색상 선택**: 요소의 채우기 및 선 색상을 즉시 변경합니다.
  - **스마트 삭제**: 개체 또는 그룹 전체를 즉시 제거할 수 있습니다.
  - **작업 내역 관리**: 무제한 실행 취소/다시 실행 지원 (`Ctrl+Z` / `Ctrl+Shift+Z`).
- **현대적인 인터랙티브 UI**:
  - **고성능 캔버스**: 부드러운 줌 및 이동 기능을 제공합니다.
  - **영역 선택**: 드래그 또는 키보드 조작을 통한 다중 선택 기능을 지원합니다.
  - **컨텍스트 메뉴**: 마우스 우클릭으로 모든 도구에 빠르게 접근 가능합니다.
- **고급 내보내기**: SVG, PDF, EPS 변환 및 개별 요소별 내보내기를 지원합니다.
- **다국어 지원**: 영어 및 한국어를 완벽하게 지원합니다 (시스템 언어 자동 감지).

## 🛠 프로젝트 구조
```text
simplevectors/
├── src/
│   ├── core/          # 비즈니스 로직: SVG 파싱, 이미지 추적
│   ├── ui/            # 그래픽 인터페이스: 캔버스, 메인 윈도우
│   └── assets/        # 리소스: 다국어(i18n), 아이콘
├── .github/           # 자동화: CI/CD 워크플로
├── Dockerfile         # 컨테이너 설정
└── run.sh             # 통합 실행 스크립트
```

## 📦 배포 및 릴리스
- **단일 실행 파일**: **Windows(.exe)**, **Linux**, **macOS**용 실행 파일이 업데이트마다 자동으로 빌드됩니다.
  - 🔗 [최신 버전 다운로드](https://github.com/hslcrb/simplevectors/releases)
- **도커 컨테이너**: GHCR(GitHub Container Registry)을 통해 안정적인 환경을 제공합니다.
  ```bash
  docker pull ghcr.io/hslcrb/simplevectors:latest
  ```
- **자동 버전 관리**: 커밋 10번마다 버전이 자동으로 갱신되는 정책(`v0.0.x`)을 따릅니다.

## 📚 문서 (Documentation)
상세 가이드 및 튜토리얼은 **[프로젝트 위키](https://github.com/hslcrb/simplevectors/wiki)**에서 확인하실 수 있습니다.

## 🏁 시작하기
### 로컬 실행
Python 3.12 버전 이상이 설치된 환경에서 다음을 실행하십시오:
```bash
./run.sh
```

## 제작자 (Author)
Rheehose (Rhee Creative) 2008-2026

## 라이선스 (License)
Apache 2.0 License
