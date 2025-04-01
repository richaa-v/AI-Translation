from flask import Flask, request, jsonify
from googletrans import Translator
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import tempfile
from pydub import AudioSegment
import speech_recognition as sr

app = Flask(__name__)

SUPPORTED_LANGUAGES = {
    'ig': 'Igbo',
    'ha': 'Hausa',
    'yo': 'Yoruba',
    'sw': 'Swahili',
    'ar': 'Arabic',
    'fr': 'French',
    'zu': 'Zulu',
    'am': 'Amharic',
    'so': 'Somali',
    'pt': 'Portuguese',
    'es': 'Spanish',
    'en': 'English'
}

def extract_audio(video_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    audio.write_audiofile(temp_audio.name)
    return temp_audio.name

def speech_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except Exception as e:
        return str(e)

def translate_text(text, target_lang):
    translator = Translator()
    translation = translator.translate(text, dest=target_lang)
    return translation.text

@app.route('/translate', methods=['POST'])
def translate_video():
    if 'video' not in request.files or 'target_language' not in request.form:
        return jsonify({'error': 'Missing video file or target language'}), 400
    
    video_file = request.files['video']
    target_lang = request.form['target_language']
    
    
    # Save uploaded video temporarily
    temp_video = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    video_file.save(temp_video.name)
    
    try:
        # Extract audio from video
        audio_path = extract_audio(temp_video.name)
        
        # Convert speech to text
        original_text = speech_to_text(audio_path)
        
        # Translate text
        translated_text = translate_text(original_text, target_lang)
        
        # Here you would implement lip sync and audio generation
        # This is a placeholder for where you'd add those implementations
        
        return jsonify({
            'original_text': original_text,
            'translated_text': translated_text,
            'target_language': target_lang
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up temporary files
        os.unlink(temp_video.name)
        os.unlink(audio_path)

if __name__ == '__main__':
    app.run(debug=True)