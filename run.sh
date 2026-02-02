#!/bin/bash

# 프로젝트 디렉토리 설정
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
REQUIREMENTS="$PROJECT_DIR/requirements.txt"

# 가상환경 확인 및 자동 생성
if [ ! -d "$VENV_DIR" ]; then
    echo "⚡ 가상환경이 없습니다. 새로 생성합니다... (Virtual environment not found. Creating...)"
    python3 -m venv "$VENV_DIR"
    
    if [ $? -ne 0 ]; then
        echo "❌ 가상환경 생성 실패 (Failed to create venv)."
        exit 1
    fi
    
    echo "📦 생성 완료. 의존성 패키지를 설치합니다... (Installing dependencies...)"
    source "$VENV_DIR/bin/activate"
    
    if [ -f "$REQUIREMENTS" ]; then
        pip install --upgrade pip
        pip install -r "$REQUIREMENTS"
    else
        echo "⚠️ requirements.txt 파일이 없습니다. (requirements.txt missing)"
    fi
else
    echo "✅ 가상환경이 확인되었습니다. (Virtual environment found.)"
    source "$VENV_DIR/bin/activate"
fi

# PYTHONPATH 설정: 프로젝트 루트를 경로에 추가하여 'src' 패키지를 인식하게 함
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

# 실행: 모듈 모드로 실행하여 상대 경로 import 문제 해결
echo "🚀 SimpleVectors 실행 중... (Launching SimpleVectors...)"
python3 -m src.main
