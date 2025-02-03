import requests
import environ

env = environ.Env()
environ.Env.read_env()

def get_naver_token(code):
  url = 'https://nid.naver.com/oauth2.0/token'

  data = {
    'grant_type': 'authorization_code',
    'client_id': env('NAVER_CLIENT_ID'),
    'client_secret': env('NAVER_SECRET'),
    'code': code,
  }

  response = requests.post(url, data=data)

  if response.status_code == 200:
    token_info = response.json()
    return token_info.get('access_token')
  else:
    raise Exception(f"네이버 로그인 오류: {response.status_code} - {response.text}")

def get_naver_user_info(access_token):
  url = 'https://openapi.naver.com/v1/nid/me'

  headers = {
    'Authorization': f'Bearer {access_token}',
  }

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    user_info = response.json()
    return user_info
  else:
    raise Exception(f"네이버 사용자 정보 조회 오류: {response.status_code} - {response.text}")

def get_kakao_token(code):
  url = 'https://kauth.kakao.com/oauth/token'

  # 요청에 필요한 파라미터 설정
  data = {
    'grant_type': 'authorization_code',
    'client_id': env('KAKAO_CLIENT_ID'),
    'client_secret': env('KAKAO_SECRET'),
    'redirect_uri': env('KAKAO_REDIRECT_URI'),
    'code': code,
  }

  # 카카오 API에 POST 요청
  response = requests.post(url, data=data)

  # 응답 결과 처리
  if response.status_code == 200:
    token_info = response.json() # 엑세스 토큰 정보를 JSON으로 변환
    access_token = token_info.get('access_token') # 엑세스 토큰 추출
    refresh_token = token_info.get('refresh_token') # 리프레시 토큰 추출
    return access_token, refresh_token
  else:
    # 오류 처리
    raise Exception(f"카카오 로그인 오류: {response.status_code} - {response.text}")

def get_kakao_user_info(access_token):
  url = 'https://kapi.kakao.com/v2/user/me'
  
  headers = {
    'Authorization': f'Bearer {access_token}',
  }

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    user_info = response.json()
    return user_info
  else:
    raise Exception(f"카카오 사용자 정보 조회 오류: {response.status_code} - {response.text}")