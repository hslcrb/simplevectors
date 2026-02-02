import locale

TRANSLATIONS = {
    "en": {
        "app_title": "SimpleVectors",
        "file": "File",
        "open": "Open",
        "save": "Save",
        "save_as": "Save As",
        "convert": "Convert",
        "export_selected": "Export Selected",
        "edit": "Edit",
        "group": "Group",
        "ungroup": "Ungroup",
        "change_color": "Change Color",
        "view": "View",
        "language": "Language",
        "toggle_language": "Switch to Korean",
        "ready": "Ready",
        "error": "Error",
        "success": "Success",
        "file_opened": "File opened: {}",
        "file_saved": "File saved: {}",
        "conversion_complete": "Conversion complete.",
        "color_changed": "Color changed.",
        "grouped": "Elements grouped.",
        "ungrouped": "Elements ungrouped.",
        "no_selection": "No element selected.",
        "about": "About",
        "about_text": "SimpleVectors\nRheehose (Rhee Creative) 2008-2026\nLicense: Apache 2.0",
        "confirm_exit": "Are you sure you want to exit?",
        "warning": "Warning",
    },
    "ko": {
        "app_title": "SimpleVectors",
        "file": "파일",
        "open": "열기",
        "save": "저장",
        "save_as": "다른 이름으로 저장",
        "convert": "변환",
        "export_selected": "선택 항목 내보내기",
        "edit": "편집",
        "group": "그룹화",
        "ungroup": "그룹 해제",
        "change_color": "색상 변경",
        "view": "보기",
        "language": "언어",
        "toggle_language": "Switch to English",
        "ready": "준비",
        "error": "오류",
        "success": "성공",
        "file_opened": "파일 열림: {}",
        "file_saved": "파일 저장됨: {}",
        "conversion_complete": "변환 완료.",
        "color_changed": "색상 변경됨.",
        "grouped": "요소 그룹화됨.",
        "ungrouped": "그룹 해제됨.",
        "no_selection": "선택된 요소 없음.",
        "about": "정보",
        "about_text": "SimpleVectors\nRheehose (Rhee Creative) 2008-2026\n라이선스: Apache 2.0",
        "confirm_exit": "종료하시겠습니까?",
        "warning": "경고",
    }
}

class I18n:
    def __init__(self):
        self.current_lang = "en"
        self.set_system_default()

    def set_system_default(self):
        try:
            sys_lang = locale.getdefaultlocale()[0]
            if not sys_lang:
                import os
                sys_lang = os.environ.get('LANG', 'en')
            
            print(f"Detected System Language: {sys_lang}")
            
            if sys_lang and sys_lang.startswith("ko"):
                self.current_lang = "ko"
            else:
                self.current_lang = "en"
        except Exception as e:
            print(f"Locale detection error: {e}")
            self.current_lang = "en"

    def set_language(self, lang):
        if lang in TRANSLATIONS:
            self.current_lang = lang

    def toggle_language(self):
        self.current_lang = "ko" if self.current_lang == "en" else "en"

    def get(self, key):
        return TRANSLATIONS.get(self.current_lang, {}).get(key, key)

i18n = I18n()
