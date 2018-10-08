---
title: OpenVPN을 통한 가상 사설망(VPN) 구축
tags: [블로그, CS]
---

## 1. 서론 
최근 학교를 떠나 한 학기 동안 타지에서 생활하게 되었습니다. 논문을 봐야할 경우가 생길 것 같아, 학교에서 제공하는 논문 서비스를 학교 밖에서 이용하는 방법은 없을까 생각해 보았습니다. 저희 학교에서는 내부망에서 ieee 학회 등의 논문 서비스에 접속하는 경우, 다음과 같은 institutional login을 통해서 논문을 다운받을 수 있는 서비스를 제공하고 있었습니다. 첫번째 스크린샷은 일반 외부 네트워크에서 연결한 경우, 두번째는 학교 내부(학교 wifi) 네트워크에서 연결한 경우입니다. 

![](/assets/img/OpenVPN%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%90%E1%85%A9%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB%20%E1%84%80%E1%85%A1%E1%84%89%E1%85%A1%E1%86%BC%20%E1%84%89%E1%85%A1%E1%84%89%E1%85%A5%E1%86%AF%E1%84%86%E1%85%A1%E1%86%BC(VPN)%20%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8/99520D3D5B91D7EE27.jpg)

![](/assets/img/OpenVPN%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%90%E1%85%A9%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB%20%E1%84%80%E1%85%A1%E1%84%89%E1%85%A1%E1%86%BC%20%E1%84%89%E1%85%A1%E1%84%89%E1%85%A5%E1%86%AF%E1%84%86%E1%85%A1%E1%86%BC(VPN)%20%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8/991BA7365B943B4835.jpg)
  
간단하게는, 학교 내부망으로 접속하여 (편의성을 위해서 그래픽 환경을 사용할 수 있는 vnc로 접속) 거기서부터 논문을 다운받고, 이를 제 노트북으로 보내면 되는 것이었습니다. 하지만, 대부분의 학교가 그렇겠지만, 포트가 막혀있었고, 학생 개인 신분으로 직접 포트를 열 수 있는 방법이 없었습니다. 그래서 생각해 낸 것이 VPN을 사용하는 것이었습니다.

