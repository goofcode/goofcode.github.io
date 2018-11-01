---
title: Visual Studio, DirectX LNK 2019, LNK 2001 에러
slug: vs-directx-lnk-error
thumbnail: assets/img/Visual%20Studio,%20DirectX%20LNK%202019,%20LNK%202001%20%E1%84%8B%E1%85%A6%E1%84%85%E1%85%A5/ECEA93A0-EE05-487D-B217-29444CB8CA00.png
tags: [블로그,CS,bugfix]
---
 

외부 라이브러리를 사용하여 프로젝트를 진행하면 심심치 않게 볼 수 있는 에러가 바로 LNK 2019, LNK 2001 에러입니다.

![](/assets/img/Visual%20Studio,%20DirectX%20LNK%202019,%20LNK%202001%20%E1%84%8B%E1%85%A6%E1%84%85%E1%85%A5/9C1C6D63-DF12-46D4-8939-CAA7D0888BF1.png)

![](/assets/img/Visual%20Studio,%20DirectX%20LNK%202019,%20LNK%202001%20%E1%84%8B%E1%85%A6%E1%84%85%E1%85%A5/27B8E4FD-14B0-4051-AF95-B2F60B72609A.png)

이러한 에러는 코드에서 참조된 외부 심볼을 visual studio가 찾을 수 없는 경우에 발생하게 됩니다. DirectX를 사용할 때는 크게 두 가지의 원인이 있습니다. 

## Visual Studio에서 디렉토리 또는 라이브러리를 추가하지 않았거나, 플랫폼에 맞지 않게 설정
외부 라이브러리를 사용할 때에는 Visual Studio가 어디서 코드를 찾아봐야 하는지 명시적으로 알려줄 필요가 있습니다. 솔루션 탐색기 내의 프로젝트에서 오른쪽 클릭 -> 속성 또는 Alt + Enter를 눌러 속성창을 열어봅시다.

![](/assets/img/Visual%20Studio,%20DirectX%20LNK%202019,%20LNK%202001%20%E1%84%8B%E1%85%A6%E1%84%85%E1%85%A5/F458A465-B404-49E0-852D-30533654D2D8.png)

속성 -> 구성 속성 -> VC++ 디렉터리로 이동하면 VC++가 검색할 디렉토리를 지정할 수 있습니다. 여기서 DirectX가 설치된 디렉토리를 추가해줘야 합니다. 

![](/assets/img/Visual%20Studio,%20DirectX%20LNK%202019,%20LNK%202001%20%E1%84%8B%E1%85%A6%E1%84%85%E1%85%A5/ECEA93A0-EE05-487D-B217-29444CB8CA00.png)

다음과 같이 오른쪽 끝 화살표를 누르면 편집을 할 수 있는데, 

![](/assets/img/Visual%20Studio,%20DirectX%20LNK%202019,%20LNK%202001%20%E1%84%8B%E1%85%A6%E1%84%85%E1%85%A5/23F04D79-8F5E-43E8-BC63-69CFCB26A847.png)

포함 디렉터리에는 DirectX의 include 폴더를, 

![](/assets/img/Visual%20Studio,%20DirectX%20LNK%202019,%20LNK%202001%20%E1%84%8B%E1%85%A6%E1%84%85%E1%85%A5/5998FA40-2B0F-4210-92D1-C449EA7CB4C2.png)

라이브러리 디렉터리에는 자신이 **빌드하려는 플랫폼에 맞게** DirectX의 Lib에 x86 또는 x64 폴더를 추가해주면 됩니다. 

![](/assets/img/Visual%20Studio,%20DirectX%20LNK%202019,%20LNK%202001%20%E1%84%8B%E1%85%A6%E1%84%85%E1%85%A5/D9B75221-1DCA-4874-80A2-CFB750031CA5.png)

그러면 이제 VC++는 해당 디렉토리에서 파일을 찾을 수 있게 됩니다. 이제 링커에게 필요한 라이브러리 파일을 추가해 줍시다. 저의 경우 `d3d9.lib`와 `d3dx9.lib`, `winmm.lib`내의 함수를 사용하고 있기 때문에 다음과 같이 종속성을 입력시켰습니다.

![](/assets/img/Visual%20Studio,%20DirectX%20LNK%202019,%20LNK%202001%20%E1%84%8B%E1%85%A6%E1%84%85%E1%85%A5/3B1AE98E-1A78-49E2-BBA4-AFC8B1219539.png)


## DirectX가 잘못 설치 됨
DirectX를 설치하면서 다음과 같은 에러를 만났다면, 관련 파일은 존재할 수 있지만 DirectX가 제대로 설치된 것이 아닙니다. 

![](/assets/img/Visual%20Studio,%20DirectX%20LNK%202019,%20LNK%202001%20%E1%84%8B%E1%85%A6%E1%84%85%E1%85%A5/80F3E05B-B4BD-4B9E-AFBB-621FE2343573.png)

이 에러는 보통 DirectX가 설치하려는 VC++보다 높은 버전의 VC++이 설치되어 있을 때 충돌이 일어나기 때문에 발생합니다. 따라서 DirectX를 설치하기 전에 다음 두 프로그램을 제거하면 됩니다.

![](/assets/img/Visual%20Studio,%20DirectX%20LNK%202019,%20LNK%202001%20%E1%84%8B%E1%85%A6%E1%84%85%E1%85%A5/E1452E8C-B2A1-4C14-9911-E0DC86A66B9A.png)

프로그램 추가/제거에서 프로그램 제거를 진행해도 되고, 혹은 cmd 명령어로 간단하게 제거할 수도 있습니다.

```
MsiExec.exe /passive /X{F0C3E5D1-1ADE-321E-8167-68EF0DE699A5}
MsiExec.exe /passive /X{1D8E6291-B0D5-35EC-8441-6616F567A0F7}
```

이후 DirectX를 다시 설치하면 정상적으로 설치가 되고, 링크 에러 또한 사라집니다.