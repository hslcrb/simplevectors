# SimpleVectors v0.0.0

A powerful and modular vector graphics editor capable of opening, saving, converting, and modifying vector files (SVG, EPS).

[![CI/CD Pipeline](https://github.com/hslcrb/simplevectors/actions/workflows/pipeline.yml/badge.svg)](https://github.com/hslcrb/simplevectors/actions/workflows/pipeline.yml)

## Features
- **Open & Save**: Full support for SVG and EPS formats.
- **Image Tracing**: Convert bitmap images (PNG, JPG) into high-quality SVG vector paths with multiple presets (Default, Detailed, Simplified, Sketch).
- **Advanced Editing**:
  - **Grouping & Ungrouping**: Organize multiple elements into logical groups.
  - **Color Manipulation**: Change fill colors of individual or grouped elements.
  - **Deletion**: Remove unwanted elements or groups.
  - **Undo/Redo**: Robust history management (Ctrl+Z / Ctrl+Shift+Z).
- **Interactive Canvas**:
  - **Multi-selection**: Select multiple elements via area drag or Ctrl-click.
  - **Seamless Navigation**: Smooth zooming (Ctrl+Wheel or Ctrl+/-) and panning (WASD or Arrow keys).
  - **Context Menu**: Right-click for quick access to all editing tools.
- **Conversion**: Export vectors to SVG, PDF, EPS, or individual elements.
- **Internationalization**: Full bilingual support (English & Korean) with automatic system detection.

## CI/CD & Releases
- **Standalone Binaries**: Executables for Linux, Windows, and macOS are automatically built and released on every push. [Download latest releases](https://github.com/hslcrb/simplevectors/releases).
- **Docker Container**: A Dockerized version is available at GitHub Container Registry.
  ```bash
  docker pull ghcr.io/hslcrb/simplevectors:latest
  ```
- **Automated Versioning**: Versions follow `v0.0.x` format, incrementing every 10 commits.

## How to Run
Simply execute the run script in the terminal:
```bash
./run.sh
```

## Author
Rheehose (Rhee Creative) 2008-2026

## License
Apache 2.0 License

---

# SimpleVectors (심플벡터) v0.0.0

SVG, EPS 등 벡터 파일을 열고, 저장하고, 변환하며 정밀하게 편집할 수 있는 강력한 모듈형 벡터 그래픽 편집기입니다.

[![CI/CD Pipeline](https://github.com/hslcrb/simplevectors/actions/workflows/pipeline.yml/badge.svg)](https://github.com/hslcrb/simplevectors/actions/workflows/pipeline.yml)

## 기능 (Features)
- **열기 및 저장**: SVG 및 EPS 형식을 완벽하게 지원합니다.
- **이미지 추적 (Image Trace)**: 비트맵 이미지(PNG, JPG)를 고품질 SVG 벡터 패스로 변환합니다 (프리셋: 기본값, 상세함, 단순함, 스케치).
- **고급 편집 기능**:
  - **그룹화 및 해제**: 여러 요소를 그룹으로 묶거나 개별 요소로 분리합니다.
  - **색상 변경**: 개별 또는 그룹화된 요소의 채우기 색상을 변경합니다.
  - **삭제**: 불필요한 요소나 그룹을 즉시 제거합니다.
  - **되돌리기/다시실행**: 무제한 작업 내역 관리 지원 (Ctrl+Z / Ctrl+Shift+Z).
- **인터랙티브 캔버스**:
  - **다중 선택**: 영역 드래그 또는 Ctrl-클릭을 통한 일괄 선택 기능을 지원합니다.
  - **유연한 탐색**: 부드러운 줌(Ctrl+휠 또는 Ctrl+/-) 및 이동(WASD 또는 방향키) 기능을 제공합니다.
  - **컨텍스트 메뉴**: 마우스 우클릭으로 모든 편집 도구에 빠르게 접근할 수 있습니다.
- **변환 및 내보내기**: SVG, PDF, EPS 변환 및 개별 요소 내보내기를 지원합니다.
- **국제화**: 영어 및 한국어를 완벽하게 지원하며, 시스템 언어를 자동으로 감지합니다.

## CI/CD 및 배포 (Releases)
- **단일 실행 파일**: Linux, Windows, macOS용 실행 파일이 푸시할 때마다 자동으로 빌드되어 릴리스됩니다. [최신 릴리스 다운로드](https://github.com/hslcrb/simplevectors/releases).
- **도커 컨테이너**: GHCR에서 도커 이미지를 제공합니다.
  ```bash
  docker pull ghcr.io/hslcrb/simplevectors:latest
  ```
- **자동 버전 관리**: `v0.0.x` 형식을 따르며, 커밋 10번마다 버전이 자동으로 올라갑니다.

## 실행 방법
터미널에서 다음 스크립트를 실행하십시오:
```bash
./run.sh
```

## 제작자 (Author)
Rheehose (Rhee Creative) 2008-2026

## 라이선스 (License)
Apache 2.0 License
