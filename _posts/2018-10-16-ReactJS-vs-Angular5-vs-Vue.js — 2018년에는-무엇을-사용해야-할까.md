---
title: ReactJS vs Angular5 vs Vue.js — 2018년에는 무엇을 사용해야 할까
slug: react vs angular vs vue
thumbnail: assets/img/ReactJS%20vs%20Angular5%20vs%20Vue.js%E2%80%8A%E2%80%94%E2%80%8A2018%E1%84%82%E1%85%A7%E1%86%AB%E1%84%8B%E1%85%A6%E1%84%82%E1%85%B3%E1%86%AB%20%E1%84%86%E1%85%AE%E1%84%8B%E1%85%A5%E1%86%BA%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%89%E1%85%A1%E1%84%8B%E1%85%AD%E1%86%BC%E1%84%92%E1%85%A2%E1%84%8B%E1%85%A3%20%E1%84%92%E1%85%A1%E1%86%AF%E1%84%81%E1%85%A1/87521561-69BF-4876-AEC5-3F63D131DB55.png
tags: [블로그,번역]
---
 

원문: [ReactJS vs Angular5 vs Vue.js — What to choose in 2018?](https://medium.com/@TechMagic/reactjs-vs-angular5-vs-vue-js-what-to-choose-in-2018-b91e028fa91d)

![](/assets/img/ReactJS%20vs%20Angular5%20vs%20Vue.js%E2%80%8A%E2%80%94%E2%80%8A2018%E1%84%82%E1%85%A7%E1%86%AB%E1%84%8B%E1%85%A6%E1%84%82%E1%85%B3%E1%86%AB%20%E1%84%86%E1%85%AE%E1%84%8B%E1%85%A5%E1%86%BA%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%89%E1%85%A1%E1%84%8B%E1%85%AD%E1%86%BC%E1%84%92%E1%85%A2%E1%84%8B%E1%85%A3%20%E1%84%92%E1%85%A1%E1%86%AF%E1%84%81%E1%85%A1/87521561-69BF-4876-AEC5-3F63D131DB55.png)

얼마 전 저희는 Angular 2와 React를 비교하는 글을 게재하였습니다. 해당 글에서, 두 프레임워크의 장점과 단점을 설명하며 2017년에 목적에 따라 무엇을 선택해야 하는지를 제시하였습니다. 그렇다면 2018년 프론트엔드 시장에서는 무슨 일이 일어나고 있을까요?

JavaScript 프레임워크는 매우 빠르게 발전하고 있는데, 업데이트가 빈번한 Angular와 ReactJS, 또 다른 플레이어 Vue.js가 오늘날 시장을 점유하고 있습니다.

저희는 특정 프레임워크에 대한 사전지식이 필요한 일자리의 수를 분석하였습니다. [indeed.com](indeed.com)에서 조사한 바에 따르면, 60,000개 이상의 일자리에 대해 다음과 같은 분포를 얻을 수 있었습니다.

![](/assets/img/ReactJS%20vs%20Angular5%20vs%20Vue.js%E2%80%8A%E2%80%94%E2%80%8A2018%E1%84%82%E1%85%A7%E1%86%AB%E1%84%8B%E1%85%A6%E1%84%82%E1%85%B3%E1%86%AB%20%E1%84%86%E1%85%AE%E1%84%8B%E1%85%A5%E1%86%BA%E1%84%8B%E1%85%B3%E1%86%AF%20%E1%84%89%E1%85%A1%E1%84%8B%E1%85%AD%E1%86%BC%E1%84%92%E1%85%A2%E1%84%8B%E1%85%A3%20%E1%84%92%E1%85%A1%E1%86%AF%E1%84%81%E1%85%A1/A4A71B05-E9CD-4768-AD7C-1DD2A111DA39.png)

이와 같은 데이터를 고려하여, 저희는 각 프론트엔드 프레임워크의 주된 장점과 단점을 공유하고 기술 전문가들과 엔지니어들이 각 개발 요구에 맞춰 최선의 선택을 하도록 돕겠습니다.

## Pros and cons of Angular 5
Angular는 슈퍼히어로 같은 JavaScript MVVM 프레임워크이고, 2009년에 만들어졌으며, 상호작용이 많은(highly interactive) 웹 어플리케이션을 만드는데에 적합합니다.

**Angular 5의 장점:**

* 강화된 RXJS, 빠른 컴파일 (3초 미만), HttpClient와 같은 새로운 기능들이 있습니다.
* 문서화가 자세하게 되어 있어 동료에게 묻지 않고도 개인 개발자가 필요한 정보를 얻는 것이 가능합니다. 하지만 교육에 더 많은 시간이 필요합니다.
* 양방향 데이터 바인딩은 어플리케이션에 대한 행동 하나가 미치는 에러 발생의 위험성을 낮춰줍니다.
* MVVM (Model-View-ViewModel)은 어플리케이션의 같은 부분을 같은 데이터셋을 사용하여 여러 개발자들이 각자 작업할 수 있도록 해줍니다.
* 모듈의 컴포넌트들과 관련된 기능의 Dependency injection과 일반적인 모듈성을 제공합니다.

**Angular 5의 단점**

* 첫번째 버전의 Angular로부터 파생된 복잡한 문법을 가지고 있습니다. 그럼에도, Angular 5는 비교적 배우기 쉬운 TypeScript 2.4를 사용합니다.
* 이전 버전으로부터 최신 버전으로 이전시킬 때 migration 이슈가 발생할 수 있습니다.

Angular 5를 사용하는 회사들: Upwork, Freelancer, Udemy, YouTube, Paypal, Nike, Google, Telegram, Weather, iStockphoto, AWS, Crunchbase.

## Pros and cons of ReactJS
ReactJS는 JavaScript 라이브러리이며, Facebook에 의해 2013년에 오픈소스화되었고, 데이터가 주기적으로 변화하는 거대한 웹 어플리케이션을 만드는데에 적합합니다.

**ReactJS의 장점**:

* 배우기 쉽습니다. React는 문법이 간단하기 때문에 훨씬 배우기 쉽습니다. 엔지니어들은 HTML 작성 능력을 다시 상기하기만 하면 됩니다. Angular같이 TypeScript를 깊이 배울 필요가 없습니다. 
* 유연성이 높고, 반응성이 아주 뛰어납니다.
* 가상 DOM은 HTML, XHTML, XML 형식의 document들을 트리 형태로 배치하여 웹브라우저가 각기 다른 element들을 parsing할 때 수용성(acceptable)이 높아집니다.
* ES6/7과 결합하여, ReactJS는 손쉽게 높은 부하를 처리합니다.
* 하향성(Downward) 데이터 바인딩을 통해 child element가 parent의 데이터의 영향을 주지 못하도록 합니다.
* 100% 오픈소스 라이브러리로, 전세계 개발자들의 contribution으로 매일 업데이트되고 개선됩니다.
* 유저단의 데이터가 동시에 서버단에서 쉽게 표현되기 때문에 확실히 가볍습니다.
* Facebook이 제공하는 “codemods”가 버전 이전 작업의 대부분을 자동화해 주기 때문에, migration이 일반적으로 쉽습니다.

**ReactJS의 단점:**

* 공식 문서의 부족 - ReactJS가 매우 빠르게 개발되기 때문에 적절한 문서화가 이루어지지 않고, 많은 개발자들이 시스템적인 접근 없이 contribute하기 때문에 문서가 조금 난잡합니다.
* React는 자기 주장이 강하지 않습니다. - 이는 개발지가 종종 너무 많은 선택지를 가지게 된다는 뜻입니다. 
* 숙달하는데에 많은 시간이 필요합니다. 이는 MVC 프레임워크를 유저 인터페이스에 어떻게 적용해야 하는지에 대한 깊은 지식을 가지고 있어야 한다는 것을 의미합니다.

ReactJS를 사용하는 회사들: Facebook, Instagram, Netflix, New York Times, Yahoo, Khan Academy, Whatsapp, Codecademy, Dropbox, Airbnb, Asana, Atlassian, Intercom, Microsoft.

## Pros and cons of Vue.js
Vue.js는 JavaScript 프레임워크이며, 2013년에 출시되었고, 높은 유연성을 가진 유저인터페이스와 세련된 sing-page 어플리케이션 개발에 완벽하게 들어맞습니다.

**Vue.js의 장점:**

* 강력한 HTML. 이는 Vue.js가 Angular와 비슷한 성질을 가진다는 것을 의미하고 여러 컴포넌트를 사용하여 HTML 블록을 최적화하는 것을 도와줍니다.
* 상세한 문서. Vie.js는 매우 상세하게 문서화되어 있어 개발자들의 learning curve를 낮춰주고 기본적인 수준의 HTML과 JavaScript만을 사용하는 어플리케이션 개발에 걸리는 많은 시간을 절약해줍니다.
* 적용성(adaptability). Vue.js는 설계와 구조 상 Angular, React와 비슷하기 때문에 다른 프레임워크에서 Vue.js로 빠르게 이전할 수 있습니다.
* 멋진 통합. single-page 어플리케이션과 더 복잡한 웹 어플리케이션의 인터페이스 모두를 Vue.js를 사용하여 구축할 수 있습니다. 전체 시스템에 부정적인 영향을 끼치지 않으면서 현존하는 인프라에 작은 interactive 부분들을 통합시키기 쉽다는 것입니다.
* 확장성. 간단한 구조를 통해 크고 재사용 가능한 template들을 부가적인 시간 투자 없이 개발할 수 있도록 도와줍니다.
* 매우 작은 사이즈. Vue.js는 20KB 정도로 속도와 유연성을 유지하여 다른 프레임워크 보다 더 나은 성능을 가능하게 합니다. 

**Vue.js의 단점:**

* 자료의 부족. Vue.js는 React 또는 Angular에 비해서 작은 시장 점유율을 가지고 있기 때문에, 프레임워크 내의 정보 공유 또한 기초적인 수준에 머물러 있습니다.
* 지나친 유연성에 대한 위험성. 종종 대형 프로젝트에 통합 시키는 과정에서 문제가 발생하고 이에 대한 해법이 아직까지는 없지만, 분명 곧 그 해법이 나타날 것입니다.
* 영어 문서의 부족. 이 때문에 개발 단계에서 부분적으로 복잡해지지만, 점점 더 많은 자료가 영어로 번역되고 있습니다.

Vue.js를 사용하는 회사들: Xiaomi, Alibaba, WizzAir, EuroNews, Grammarly, Gitlab and Laracasts, Adobe, Behance, Codeship, Reuters.

## CONCLUSION
실제 엔지니어들을 위해서, 프레임워크 간의 큰 차이는 없지만 새로운 것에 익숙해지는 것에 시간이 걸릴 뿐입니다. 저희 회사에서는 주로 ReactJS와 Angular 2/4/5에 대한 전문성을 키우고 있지만, Vue.js 또한 고려 대상입니다. 모든 프레임워크는 각자의 장단점을 가지고 있으므로, 제품 개발 동안 각 case에 대한 적절한 선택이 있을뿐입니다.

[https://www.techmagic.co/](https://www.techmagic.co/)