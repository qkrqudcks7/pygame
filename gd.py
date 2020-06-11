import pygame # 파이게임 설정
import sys   # 시스템 부르고
import random # 운석 랜덤으로 떨어지게 설정하기 위해 랜덤 설정
from time import sleep  # 타임 슬립 깔고


화면넓이 = 480
화면높이 = 640
운석=['rock01.png','rock02.png','rock03.png','rock04.png','rock05.png',\
    'rock06.png','rock07.png','rock08.png','rock09.png','rock10.png',\
        'rock11.png','rock12.png','rock13.png','rock14.png','rock15.png',\
            'rock16.png','rock17.png','rock18.png','rock19.png','rock20.png',\
                'rock21.png','rock22.png','rock23.png','rock24.png','rock25.png'\
                    'rock26.png','rock27.png','rock28.png','rock29.png','rock30.png']
음향=['explosion01.wav','explosion02.wav','explosion03.wav','explosion04.wav']
def 맞춘카운트(count):
    global gamepad
    font=pygame.font.Font('NanumGothic.ttf',20)
    text=font.render('파괴한 운석 수:'+str(count),True,(255,255,255)) # 255 3개이거 흰색
    gamepad.blit(text,(10,0))

def 못맞춘카운트(count):
    global gamepad
    font=pygame.font.Font('NanumGothic.ttf',20)
    text=font.render('놓친 운석 수:'+str(count),True,(255,0,0)) # 이건 빨간색
    gamepad.blit(text,(350,0))

def 메세지(text):
    global gamepad,게임오버사운드
    textfont=pygame.font.Font('NanumGothic.ttf',60)
    text=textfont.render(text,True,(255,0,0))
    textposition=text.get_rect() # get.rect가 아니라 get_rect이다 주의
    textposition.center=(화면넓이/2,화면높이/2) # 화면 정중앙에 위치
    gamepad.blit(text,textposition) # 실질적으로 출력하라는 코드
    pygame.display.update() # 화면 업데이트
    pygame.mixer.music.stop()
    게임오버사운드.play()
    sleep(2) # 2초 쉬고
    pygame.mixer.music.play(-1)
    실행() # 다시 게임 시작

def 충돌():
    global gamepad
    메세지('전투기 파괴!')

def 게임오버():
    global gamepad
    메세지('게임 오버!')


def 게임화면(obj,x,y):
    global gamepad
    gamepad.blit(obj,(x,y))

def 게임초기화():
    global gamepad, clock, background,plane,missile,explosion,미사일사운드,게임오버사운드 # 글로벌로 게임패드랑 클락 땡겨온다
    pygame.init() # 파이게임 초기화
    gamepad = pygame.display.set_mode((화면넓이,화면높이))
    pygame.display.set_caption('뵹차니의 슈팅게임')
    clock= pygame.time.Clock()
    background= pygame.image.load('gd.png')              #배경화면 설정
    plane=pygame.image.load('spaceship.png')                   # 비행기 설정
    missile=pygame.image.load('missile.png')          # 미사일 설정
    explosion=pygame.image.load('explosion.png')          # 비행기 폭파되는거 가져옴
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1)
    미사일사운드=pygame.mixer.Sound('missile.wav')
    게임오버사운드=pygame.mixer.Sound('gameover.wav')
