import os
from openai import OpenAI # ChatGPT 라이브러리
from google.cloud import texttospeech # Google TTS 라이브러리
import speech_recognition as sr  # 음성 인식을 위한 라이브러리
import env  # 별도의 API 키가 등록된 파일

# API 키 설정
openai_api_key = os.getenv("OPENAI_API_KEY", env.OPEN_API_KEY)
client = OpenAI(api_key=openai_api_key)

conversation = ""
user_name = "user"
bot_name = "gpt"

tts_client = texttospeech.TextToSpeechClient()

# 음성 인식을 위한 Recognizer 객체 생성
recognizer = sr.Recognizer()
mic = sr.Microphone()

print("라즈베리파이 음성 입력이 활성화되었습니다. 질문을 말씀하세요.")

try:
    # 마이크로부터 음성 입력 받기
    with mic as source:
        print("질문을 말씀하세요...")
        recognizer.adjust_for_ambient_noise(source)  # 주변 소음 조정
        audio = recognizer.listen(source)  # 음성 입력 캡처

    # 음성을 텍스트로 변환
    input_text = recognizer.recognize_google(audio, language="ko-KR")  # 한국어 설정
    print(f"입력된 질문: {input_text}")

    prompt = user_name + ":" + input_text + "\n" + bot_name + ":"
    conversation += prompt

    # OpenAI API 호출
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": conversation}
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # OpenAI 응답에서 텍스트 추출
    response_str = response.choices[0].message.content.strip()
    conversation += response_str + "\n"
    print("- " + response_str)

    # 텍스트를 음성 파일로 변환하여 저장
    synthesis_input = texttospeech.SynthesisInput(text=response_str)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE, name="ko-KR-Wavenet-B"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response_audio = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    output_file = "output.mp3"
    with open(output_file, "wb") as out:
        out.write(response_audio.audio_content)
    print(f"음성 응답이 '{output_file}'에 저장되었습니다.")

    # 저장된 MP3 파일 재생
    print("생성된 응답을 재생합니다...")
    os.system(f"mpg123 {output_file}")

except sr.UnknownValueError:
    print("음성을 인식할 수 없습니다. 다시 시도해 주세요.")
except sr.RequestError as e:
    print(f"음성 인식 서비스에 문제가 발생했습니다: {e}")