VPN에 대한 자세한 내용들은 [여기](https://ko.wikipedia.org/wiki/%EA%B0%80%EC%83%81%EC%82%AC%EC%84%A4%EB%A7%9D)서 확인하시면 될 것 같습니다. 추가로, 이 구조를 사용하여 집에 연결해 놓은 PC 또는 라스베리파이에 vpn을 통해 간단하게 접속하는 것도 시도해 볼 수 있겠습니다.

## 2. VPN 구축
우선 VPN을 구축하기 위해서는 공인 IP를 사용하는 OpenVPN 서버가 필요합니다. 저는 Elastic IP가 적용된 EC2 인스턴스를 OpenVPN 서버로, 학교 내의 ubuntu 16.04 서버와 개인용 맥북을 클라이언트로 하여 네트워크를 구성하였습니다. 전체 구성은 다음과 같은 그림이 되겠네요.

![](/assets/img/OpenVPN%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%90%E1%85%A9%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB%20%E1%84%80%E1%85%A1%E1%84%89%E1%85%A1%E1%86%BC%20%E1%84%89%E1%85%A1%E1%84%89%E1%85%A5%E1%86%AF%E1%84%86%E1%85%A1%E1%86%BC(VPN)%20%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8/%E1%84%80%E1%85%B3%E1%84%85%E1%85%B5%E1%86%B71.png)

### 2.1. OpenVPN 서버 환경 세팅
우선, OpenVPN 서버로 정한 기기(저의 경우 EC2 인스턴스)에 접속하여 OpenVPN과 easy-rsa를 설치해줍니다.
```bash
$ sudo apt-get update
$ sudo apt-get install openvpn easy-rsa
```
그 다음으로 CA(certificate authority) 설정을 위해 CA 디렉토리를 만들어주고 해당 디렉토리로 이동합니다.
```bash
$ make-cadir ~/openvpn-ca
$ cd ~/openvpn-ca
```
이제 CA variable을 설정하기 위해 vars를 에디터로 열어 다음 몇 가지 변수를 찾아 원하는대로 수정해줍니다. 하지만 공란으로 남겨둬서는 안됩니다. 또한 KEY_NAME 변수는 편의성을 위해서 server로 바꾸었습니다.
```bash
# ~/openvpn-ca/vars
...
export KEY_COUNTRY="KR"
export KEY_PROVINCE="Seoul"
export KEY_CITY="Seoul"
export KEY_ORG="Goofcode"
export KEY_EMAIL="goofcode@gmail.com"
export KEY_OU="OrganizationUnit"
...
export KEY_NAME="server"
...
```
이제, easy-rsa를 사용하여 CA를 빌드하면 됩니다. 
```bash
$ cd ~/openvpn-ca
$ source vars
$ ./clean-all
$ ./build-ca
```
빌드 과정에서 몇가지 설정을 어떻게 할것인지 물어보는데, 저희는 앞서 vars를 수정해 놓았기 때문에 기본값이 이미 설정되어 있습니다. 따라서 빌드가 완료될 때까지 Enter를 눌러 기본값을 적용시키면 됩니다.
이제 서버의 certificate과 key, encryption 파일을 생성합니다. 여기서 입력으로 주어지는 server라는 이름은 편의상 사용한 것이고, 임의로 바꾸어도 됩니다. 하지만 이 이름을 변경할 경우, 이후 명령에서도 사용했던 이름을 계속 사용해야 합니다.
```bash
$ ./build-key-server server
```
아까와 비슷하게 Enter를 눌러 미리 설정된 기본값을 설정하면 되고, 추가적으로 마지막 두 질문에 y를 입력하여 key를 빌드하면 됩니다.
```
. . .
Certificate is to be certified until May  1 17:51:16 2026 GMT (3650 days)
Sign the certificate? [y/n]: y

1 out of 1 certificate requests certified, commit? [y/n] y
Write out database with 1 new entries
Data Base Updated
```
이제 키 교환에 사용되는 Diffe-Hellman 키와 HMAC 시그니처를 생성합니다. 첫번째는 몇 분가량의 시간이 소요될 수 있습니다.
```bash
$ ./build-dh
$ openvpn --genkey --secret keys/ta.key
```
이제 만들어진 credential을 통해서 OpenVPN 설정을 해보겠습니다. 만들었던 crendential을 openvpn 디렉토리로 옮기고, 샘플 설정도 가져옵니다.
```bash
$ cd ~/openvpn-ca/keys
$ sudo cp ca.crt server.crt server.key ta.key dh2048.pem /etc/openvpn
$ gunzip -c /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz | sudo tee /etc/openvpn/server.conf
```
이제 샘플 설정을 조금 수정해 봅시다. 복사한 샘플 설정에서 다음 부분을 찾아 원하는대로 수정해줍니다.
```bash
# /etc/openvpn/server.conf

tls-auth ta.key 0          	# 앞에 있던 ;(주석처리)를 없앱니다.
key-direction 0            	# 밑에 이 부분을 새로 추가합니다.

cipher AES-128-CBC      		# 앞에 있던 ;를 없앱니다. 암호화 방식 중 AES-128-CBC를 사용합니다.
auth SHA256             		# 밑에 이 부분을 새로 추가합니다.

user nobody                	# 앞에 있던 ;를 없앱니다.
group nobody               	# 앞에 있던 ;를 없앱니다.

client-to-client            # 앞에 있던 ;를 없앱니다. 이 설정을 해주어야 OpenVPN의 client 끼리의 통신이 가능해집니다.

# 여기부터는 옵션입니다.
# 만약 vpn이 활성화되었을 때, 모든 트래픽을 vpn을 사용하여 보내려면,

# 다음 부분에서 앞에 있던 ;를 없앱니다.
push "redirect-gateway def1 bypass-dhcp"    
push "dhcp-option DNS 208.67.222.222"
push "dhcp-option DNS 208.67.220.220"

# OpenVPN에서 사용하는 포트와 프로토콜을 변경하려면 (기본 1194/UDP)
# 예를 들어 1234번과 TCP를 사용하려면 다음과 같이 설정을 변경합니다.
port 1234        
proto tcp

# 혹시 $ ./build-key-server server 명령에서 server가 아닌 다른 이름을 사용했다면,
# 다음 설정을 이름에 맞게 변경하시면 됩니다.
cert server.crt
key server.key
```
그러면 이제 OpenVPN 서버로 동작할 수 있도록, 네트워크 설정을 해줍니다.
ip forwarding 기능을 활성화하고, 설정을 적용시킵니다.
```bash
# /etc/sysctl.conf
net.ipv4.ip_forward=1
```
```bash
$ sudo sysctl -p
```

다음 명령어로 기본 네트워크 인터페이스를 확인한 뒤, _etc_ufw/before.rules에 다음과 같이 설정을 추가해줍니다. 이때 eth0 대신 확인한 네트워크 인터페이스를 입력해야합니다.
```bash
$ ip route | grep default
```
```bash
# /etc/ufw/before.rules

#
# rules.before
#
# Rules that should be run before the ufw command line added rules. Custom
# rules should be added to one of these chains:
#   ufw-before-input
#   ufw-before-output
#   ufw-before-forward
#

# START OPENVPN RULES
# NAT table rules
*nat
:POSTROUTING ACCEPT [0:0] 
-A POSTROUTING -s 10.8.0.0/8 -o eth0 -j MASQUERADE
COMMIT
# END OPENVPN RULES

# Don't delete these required lines, otherwise there will be errors
*filter
. . .
```
ufw가 forwarding을 허용하도록 설정을 변경합니다.
```bash
# /etc/default/ufw
DEFAULT_FORWARD_POLICY="ACCEPT"
```
마지막으로 OpenVPN에서 사용할 포트를 방화벽에서 열어줍니다. 포트와 프로토콜을 바꾸어 설정하였다면, 여기서 해당하는 포트와 프로토콜을 열어줘야합니다.
```bash
$ sudo ufw allow 443/udp
$ sudo ufw disable
$ sudo ufw enable
```

AWS instance를 사용한다면, 한가지 더 해주어야 할 설정이 있습니다. 바로 보안그룹에서 OpenVPN 포트로의 인바운드 패킷을 허용하는 것이죠. [여기](https://stackoverflow.com/questions/17161345/how-to-open-a-web-server-port-on-ec2-instance)를 참조하세요.

### 2.2 client config, certificate, key pair 생성
client에서 사용할 configuration 파일을 쉽게 여러 번 만들 수 있도록 합니다. 샘플 client 설정을 base.conf로 복사하고,
```bash
$ mkdir -p ~/client-configs/files
$ chmod 700 ~/client-configs/files
$ cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf ~/client-configs/base.conf
```
이를 저희의 설정에 맞도록 재설정합니다. 
```bash
# ~/client-configs/base.conf

# server_IP_address 대신 OpenVPN 서버의 IP 주소를 적으면 됩니다.
remote server_IP_address 443        

# udp 또는 tcp로 서버의 설정에 맞게 변경합니다.
proto udp                          

# 주석(;)을 해제합니다.
user nobody                                                             
group nobody                                                           

# 다음 부분을 찾아 주석처리 합니다. 
# ca ca.crt
# cert client.crt
# key client.key        

# 다음 부분을 추가합니다.
cipher AES-128-CBC
auth SHA256
key-direction 1

# 다음 부부을 주석처리한 상태로 추가합니다.
# client 환경에 따라 설정을 켜야할 수도 있습니다.
# script-security 2
# up /etc/openvpn/update-resolv-conf
# down /etc/openvpn/update-resolv-conf
```
그리고 다음 스크립트 파일을 ~_client-configs_make_config.sh로 저장합니다. 이 스크립트 파일로 config를 손쉽게 생성할 수 있습니다.
```bash
#!/bin/bash

# First argument: Client identifier

KEY_DIR=~/openvpn-ca/keys
OUTPUT_DIR=~/client-configs/files
BASE_CONFIG=~/client-configs/base.conf

cat ${BASE_CONFIG} \
    <(echo -e '') \
    ${KEY_DIR}/ca.crt \
    <(echo -e '\n') \
    ${KEY_DIR}/${1}.crt \
    <(echo -e '\n') \
    ${KEY_DIR}/${1}.key \
    <(echo -e '\n') \
    ${KEY_DIR}/ta.key \
    <(echo -e '') \
    > ${OUTPUT_DIR}/${1}.ovpn
```
그리고 실행 가능하도록 바꿔줍니다. 
```bash
$ chmod 700 ~/client-configs/make_config.sh
```
이제 OpenVPN client에서 사용할 certificate과 key pair를 만들겠습니다. 여기서부터는 client 하나 당 각각 해주어야 하는 작업입니다. 이들을 client에서 만들고 server에서 사인하는 방법도 있지만, 간단하게 하기 위해서 서버에서 이를 만들어 주겠습니다. server와 마찬가지로 client1은 임의의 이름입니다.
```bash
$ cd ~/openvpn-ca
$ source vars
$ ./build-key client1
```
아까 server에서 진행했던 것과 마찬가지로 기본값을 Enter로 적용시키고, 마지막 두 질문에서만 y를 입력하면 됩니다.

만들었던 certificate, key pair를 사용하여 client configuration을 만들면, (위에서 만들었던 key와 동일한 이름을 인자로 넘기면 됩니다.)
```bash
$ cd ~/client-configs
$ ./make_config.sh client1
```

결과로 client1.ovpn이라는 OpenVPN client 설정 파일을 생성하게 됩니다. 이 설정파일을 scp나 sftp 등의 방법으로 client 로 옮겨 OpenVPN을 실행할 때 파라미터로 넘기면 되겠습니다.

### 2.3 client 에서 OpenVPN 으로 VPN 에 연결
저 같은 경우 client로 ubuntu 16.04와 Mac OS X를 사용하였습니다. ubuntu의 경우는 client1이라는 이름을 사용하였고, Mac OS는 client-mac이라는 이름을 사용하여 설정파일을 만들었습니다.

ubuntu client에서는, openvpn을 apt-get을 통해서 설치하고, 서버로부터 전달받은 client1.ovpn으로 openvpn을 실행합니다.
```bash
$ sudo apt-get update
$ sudo apt-get install openvpn
$ sudo openvpn --config client1.ovpn
```
만약 _etc_openvpn/update-resolv-conf가 존재하면, ovpn파일에서 다음을 찾아 주석해제 처리합니다.
```bash
script-security 2
up /etc/openvpn/update-resolv-conf
down /etc/openvpn/update-resolv-conf
```
Ubuntu 서버에서 booting시 openvpn가 실행되게 하려면 [여기](https://askubuntu.com/questions/464264/starting-openvpn-client-automatically-at-boot)를 참조하세요.

Mac OS X같은 경우, 가장 좋은 방법이 Tunnelblick이라는 app을 이용하는 것입니다. Tunnelblick을 설치하면, 서버에서 가져온 설정파일을 실행하는 것만으로 설정을 등록하고 언제든 실행할 수 있게 해줍니다. 다만 routing table을 재설정하는데에 권한 문제가 있어, [여기](https://github.com/Tunnelblick/Tunnelblick/issues/334)를 참고하여 user nobody, group nogroup 부분을 주석처리하여야 정상 작동합니다.

## 3. 결과
![](/assets/img/OpenVPN%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%90%E1%85%A9%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB%20%E1%84%80%E1%85%A1%E1%84%89%E1%85%A1%E1%86%BC%20%E1%84%89%E1%85%A1%E1%84%89%E1%85%A5%E1%86%AF%E1%84%86%E1%85%A1%E1%86%BC(VPN)%20%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8/99F5564A5B94760807.jpg)

이제 위 그림처럼 EC2 instance, 교내 ubuntu 서버, 제 맥북 간의 vpn tunnel이 만들어졌습니다. 각각의 OS는 OpenVPN를 통해 vpn의 가상 네트워크 인터페이스를 다음과 같이 인식합니다. 

Ubuntu client(client1) - ifconfig 

![](/assets/img/OpenVPN%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%90%E1%85%A9%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB%20%E1%84%80%E1%85%A1%E1%84%89%E1%85%A1%E1%86%BC%20%E1%84%89%E1%85%A1%E1%84%89%E1%85%A5%E1%86%AF%E1%84%86%E1%85%A1%E1%86%BC(VPN)%20%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8/997BB1365B95C48810.png)

Mac OS X client (client-mac) - ifconfig

![](/assets/img/OpenVPN%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%90%E1%85%A9%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB%20%E1%84%80%E1%85%A1%E1%84%89%E1%85%A1%E1%86%BC%20%E1%84%89%E1%85%A1%E1%84%89%E1%85%A5%E1%86%AF%E1%84%86%E1%85%A1%E1%86%BC(VPN)%20%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8/996B7F345B95C5543C.png)

ubuntu에서는 10.8.0.6, mac에서는 10.8.0.10이라는 IP 주소를 갖는다는 것을 확인할 수 있습니다. 해당 인터페이스를 사용하면 client-mac (10.8.0.10) -> client1 (10.8.0.6) 을 포함한 3 vpn 노드 간의 모든 통신이 가능한 것이죠. 

![](/assets/img/OpenVPN%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%90%E1%85%A9%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB%20%E1%84%80%E1%85%A1%E1%84%89%E1%85%A1%E1%86%BC%20%E1%84%89%E1%85%A1%E1%84%89%E1%85%A5%E1%86%AF%E1%84%86%E1%85%A1%E1%86%BC(VPN)%20%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8/990A183F5B95C4E018.png)

저 같은 경우 미리 설정해 놓은 vnc를 사용하여 Ubuntu client의 데스크탑 환경에 접속할 수 있습니다. 

![](/assets/img/OpenVPN%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%90%E1%85%A9%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB%20%E1%84%80%E1%85%A1%E1%84%89%E1%85%A1%E1%86%BC%20%E1%84%89%E1%85%A1%E1%84%89%E1%85%A5%E1%86%AF%E1%84%86%E1%85%A1%E1%86%BC(VPN)%20%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8/99EB79435B95C8AA25.png)

![](/assets/img/OpenVPN%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%90%E1%85%A9%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB%20%E1%84%80%E1%85%A1%E1%84%89%E1%85%A1%E1%86%BC%20%E1%84%89%E1%85%A1%E1%84%89%E1%85%A5%E1%86%AF%E1%84%86%E1%85%A1%E1%86%BC(VPN)%20%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8/990FE0435B95C8A421.jpg)

![](/assets/img/OpenVPN%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%90%E1%85%A9%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB%20%E1%84%80%E1%85%A1%E1%84%89%E1%85%A1%E1%86%BC%20%E1%84%89%E1%85%A1%E1%84%89%E1%85%A5%E1%86%AF%E1%84%86%E1%85%A1%E1%86%BC(VPN)%20%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8/99DF90435B95C8D111.jpg)

성공 !

저와 같은, 혹은 비슷한 용도로 vpn client를 사용하실 분들을 server를 설정할 때, 모든 패킷을 vpn을 통해 보내는 설정을 넣으시면 안됩니다. 해당 설정을 넣게 되면 다음과 같은 형태로 동작합니다.

![](/assets/img/OpenVPN%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%90%E1%85%A9%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB%20%E1%84%80%E1%85%A1%E1%84%89%E1%85%A1%E1%86%BC%20%E1%84%89%E1%85%A1%E1%84%89%E1%85%A5%E1%86%AF%E1%84%86%E1%85%A1%E1%86%BC(VPN)%20%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8/2.png)

저희가 원하던 그림은 이런 것인데 말이죠.

![](/assets/img/OpenVPN%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%90%E1%85%A9%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB%20%E1%84%80%E1%85%A1%E1%84%89%E1%85%A1%E1%86%BC%20%E1%84%89%E1%85%A1%E1%84%89%E1%85%A5%E1%86%AF%E1%84%86%E1%85%A1%E1%86%BC(VPN)%20%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8/1.png)
