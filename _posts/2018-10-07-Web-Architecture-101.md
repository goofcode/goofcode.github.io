---
title: Web Architecture 101
tags: [블로그, 번역]
---

웹 아키텍처 101 - 웹개발자를 시작할 때 알았다면 좋았을 기본 아키텍처

[원문](https://engineering.videoblocks.com/web-architecture-101-a3224e126947) (Storyblocks는 원저자가 VP로 있는 회사의 이름입니다.)

![](/assets/img/2018-10-07-Web-Architecture-101/1_K6M-x-6e39jMq_c-2xqZIQ.png)

위 다이어그램은 Storyblocks의 아키텍처를 꽤나 잘 나타내는 그림입니다. 경험이 많은 웹 개발자가 아니라면 복잡해 보이겠지만, 각 컴포넌트에 대해 깊이 알아보기 전에 간단하게 짚고 넘어간다면 훨씬 접근하기 쉬워질 것입니다.

> 한 유저가 구글에 “숲 속의 강렬하고 아름다운 안개와 햇빛”이라고 검색하면, 가장 [첫번째 검색 결과](https://www.storyblocks.com/stock-image/strong-beautiful-fog-and-sunbeams-in-the-forest-bxxg0dvxdzj6gt9ini)를 저희 사진 및 벡터 이미지 사이트인  Storyblocks에서 찾을 수 있습니다. 유저가 결과를 클릭하면 이미지 상세 페이지로 redirect됩니다. 유저의 브라우저 내부에서는 Storyblocks에 어떻게 접근할지 알아내기 위해 DNS 서버로 request를  보낸 후 Storyblocks에 request를 보내게 됩니다.  

> 이 request는 load balancer에 도달하게 되는데, load balancer는 10개 또는 현재 request를 처리하는 시점에 실행 중인 웹서버 중 하나를 랜덤하게 선택합니다. 그러면 웹서버는 해당 이미지에 대한 몇몇 정보를 caching service에서 찾아보고 나머지 데이터를 database로부터 받아옵니다. 만약 이미지에 대한 컬러 프로파일이 아직 계산되지 않았다는 것을 알게되면, “color profile” job을 job queue에 보내 해당 job을 비동기적으로 처리하고 그 결과에 따라 적절하게 database를 업데이트하게 됩니다.  

> 다음으로, full text search service로 request를 보내, 사진의 제목을 input으로 사용해 비슷한 사진들을 찾아냅니다. 유저가 Storyblocks의 멤버로 로그인이 되어있으면, account service에서 해당 유저의 정보를 검색합니다. 마지막으로, data firehose로 page view event를 발생시켜 cloud storage system에 기록하고 결과적으로 data warehouse에 load되게 합니다. 이는 분석가들이 사업적인 질문에 대한 답을 얻는데 도움이 됩니다.  

> 서버는 이제 view를 html로 render하고 이를 load balancer로 전달하여 유저의 브라우저로 보냅니다. 해당 페이지는 Javascript와 CSS asset이 포함되어있는데, 이들은 CDN에 연결되어 있는 cloud storage system에 load되어 있어서 유저는 CDN에 접근하여 이 정보들을 가져옵니다. 마지막으로, 브라우저는 유저가 page를 시각적으로 볼 수 있게 그려(render)줍니다.  

다음으로는 각 컴포넌트에 대한 “101”(주로 개론 수업의 수업 번호) 소개를 하면서 앞으로 살펴볼 웹 아키텍처 전반에 대한 생각의 틀을 제공하고, 제가 Storyblocks에서 배웠던 몇몇 글들을 따라가면서 구체적인 구현 권장사항을 제시하겠습니다.

## 1. DNS
DNS는 “Domain Name Server”의 준말로 world wide web을 가능하게하는 기반 기술입니다. 거의 모든 기본적인 수준의 DNS는 domain 이름(google.com 등)에서 IP 주소(85.129.83.120 등)로의 key/value 검색을 제공하는데, 이는 컴퓨터에서 출발한 request가 적절한 서버에 도착하도록 경로를 설정(route)하는데에 필요합니다. 전화번호에 비유하자면, domain 이름과 IP 주소의 차이는 “john에게 전화"와 “201-867-5309로 전화”의 차이와 같습니다. 옛날에 john의 번호를 찾기 위해 전화번호부를 뒤져야 했던 것처럼, domain으로부터 IP 주소를 찾기 위해서는 DNS가 필요합니다. DNS가 인터넷 세계에서의 전화번호부라고 생각해도 좋습니다.

DNS에 대해서 더 깊이 살펴볼 부분들이 있지만, 101 수준에서는 중요하지 않기 때문에 넘어가도록 하겠습니다.

## 2. Load Balancer
load balancer에 대한 자세한 사항들을 다루기 전에, 수평적인 vs 수직적인 application scaling에 대해 조금 살펴봐야 합니다. 이들이 무엇이고 어떻게 다를까요?  [StackOverflow 포스트](https://stackoverflow.com/questions/11707879/difference-between-scaling-horizontally-and-vertically-for-databases)에 간결하게 설명이 되어있는데, 수평적 scaling은 resource pool에 기계를 더 추가하는 것을 의미하는 반면, “수직적인 scaling”은 현존하는 기계에 더 많은 출력(power)를 추가(즉, CPU, RAM)하는 것을 의미하는 것입니다.

웹개발에서는 (거의) 항상 수평적으로 scale하는 것을 선호하는데, 간단히 말하자면 무언가 고장나기 때문입니다. 서버는 임의대로 고장나고, 네트워크는 성능이 저하(degrade)되며 전체 데이터 센터가 종종 연결이 끊어집니다. 하나 이상의 서버를 가짐으로써 어플리케이션이 계속 동작할 수 있도록 대비하는 것입니다. 다른 말로, 어플리케이션이 “fault tolerant(장애를 견뎌내는)“하도록 만드는 것입니다. 둘째로, 수평적 scaling은 서로 다른 backend 부분들(웹서버, database, 임의의 service 등)이 서로 다른 서버에서 동작하도록 하여 결합도(couple)을 최소한으로 유지시켜 줍니다. 마지막으로, 수직적인 scale로는 불가능한 scale을 가능하게 합니다. 당신의 어플리케이션에 필요한 모든 연산을 할 수 있는 컴퓨터는 이 세상에 없습니다. 구글의 검색 플랫폼이 본질적인 예시가 될 수 있고, 이는 물론 더 작은 scale을 가진 회사에도 적용됩니다. 예를 들어 Storyblocks는 150개에서 400개의 EC2 인스턴스를 사용합니다. 수직적 scaling을 통해 필요한 전체 연산량을 제공하는 것을 어려웠을 것입니다.

좋습니다, load balancer로 되돌아가 보죠. load balancer는 수평적 scaling을 가능하게 하는 마법의 소스입니다. load balancer는 들어오는 request를 복제된 다수의 어플리케이션 서버 중 하나로 보내고, 해당 어플리케이션 서버로부터 돌아온 response를 client로 보냅니다. 모든 어플리케이션 서버가 request를 동일한 방식으로 처리함으로써 request를 단순 분배할 수 있도록 하여 어떤 특정 서버에도 과부하가 걸리지 않도록 해야 합니다.

결론적으로 load balancer는 꽤 직관적입니다. 그 내부에는 분명 복잡한 것들이 있지만 101 수준에서는 다룰 필요가 없습니다.
 
## 3. Web Application Server
고수준(high level)의 web application server는 상대적으로 설명하기 쉽습니다. web application server는 유저의 request를 처리하며 중심이 되는 비지니스 로직을 수행하고 유저의 브라우저로 HTML을 돌려 보냅니다. 이를 위해 web application server는 일반적으로 database, caching layer, job queue, search service, 다른 microservice, data/login queue 등과 같은 다양한 종류의 백엔드 인프라와 정보를 주고 받습니다. 이미 언급했듯, 일반적으로 최소 2개, 종종 훨씬 많은 수의 web application server가 load balancer에 연결되어 유저의 request를 처리하게 됩니다.

application 서버를 구현할 때는 특정 언어(Node.js, Ruby, PHP, Scala, Java, C# .NET 등)와 웹 MVC 프레임워크(Node.js의 경우 Express, Ruby on Rails, Scala의 경우 Play, PHP의 경우 Laravel 등)을 선택해야 된다는 사실을 알고 있어야 합니다. 하지만, 이러한 언어와 프레임워크에 대한 디테일은 여기서 다루지 않겠습니다.

## 4. Database Servers
모든 web application은 정보를 저장하기 위해서 하나 또는 하나 이상의 database를 사용합니다. database는 자료 구조(data structure)의 정의하고 새로운 데이터의 삽입하고, 존재하는 데이터의 검색, 업데이트, 삭제, 연산하는 방법을 제공합니다. 대부분의 경우 web application server는 database와 직접적으로 데이터를 주고 받고, job server 또한 마찬가지입니다. 추가적으로, 각 백엔드 service는 application의 다른 부분들과는 떨어져있는 고유한 database를 가지기도 합니다.

각 아키텍처 컴포넌트의 특정 기술에 대해 자세히 다루지 않으려고 했지만, 다음 단계의 database에 대한 이야기를 하지 않는 것은 오히려 좋지 않을 것 같습니다. 바로 SQL과 NoSQL이죠.

SQL은 “Structured Query Language(구조적 쿼리 언어)”의 줄임말이고, 이는 많은 사람들에게 접근이 허용된 관계 데이터(relational data)에 대한 표준적인 쿼리 방식을 제공하기 위해서 1970년대에 발명되었습니다. SQL database에서 데이터는 테이블에 저장되며 이 테이블들은 주로 정수인 공통의 ID를 통해 연결됩니다. 유저의 과거 주소 정보를 저장하는 간단한 예제를 한번 봅시다. users와 user_addresses라는 2개의 테이블을 유저의 id를 통해서 연결합니다. 아래 이미지에 간단하게 나타나 있습니다. user_addresses 내의 user_id라는 column이 users 테이블의 id column에 대한 “foreign key(외래키)"가 되어 두 테이블을 연결하고 있습니다.

![](/assets/img/2018-10-07-Web-Architecture-101/5A10C6C8-6E24-41B1-AA5C-3EBFB9DC8D69.png)

SQL에 대해 잘 모른다면, [Khan Academy의 튜토리얼](https://www.khanacademy.org/computing/computer-programming/sql)을 진행해보는 것을 강력히 추천합니다. SQL은 웹 개발에서 빠질 수 없는 부분이므로, application을 적절하기 위해서는 SQL에 대한 기본적인 지식이 필요합니다.

NoSQL은 “Non-SQL”을 줄임말인데, 큰 web application으로부터 발생하는 방대한 양의 데이터를 처리하기 위해 떠오른 새로운 종류의 database 기술입니다(대부분의 SQL의 변종들은 수평적으로 scale되지 않고, 특정한 부분에서 수직적으로 scale됩니다). NoSQL에 대해서 아무것도 모른다면, 다음과 같은 high level의 입문서부터 시작하는 것을 추천합니다.

* https://www.w3resource.com/mongodb/nosql.php
* http://www.kdnuggets.com/2016/07/seven-steps-understanding-nosql-databases.html
* https://resources.mongodb.com/getting-started-with-mongodb/back-to-basics-1-introduction-to-nosql

또한, 웹 산업이 인터페이스로 SQL에 의존하고 있고, 심지어 NoSQL의 인터페이스로도 사용하기 때문에 SQL을 반드시 배워야 합니다. 요즘 시대에 SQL을 피할 수 있는 방법은 없습니다.

## 5. Caching Service
caching service는 간단한 key/value 데이터 저장을 제공하여 O(1) 시간에 가깝게 정보를 저장하고 찾는 것을 가능하게 합니다. application은 주로 비싼(expensive, 연산량이 많은) 연산의 결과를 caching service를 이용하여 저장하고, 다음에 해당 연산이 필요할 때 연산을 하지 않고 저장된 cache를 불러옵니다. application은 database query, 외부 서비스, 어떤 URL에 대한 HTML 등의 결과를 저장할 수 있습니다. 실제 application의 몇몇 예시들을 들어보겠습니다.

* Google에서는 “개” 또는 “테일러 스위프트"와 같은 흔한 검색 쿼리에 대한 결과를 매번 다시 연산하기보다는 cache에 저장합니다.
* Facebook은 post 데이터, 친구 등 로그인 했을 때 보이는 정보들을 cache에 저장합니다. Facebook의 caching에 대한 자세한 내용은 [여기](https://medium.com/@shagun/scaling-memcache-at-facebook-1ba77d71c082)서 확인해 보세요 
* Storyblocks에서는 서버사이드 React 렌더링의 HTML 결과, 검색 결과, typeahead 결과 등을 cache합니다.

가장 널리 쓰이는 두 가지 caching server 기술이 바로 Redis와 Memcache입니다. 이 둘에 대해서는 다른 포스트에서 다루어보도록 하겠습니다.

## 6. Job Queue & Servers
대부분의 web application은 유저의 request에 응답하는 것과 직접적으로 관련 없이 비동기적으로 어떤 작업들을 수행해야 할 필요성이 있습니다. 예로, Google이 검색 결과를 보여주기 위해서는 전체 인터넷을 돌아다니며 수집하고 인덱싱할 필요가 있습니다. 이를 유저가 검색하는 시점에 수행할 필요는 없죠. 대신, 비동기적으로 웹을 돌아다니며 검색 인덱스를 업데이트합니다.

비동기적인 일을 가능하게 하는 아키텍처는 다를 수 있지만, “job queue” 아키텍처라는 것이 가장 일반적으로 사용됩니다. job queue 아키텍처는 수행되어야 하는 job으로 이루어진 queue와, job을 수행하는 하나 이상의 job server (종종 "workers”라고 불립니다) 두 부분으로 이루어져 있습니다.

job queue는 비동기적으로 실행되어야 하는 job들을 list의 형태로 저장합니다. 가장 간단한 형태는 FIFO queue 이지만, 결국 대부분의 application은 일종의 priority queuing 시스템이 필요하게 됩니다. 어떤 정기적인 스케줄에 의해서이건 유저의 행동의 의해서이건, application에서 job이 수행되어야 하면 단순히 적절한 job을 queue에 넣기만 하면 됩니다.

예를 들어 Storyblocks에서는 job queue를 이용하여 화면 뒤에서 일어나는 비지니스에 필요한 많은 일들을 처리 합니다. 비디오와 사진을 인코딩하고, metadtat tagging, 유저 통계 수집, 비밀번호 재설정 이메일 등의 job을 수행합니다. 처음에는 간단한 FIFO queue로 시작했지만, 비밀번호 재설정과 같은 시간에 민감한 작업들이 바로 처리될 수 있도록 priority queue를 사용하도록 업그레이드 하였습니다.

job server는 job을 처리합니다. 수행되어야 하는 작업이 존재하는지 job queue를 poll하고, job이 있다면 queue로부터 job을 pop하여 해당 job을 수행합니다. 프로그래밍 언어와 프레임워크에 대한 선택지는 많지만, 역시 여기서는 다루지 않겠습니다.

## 7. Full-text Search Service
많은 아니, 거의 대부분의 웹 application이 유저가 (종종 “query"라고 불리는) 텍스트 인풋을 입력하면 application이 "관련된" 결과를 출력하는 검색 기능을 가지고 있습니다. 이 기술을 가능하게 하는 것이 주로 “[full-text search](https://en.wikipedia.org/wiki/Full-text_search)”라고도 불리는 기능이고, 이는 query의 키워드를 담고있는 정보를 찾기 빠르게 찾기 위해 역 인덱스(inverted index)를 사용합니다.

![](/assets/img/2018-10-07-Web-Architecture-101/1_gun_BpdDH9KrNna1NnaocA.png)

위에서는 제목 내의 키워드를 사용하여 문서를 빠르게 검색하기 위해 3개 문서의 제목을 어떻게 역 인덱스로 변환하는지를 보여주고 있습니다. “in”, “the”, “with”와 같은 단어들은 주로 역 인덱스에는 포함되지 않는다는 사실을 알아두세요.

몇몇의 database에서는 바로 full-text search를 수행할 수 있는 반면 (예로, MySQL은 full-text search를 지원합니다.), 별도의 “search service”에서 역인덱스를 계산하고 저장하여 query 인터페이스를 제공하는 것이 더 일반적인 방법입니다. 오늘날 가장 대중적인 full-text search 플랫폼은 [Elasticsearch](https://www.elastic.co/products/elasticsearch)이고 [Sphinx](http://sphinxsearch.com/)나 [Apache Solr](http://lucene.apache.org/solr/features.html)을 사용하는 방법도 있습니다. 

## 8. Services
application이 어느정도의 규모 이상을 커지게 되면, 몇몇 “service”들은 독립적인 application으로 빠져나오게 됩니다. 바깥 세상에는 보이지 않지만, application과 다른 service들은 그런 service들과 서로 상호작용합니다. 예를 들어 Storyblock에서는 기능적이고 조직적인 몇가지 service가 있습니다:

* 계정 서비스에서는 전 사이트에 걸친 유저 데이터이를 저장하여, cross-sell의 기회를 더 쉽게 제공할 수 있도록 하고 통일성있는 UX를 만들어냅니다.
* 컨텐츠 서비스는 모든 비디오, 오디오, 이미지 컨텐츠에 대한 메타데이터를 저장합니다. 컨텐츠 다운로드 인터페이스와 다운로드 히스토리 인터페이스를 제공합니다.
* 결제 서비스는 고객 신용카드 결제에 대한 인터페이스를 제공합니다.
* HTML -> PDF 서비스는 HTML로부터 PDF 문서를 만들어내는 간단한 인터페이스를 제공합니다.

## 9. Data
오늘날, 기업의 생사는 얼마나 데이터를 잘 활용하는가에 달려있습니다. 요즘의 거의 모든 application은 특정 규모에 이르면 data가 확실히 수집되고, 저장되고, 분석하도록 data pipleline을 사용합니다. 일반적인 pipeline은 3개의 주요 stage로 구성됩니다:

1. application은 “firehose”로 데이터(주로 유저 interaction에 대한 이벤트)를 보냅니다. 이 “firehose”는 데이터를 가져와 처리하는 streaming 인터페이스를 제공합니다. 종종, raw 데이터를 변형하거나 다른 정보를 덧붙여(augment) 또 다른 firehose로 전달합니다. AWS Kinesis와 Kafka가 가장 흔히 사용되는 기술입니다.
2. raw 데이터 그리고 마지막으로 변형되거나 덧붙여진 데이터 또한 cloud storage에 저장됩니다. AWS Kinesis는 "firehose"라는 설정을 지원하는데, 이는 엄청나게 간단한 설정으로 cloud storage (S3)에 raw 데이터를 저장할 수 있게 해줍니다.
3. 변형 또는 덧붙여진 데이터는 종종 분석을 위해서 data warehouse에 load됩니다. 저희는 스타트업 업계에서 점점 더 많이 사용하는 AWS Redshift를 사용하고 있습니다만, 더 큰 회사에서는 Oracle 또는 다른 사설 warehouse 기술을 사용합니다. 데이터가 충분히 많아지면 분석을 위해서 Hadoop과 같은 NoSQL 맵리듀스 기술이 필요할지도 모릅니다. 

아키텍처 그림에 나타나지 않은 또 다른 단계도 있습니다. application이나 service의 database를 data warehouse에 로드하는 것입니다. 예를 들어, Storyblocks에서는 매일 밤 VideoBlocks, AudioBlocks, StoryBlocks, 계정 service, 컨트리뷰터 포털 database를 Redshift에 로드합니다. 이는 핵심 비지니스 데이터를 유저 interaction 데이터와 함께 위치하게 하여 분석가들에게 온전한 데이터셋을 제공합니다.

## 10. Cloud storage
AWS에 따르면, “cloud storage는 인터넷 상에서 데이터를 저장하고, 접근하고, 공유할 수 있는 간단하고 확장성있는 방법입니다.” cloud storage를 사용하면 로컬 파일 시스템에 저장해야 했던 거의 모든 데이터를 HTTP를 통한 RESTful API의 이점을 그대로 취하면서 저장하고 접근할 수 있습니다. Amazon의 S3가 제공하는 것이 현재까지 가장 인기있는 cloud storage이고, 저희 Storyblocks에서 또한 비디오, 사진, 오디오, CSS, Javascript, 유저 이벤트 데이터 등을 저장하는데에 광범위하게 사용하고 있는 것이기도 합니다.

## 11. CDN
CDN은 “Content Delivery Network”의 줄임말이고, 이는 HTML, CSS, Javascript, 이미지 등의 정적인 asset을 원본 서버에서 제공하는 것보다 훨씬 더 빠르게 제공하는 기술입니다. 이는 전세계에 있는 “edge” 서버에 콘텐츠를 배포하여 유저가 asset을 원본 서버가 아닌 “edge”에서 다운로드하게 합니다. 예를 들어 아래 그림에서 스페인에 있는 유저가 뉴욕에 있는 원본 서버로 웹 페이지를 요청하면, 해당 페이지는 대서양을 건너는 느린 HTTP request를 사용하는 대신 영국에 있는 CDN “edge” 서버로부터 load됩니다.

![](/assets/img/2018-10-07-Web-Architecture-101/29B97FEA-7855-4CF9-9E9C-CBE239C72F5A.png)

더 자세한 내용은 [여기](https://www.creative-artworks.eu/why-use-a-content-delivery-network-cdn/)를 참고해 보세요. 일반적인 web application은 CSS, Javascript, 이미지, 비디오와 다른 asset들을 제공하기 위해서 항상 CDN을 사용합니다. 몇몇의 application은 정적 HTML page에 대해서도 CDN을 사용합니다.

## 맺음말
이것으로 웹 아키텍처 101을 마치겠습니다. 도움이 되었길바랍니다. 여기서 다뤘던 컴포넌트들에 대해 조금 더 자세하게 알아보는 201 글을 내년에나 내후년 중으로 시리즈로 포스트할 수 있으면 좋겠습니다.