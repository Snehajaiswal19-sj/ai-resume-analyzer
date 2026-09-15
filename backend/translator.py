from googletrans import Translator
from typing import Dict

class LanguageTranslator:
    """Translate resume analysis to multiple languages"""
    
    def __init__(self):
        self.translator = Translator()
        self.languages = {
            'hi': 'Hindi',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ar': 'Arabic',
            'bn': 'Bengali',
            'ta': 'Tamil',
            'te': 'Telugu',
            'mr': 'Marathi',
            'gu': 'Gujarati'
        }
    
    def translate_text(self, text: str, target_lang: str) -> Dict:
        """Translate text to target language"""
        try:
            if target_lang not in self.languages:
                return {'error': 'Language not supported'}
            
            result = self.translator.translate(text, dest=target_lang)
            
            return {
                'original': text,
                'translated': result.text,
                'language': self.languages[target_lang]
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_supported_languages(self) -> Dict:
        """Get list of supported languages"""
        return self.languages