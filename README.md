# ossp01
# 조선대학교 IT융합대학 컴퓨터공학과 20203181 차승환
. 주제 : 손글씨 인식 프로그램

 * 1/6 : 오픈소스 찾기

 * 1/7 : 오픈소스 소스 분석 및 주석

 * 1/8 : 오픈소스 소스 분석 및 주석

 * 1/9 : 오픈소스 개인 환경에서 실행

 * 1/10 : 손글씨 데이터의 train, test set의 생성 방법에 대한 고민. 기존처럼 음절 및 단어 데이터에 폰트를 씌워 이미지파일을 생성하고 학습하는 것으로 결정함.

 * 1/11 ~ 12 : 학습 속도의 향상을 위해 tensorflow-gpu를 사용하려고 하였으나 계속된 tensorflow import 에러로 cpu사용 결정.

 * 1/13 : tensorflow-gpu 사용을 시도하다가 결국 성공함.
          tensorflow-gpu==1.13.1 버전을 사용하기 때문에 이에 맞는 python3.7버전과, cuda, cudnn버전을 설치.
          
     python에서 json열기 
          import json 
          file = json.load(open('D:\\seonghwan\\3_2winter\\053.대용량 손글씨 OCR 데이터\\01.데이터\\1.Training\\라벨링데이터\\라벨\\HW-OCR\\4.Validation\\P.Paper\\O.Form\\IMG_OCR_53_4PO_09451.json', 'rt', encoding='UTF8')) 
          file.keys() 
          file['Annotation'] 
          type(file['Images']) 
          etc.. 
