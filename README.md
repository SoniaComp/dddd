# API INTERFACE
* [GET] /api/tag/ : 태그 추천
    - input: {text: text}
    - output: {documentclassification 알고리즘 결과 dict}

* [POST] /api/question/ : 질문 등록 및 유사 사례 추천 (질문 등록과 동시에 서버에서 AI 돌림)
    - input: {title: text, description: text, tags: charArray, *phonenumber: char(11)}
    - output: {id: Question.id(생성된 Question 객체 아이디)}

* [GET] /api/question/ : 유사 사례 추천 결과값 가져오기
    - input: {id: int}
    - output: {'question': {
            'id': question.id,
            'title': question.title,
            'content': question.description,
        }, 'answers': answers.answer, 'code': code
        }

* [GET] /api/event/ : 핸드폰 번호 입력한 AI 응답 보기
    - input: {code: char(20)}
    - output: status.HTTP_200_OK

* [POST] /api/event/comp/ : 기업 사전 예약 페이지
    - input: {name: char(30)(기업명), manager: char(30)(담당자), comp_number: char(15)(사업등록번호), email: char(100)(이메일)}
    - output: status.HTTP_200_OK

* [GET] /api/panrye/
    - input: {'code':char(20)} 코드 내용 입력해서, 관련 내용 있을 경우 바로 보내주고, 없을 경우 찾아서 저장
    - output: {'results': char(판례내용)}
    - error: 판례가 없는 경우 status.HTTP_404_NOT_FOUND

* [POST] /api/ai/ : ai 응답 만족도 조사
    - input: {id: int(Question.id), answer: text(ai응답_응답), title: text(ai응답_질문제목), content: text(ai응답_질문내용), satisfaction: bool}
    전체에 대한 만족도 일경우, answer에 '' 들어가고, 아닐 경우, 특정 값이 answer, title, content에 들어감
    - output: status.HTTP_200_OK


# 1. How To Start
```shell
# 가상환경 설정 - virtualenv
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
# 프로젝트 시작
$ python3 manage.py runserver
```

# 2. How To Deploy
### USE gunicorn
[gunicorn 설정 방법](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04#create-a-gunicorn-systemd-service-file)

```bash
gunicorn barlaw.wsgi:application --bind 0:10301

uwsgi --http :8000 --module barlaw.wsgi --virtualenv /path/to/virtualenv

sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl status gunicorn.service

journalctl --unit=gunicorn | tail -n 300 # gunicorn 관련 로그
```

# 3. How To Use ADMIN
* core > admin 에서 admin.site.register(모델 이름) 설정

* 장고 서버 도메인/admin에서 확인

# 4. Folder Structure
## AI
1. 유사사례 검색
* api.berts 에 USE_BERT.zip에 있던 파일들 존재
* settings.py에 model, device, tokenizer를 전역변수로 설정

2. 태그
* api.documentation 에 파일 존재

## api 폴더
views.py에 모든 API 관련 존재(알리고 문자발송 관련 API 포함)

## barlaw 폴더
* 장고 정값 포함
* settings.py에 메일발송, 데이터베이스 연결 정보 등 모든 정보 존재

## core 폴더
models.py에 모든 모델 존재

# 5. Cloud 관련
## **was-server**

* pw: p4WQyO8ng2Vv

1. python3, pip 설치

2. Django 설치
**[How To Use PostgreSQL with your Django Application on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)**

## database

* pw: 3yuF4Yrywtxe

VM 에 직접 MySQL 설치([MySQL documentation](https://dev.mysql.com/doc/))


1. [MySQL 설치](https://jetalog.net/82) 방법

    ```bash
    $ sudo apt-get install mysql-server
    $ sudo ufw allow mysql # mysql port 3306 열어주기
    $ sudo systemctl start mysql
    $ bsudo systemctl enable mysql # 서버 재시작되더라도 mysql 자동 시작 등록
    $ sudo /usr/bin/mysql -u root -p # mysql에 접속하기
    비밀번호: 
    ```

2. MySQL 정보

* **database: barlaw**

*  **user**: dev / **pw**: barlaw!

    ```sql
    $ CREATE DATABASE barlaw;
    $ USE barlaw;
    ```

    **사용자**

    dev@localhost (lawtheBar12!)

    dev@'%' (lawtheBar12!)

    ```sql
    mysql> create user 'test'@'localhost' identified by 'test1234';
    Query OK, 0 rows affected (0.00 sec)
     
    mysql> grant all privileges on test_database.* to test@'localhost';
    Query OK, 0 rows affected (0.00 sec)

    mysql> flush privileges;

    mysql> show grants for dev@'localhost'; # 권한 부여 확인
    ```

    **외부 접속 허용**

    참고: [https://jetalog.net/82](https://jetalog.net/82)

    devremote lawtheBar12!

    ```bash
    $ mysql_secure_installation # 보안관련 설정 / 비밀번호: barlaw
    $ sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
    # bind address 변경
    $ sudo service mysql restart # 재실행
    $ sudo mysql -u root [-h 아이피주소] -p
    Enter password: (비밀번호 입력. 입력한 값은 표시되지 않음.)
    ```

    **한글 설정: 14.63.174.14**

    [https://jyspw.tistory.com/24](https://jyspw.tistory.com/24)

    ```jsx
    ALTER DATABASE [DB명] CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
    ```

