<!--
프로젝트 개요(기획 배경, 목적 등)
팀원 소개(FE, BE) + 팀원 깃허브 링크 연결
ERD
html 플로우 차트(주요 기능 설명하면서)
+ 사용법?
사용 예시(웹사이트 캡처 화면 포함)
사용 도구(언어, 협업 툴 - 링크 포함)
-->


# 📝 On-Record(온기록)
### 🍀 피로그래밍 22기 최종 프로젝트
📆 **개발 기간**: 2025년 01월 27일 ~ 2025년 02월 18일
### 📂 Contents
1. [🔗 배포 URL](#-배포-URL)
2. [☀️ 서비스 소개](#-서비스-소개)
3. [🐶 팀원 소개](#-팀원-소개)
4. [💻 사용 툴](#-사용-툴)
5. [📈 Flowchart](#-Flowchart)
6. [🧱 System Architecture](#-System-Architecture)
7. [📀 ERD](#-ERD)


## ☀️ 서비스 소개
![온기록 로고](static/images/readme/onrecord_logo(readme).png)
> #### URL: ["온기록 사이트"](onrecord.kr, "온기록 이용해보기")
> 반려동물이나 반려식물과의 추억을 기록하면, **AI**가 반려친구의 입장에서 답장을 생성해주는 웹서비스


온기록(온기 + 기록)은 반려동물 또는 반려식물을 키우는 사용자들이 자신의 반려친구와의 소중한 일상을 기록할 수 있도록 돕는 웹 서비스입니다.
반려동물뿐만 아니라 반려식물도 포함하여 보다 폭넓은 사용자층을 대상으로 하며, 감정과 날씨 등의 요소를 활용해 일상을 더욱 생동감 있게 기록할 수 있도록 설계되었습니다.


## 💻 사용 툴(Tools)

******

#### Front-End
<p>
    <img src="https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white"/>
    <img src="https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
    <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/>
</p>


******


#### Back-End
<p>
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green">
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white">
    <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white">
    <img src="/static/images/readme/gunicorn.png">
    <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white">
    <img src="/static/images/readme/navercloud.png">
</p>


******


#### AI
<p>
    <img src="https://img.shields.io/badge/ChatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white">
</p>


******


### 🌟 협업 툴
<p>
    <img src="https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white">
    <img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white">
    <img src="https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white">
</p>

******

## 📈 Flowchart
![온기록 플로우차트](static/images/readme/onrecord_flowchart.png)

## 🧱 System Architecture
![온기록 시스템아키텍쳐](static/images/readme/onrecord_systemarchitecture.png)

## 📀 ERD
![온기록 ERD](static/images/readme/onrecord_erd.png)

## 핵심 기능
1.	캘린더 기반 일기 작성
	•	반려동물 및 반려식물을 대상으로 날짜별 일기 작성
	•	감정(이모지) 및 날씨 선택 기능
	•	다이어리 리스트 및 개별 일기 상세 보기 가능
2.	AI 답변 생성 기능
	•	사용자가 작성한 일기에 대해 AI가 반려친구(동물/식물)의 입장에서 답장을 생성
	•	AI 응답을 통해 사용자와 반려친구 간의 인터랙션을 강화
3.	반려친구 관리 기능
	•	반려동물 및 반려식물 등록 및 삭제 기능
	•	반려친구의 사진, 이름, 성격 등을 추가하여 맞춤형 관리 가능
4.	공개/비공개 설정
	•	일기별로 전체 공개/비공개 설정이 가능하여 프라이버시 보호
	•	향후 커뮤니티 기능과 연계 가능

## 사용 예시
1.	회원가입 및 로그인
	•	회원가입 후, 로그인하여 반려친구를 등록할 수 있는 초기 설정 페이지로 이동
    <img src="/static/images/readme/first_page.png">
2.	반려친구 등록
	•	반려동물 또는 반려식물 추가
    <img src="/static/images/readme/create_pet_or_plant.png">
	•	사진 업로드, 성격 설정 등의 기능을 통해 개별 맞춤 설정
    <p>
        <img src="/static/images/readme/create_pet.png">
        <img src="/static/images/readme/create_plant.png">
    </p>
3.	캘린더 화면에서 일기 작성
	•	원하는 날짜를 선택 후, 반려친구를 지정하여 일기 작성
    <img src="/static/images/readme/view_calendar.png">
4.  일기 작성
    •	감정 및 날씨 선택, 텍스트 입력 기능 제공
    <img src="/static/images/readme/create_diaries.png">
5.	AI 답변 확인
	•	작성한 일기에 대해 AI가 반려친구의 입장에서 답장을 자동 생성
	•	감정 분석을 기반으로 자연스러운 반응 제공
    <img src="/static/images/readme/detail_diaries.png">
6.	일기 리스트 및 상세보기
	•	기록된 일기를 캘린더 혹은 리스트 뷰에서 확인
	•	특정 일기 클릭 시, 상세 페이지로 이동하여 전체 내용 및 AI 답장 확인 가능
    <img src="/static/images/readme/onrecord_list.png">
7.	반려친구 관리 및 삭제 기능(마이페이지)
	•	반려친구 추가/수정/삭제 가능
	•	기존에 작성된 일기들은 유지되며, 반려친구 데이터만 삭제
    <img src="/static/images/readme/mypage.png">
8. 커뮤니티 기능(모두의 온기록)
    <img src="/static/images/readme/community.png">

## 🐶 팀원 소개
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[0HooHI](https://github.com/0HooHI "김영호 Github")
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[mangoooooo1](https://github.com/mangoooooo1 "박혜린 Github")
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[l-wanderer01](https://github.com/l-wanderer01 "장재훈 Github")
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[cestjeudi](https://github.com/cestjeudi "조주영 Github")
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Dosp74](https://github.com/Dosp74 "한종서 Github")

![온기록 팀 소개](static/images/readme/onrecord_team.png)
<!-- 
<details><summary>접고 펴는 기능
</summary>

*Write here!*
</details> -->