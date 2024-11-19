import os
import adafruit_dht
import board
import time
import requests
import env

# DHT22 온습도센서 연결
mydht22 = adafruit_dht.DHT22(board.D4)

# HTTP 요청 URL
url = os.getenv("HTTP_REQ", env.HTTP_REQ)+"/plant/censor/update"

while True:
    try:
        # 온습도센서로 값 받아오기
        humidity_data = mydht22.humidity # 습도 값
        temperature_data = mydht22.temperature # 온도 값

        # 테스트를 위한 임시 토양 습도 데이터
        soil_moisture = 1.000

        # POST Request Body 양식
        data = {
            "potId": 1,
            "plantSoilMoisture": soil_moisture,
            "plantTemperature": temperature_data
        }

        # 서버에 POST 요청 보내기
        response = requests.post(url, json=data)

        # 응답 확인
        if response.status_code == 200:
            try:
                response_data = response.json()
                print("데이터 전송 성공:", data)
                print("서버 응답:", response_data)
            except ValueError:
                print("서버로부터 응답을 받지 못했습니다.")
                print("응답 내용:", response.text)
        else:
            print("데이터 전송 실패:", response.status_code, response.text)

        time.sleep(2)

    except RuntimeError as error:
        # 온습도센서 오류 처리
        print("센서 오류:", error.args[0])
        time.sleep(2)
    except requests.exceptions.RequestException as e:
        # HTTP 요청 오류 처리
        print("HTTP 요청 오류:", e)
        time.sleep(2)
    finally:
        pass