def 실행():
    global gamepad, clock, background, plane, missile,explosion, 미사일사운드, 게임오버사운드

    전투기사이즈=plane.get_rect().size
    전투기사이드=전투기사이즈[0]
    전투기높이=전투기사이즈[1]

    x=화면넓이*0.45
    y=화면높이*0.9
    planeX=0

    missileXY=[]  # 미사일 여러개 가져올 위치 설정
    rock=pygame.image.load(random.choice(운석)) # 랜덤하게 떠어지도록
    운석크기= rock.get_rect().size
    운석폭= 운석크기[0]
    운석높이= 운석크기[1]
    운석파괴사운드=pygame.mixer.Sound(random.choice(음향)) # 운석파괴 됐을 때 랜덤으로 소리 재생
    rockX=random.randrange(0,화면넓이-운석폭) # 운석의 위치 랜덤으로
    rockY=0 # 위에서 부터 떨어지니깐 0 꼭대기부터
    운석스피드=2 #운석 떨어지는 스피드

    hit= False
    hitcount=0
    nohit=0


    ongame=False
    while not ongame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()      # QUIT창을 누르면 게임이 종료된다는 이벤트
            if event.type in [pygame.KEYDOWN]:
                if event.key==pygame.K_LEFT:
                    planeX-=5             # 키보드 왼쪽으로 누르면 5씩증가
                elif event.key==pygame.K_RIGHT:
                    planeX+=5              # 키보드 오른쪽으로 누르면 5씩증가
                elif event.key==pygame.K_SPACE:
                    미사일사운드.play()
                    missileX= x+전투기사이드/2 # 전투기 중간에 나가도록
                    missileY= y-전투기높이  # 전투기 높이에서 나가도록
                    missileXY.append([missileX,missileY]) # 여러개 나가도록
            if event.type in [pygame.KEYUP]:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    planeX=0                      # 키보드에서 up 손때면 좌표0 안 움직인다.

        게임화면(background,0,0)           # 배경화면 호출

        x+=planeX       # 위에서 조종키 입력했으니 이젠 전투기가 방향키에 따라 움직이는 값 조정.
        if x <0:
            x=0       # 만약 x좌표 맨 왼쪽 좌표인 0 보다 작아진다 그러면 그것이 0이 되게한다. 즉 화면 밖으로 못 나가게 한다
        elif x> 화면넓이-전투기사이드:
            x= 화면넓이-전투기사이드  # 비행기가 오른쪽으로 끝까지 갔을 때, 전투기가 화면넓이를 넘길려고할 때 그것을 마지막으로 한다. 화면 밖으로 못 나가도록

        if y < rockY+운석높이: # 전투기가 운석이랑 충돌했는지 체크
            if (rockX> x and rockX < x+전투기사이드) or (rockX+운석폭 > x and rockX + 운석폭 < x + 전투기사이드): # 비행기와 운석이 서로 겹치는지 안 겹치는지 확인하는 작업
                충돌() #겹치면 충돌
                   
        게임화면(plane,x,y)                # 비행기 호출  

        if len(missileXY) !=0:
            for i, bxy in enumerate(missileXY): #미사일 요소에 대해 반복
                bxy[1]-=10 # 총알의 y좌표 -10(위로이동)
                missileXY[i][1]=bxy[1] # 여기서 실수했다 missileXY라고 입력 꼭
                
                if bxy[1]<rockY: # 돌에 겹치냐 안 겹치냐
                    if bxy[0]>rockX and bxy[0]<rockX+운석높이: # 미사일이 운석을 맞췄을 때
                        missileXY.remove(bxy)  # 맞으면 기존 미사일 제거
                        hit=True
                        hitcount+=1
                if bxy[1]<=0:
                    try:
                        missileXY.remove(bxy)  # 미사일이 화면 밖으로 나가면 제거
                    except:
                        pass
        if len(missileXY) !=0:
            for bx, by in missileXY:
                게임화면(missile,bx,by)  # 미사일 그리기

        맞춘카운트(hitcount)  # hitcount 설정한것 적용

        rockY+=운석스피드 # 운석이 떨어지는데 스피드 추가
        if rockY>화면높이:
            운석크기= rock.get_rect().size
            운석폭= 운석크기[0]
            운석높이= 운석크기[1]
            rockX=random.randrange(0,화면넓이-운석폭) # 운석의 위치 랜덤으로
            rockY=0       # 운석이 화면 밖으로 나가면 또 생성
            nohit+=1 # 운석 화면 밖으로 나갔을 때 1개씩 추가 놓친거

        if nohit==3:
            게임오버()
        못맞춘카운트(nohit)

        if hit:
            게임화면(explosion,rockX,rockY) # 운석 폭발 그리기
            운석파괴사운드.play()

            운석크기= rock.get_rect().size
            운석폭= 운석크기[0]
            운석높이= 운석크기[1]
            rockX=random.randrange(0,화면넓이-운석폭) # 운석의 위치 랜덤으로
            rockY=0
            운석파괴사운드=pygame.mixer.Sound(random.choice(음향))
            hit= False

            운석스피드+=0.2 # 운석 맞출 때 마다 0.2씩 스피드 증가
            if 운석스피드>=10:
                운석스피드=10  # 스피드 10에 도달했을때 최대치 10으로 설정

        게임화면(rock,rockX,rockY) # 운석 호출
        pygame.display.update() # 디스플레이 다시 한번 호출

        clock.tick(60) # 프레임 초당 60

    pygame.quit()

게임초기화()
실행()
