---
title: Dependency Inversion을 통한 효과적인 프로그램 구조화
slug: dependency inversion
tags: [블로그,번역,소프트웨어공학]
---
  

원문: [Effective Program Structuring with the Dependency Inversion Principle](https://medium.com/datadriveninvestor/effective-program-structuring-with-the-dependency-inversion-principle-2d5adf11f863)

이전 SOLID에 관한 4개의 시리즈에서, 유연하고, 유지보수성이 높으며, 재사용 가능한 객체 지향 코드를 어떻게 작성하는지 이야기했습니다. 이 목표를 달성하기 위해서는 특정 개체(클래스, 모듈, 함수, 객체)가 어떻게 자신의 일을 하는지 세심한 주의가 필요합니다. 이에 관한 중요한 고려 사항이 바로 의존성(dependency) 입니다. 하나의 개체의 동작이 다른 개체에 의존적인가요? 그렇다면, 그 둘은 얼마나 강하게 결합(couple)되어 있나요? 한 개체의 변화가 다른 개체로 폭포처럼 흘러내려 가나요? 이러한 질문들은 [Open/Closed Principle](https://medium.com/datadriveninvestor/maintainable-code-and-the-open-closed-principle-b088c737262)과 [Liskov Subsitution Priciple](https://medium.com/@severinperez/making-the-most-of-polymorphism-with-the-liskov-substitution-principle-e22609866429)을 살펴볼 때 다뤘던 질문들이지만, 의존성 구조는 더욱 면밀하게 살펴보아야 하는 문제입니다. 여기서 SOLID의 마지막 원칙이 나오는데, 이것이 바로 Depency Inversion Priciple(DIP)입니다. 

- - - -

## A Quick Refresher on SOLID
SOLID는 다음 5가지 소프트웨어 개발원칙의 앞글자를 따서 만든 말이고, 개발자들로 하여금 유연하고 깔끔한 코드를 작성하는 것을 돕습니다. 5가지 원칙들은 다음과 같습니다.

1. [The Single Responsibility Principle (단일 책임 원칙)](https://medium.com/datadriveninvestor/writing-flexible-code-with-the-single-responsibility-principle-b71c4f3f883f) — 클래스는 단 하나의 책임(responsibility)를 가져야 하고, 따라서 단 하나의 변경 사유를 가집니다.
2. [The Open/Closed Principle (개방-폐쇄 원칙)](https://medium.com/@severinperez/maintainable-code-and-the-open-closed-principle-b088c737262) — 클래스나 다른 개체들은 확장에는 열려있지만, 변경에는 닫혀있어야 합니다.
3. [The Liskov Substitution Principle (리스코프 치환 원칙)](https://medium.com/datadriveninvestor/making-the-most-of-polymorphism-with-the-liskov-substitution-principle-e22609866429) — 객체들은 그 하위 타입으로 대체될 수 있어야 합니다.
4. [The Interface Segregation Principle (인터페이스 분리 원칙)](https://medium.com/datadriveninvestor/avoiding-interface-pollution-with-the-interface-segregation-principle-5d3859c21013) — 범용 인페이스 보다는 특정 클라이언트를 위한 인터페이스가 더 낫습니다.
5. The Dependency Inversion Principle (의존관계 역전 원칙) — 구체화보다는 추상화에 의존해야 합니다.

## The Dependency Inversion Principle
본질적으로, DIP는 구조에 관한 것입니다. 당신이 프로그램 개체들을 구조화하는 방식과 그 개체들이 서로 상호작용하는 방법은 나머지 SOLID 원칙에 대한 당신의 능력(이전 글에서 논했던 SOLID 사용상의 이점)에 직접적인 영향을 미칩니다. 의존성이 잘못 관리되면, 당신의 코드가 유연하고 유지보수성과 재사용성이 높아질 가능성이 급격히 줄어듭니다. 

Rober C. Martin은 DIP에 관한 그의 논문에서 잘못 설계된 소프트웨어의 주된 특성을 열거하였습니다: 유연하지 않습니다(rigid). 변화가 한 곳에서 다른 곳으로 흘러가 영향을 미치기 때문에 변경이 쉽지 않습니다; 망가지기 쉽습니다(fragile). 변경이 예기치 않은 고장을 불러 일으킵니다; 이식성이 없습니다(immobile). 개체가 다른 개체에 연관되어 있어 쉽게 재사용할 수 없습니다. [1] Martin은 이러한 문제점들이 주로 잘 구조화되지 않은 설계때문에 나타난다고 하였습니다. 개체가 다른 개체에 강하게 결합(couple)할수록, 유연하지 않고 깨지기 쉽고 이식성이 없는 성질이 증가합니다. 다시 말해서, 의존성 관리는 더욱 유연하여 유지보수와 재사용이 쉬운 소프트웨어를 작성하는데애 아주 중요한 요소입니다.

만약 나쁜 소프트웨어가 의존성 구조와 관련이 있다면, 어떻게 이를 해결해야 할까요? Martin은 전형적인 의존성 구조를 뒤집어 의존성 역전이라고 하였습니다. 전통적인 개체 layering에서는 high level의 개체는 low level의 개체에 의존적이고, 결국 low level의 개체는 더 low한 level의 개체에 의존적이게 됩니다. 이것이 전형적인 top-down 구조이고, 이 구조에서는 행동(policy) level에 해당하는 일을 하는 개체는 점점 세부사항에 초점을 맞추는 의존성 체인 아래로 행동을 위임합니다. 이런 모델의 문제점은 low level에서의 변경이 high level에서의 변경을 강제하고 결국 high level의 개체를 재사용하기 어렵게 만든다는 것입니다. 이 구조를 high level과 low level의 개체 모두가 공유된 추상화에 의존적인 “역전된(inverted)” 의존관계 구조와 비교해봅시다. 여기서는 소프트웨어 프로그램의 각기 다른 레이어들이 상호작용할 때 공유된 추상화를 사용하기로 약속합니다. 그렇게 하면 각 레이어는 디테일을 구현하는 것에서 해방되지만, 다른 개체에 영향을 미칠 걱정 없이 선택할 수 있게 됩니다.

명확하게 이야기하자면, DIP는 high level과 low level 모듈이 공통의 추상화에 의존적이어야 한다는 것이고, 더 나아가 디테일과 추상화가 서로 의존적이기보다는 디테일만 추상화에 의존적이어야 한다는 것입니다. 이런 원칙에 따라 의존관계 구조를 구현하면, 모듈을 재사용에 열려있도록 다른 모듈로부터 해방시킬 수 있습니다. 개체가 추상화 의존관계에 대한 미리 규정된 contract을 따르기만 한다면, 그 개체는 어디에서든 사용될 수 있는 것입니다.

- - - -

## A Failure to Abstract
당연하게도, 실제 세계에서 적용될 의도로 만들어진 원칙들을 이해하기 가장 좋은 방법은 예시와 연습입니다. 추상화를 더 잘 사용하였다면 이점을 누릴 수 있었을 프로그램을 봅시다.

```csharp
using System;

namespace dip_1
{
    class Program
    {
        static void Main(string[] args)
        {
            var bakery = new Restaurant("Bakery");
            bakery.Cook("cookies");
        }
    }

    class Restaurant
    {
        public string Name { get; set; }

        private Oven Oven = new Oven();

        public Restaurant(string name)
        {
            this.Name = name;
        }

        public void Cook(string item)
        {
            this.Oven.LightGas();
            this.Oven.Bake(item);
            this.Oven.ExtinguishGas();
        }
    }

    class Oven
    {
        public bool On { get; set; }

        public void LightGas()
        {
            Console.WriteLine("Lighting the oven's gas!");
            this.On = true;
        }

        public void ExtinguishGas()
        {
            Console.WriteLine("Extinguishing the oven's gas!");
            this.On = false;
        }

        public void Bake(string item)
        {
            if (!this.On)
            {
                Console.WriteLine("Oven's gas is not turned on.");
            }
            else
            {
                Console.WriteLine("Now baking " + item + "!");
            }
        }
    }
}
```

위 예시는 음식점의 활동을 운영하는 프로그램을 작성한 완벽하게 합리적인 첫 시도입니다. 간결하게 하기 위해서, 식당이 많은 일을 하지 않지만 다른 기능을 위해 프로그램이 어떻게 확장되어야 할지 보일 것입니다. `Restaurant` 클래스는 `Oven` 멤버를 가지고 있고 `Oven` 객체의 세 메소드(`LightGas`, `Bake`, `Extiguish`)를 호출하는 `Cook`이라는 메소드를 호출합니다. 실제로 프로그램이 실행되면 `“Bakery”`라는 이름으로 `Restaurant` 클래스를 성공적으로 인스턴스화하고 맛있는 쿠키를 만드는데 사용할 수 있습니다.

프로그램 내에 모든 것이 작동하는데, 무엇이 문제일까요? 다음을 생각해봅시다.

* `Restaurant` 클래스는 `Oven` 객체 사용에 의존적입니다. 만약 음식점에서 다른 조리 기구를 사용하게 하고 싶다면 어떻게 해야 할까요? 현재 구현 상으로는 `Restaurant` 클래스에 가서 클래스를 수정하지 않고는 아무것도 할 수 없는데, 이는 Open/Closed 원칙을 위반하는 것입니다.
* `Oven` 객체의 변경이 프로그램을 따라 폭포처럼 흘러가 `Restaurant` 클래스의 `Cook` 메소드를 망가뜨릴 가능성이 있습니다. 예를 들어, 만약 석유를 사용하는 오븐 대신 전기 오븐을 사용하기로 결정하여 `LightGas`와 `ExtiguishGas`를 바꾸기로 하였다면 어떨까요? 이는 바로 `Restaurant` 망가뜨리는데, `Oven`의 현재 메소드 이름을 사용하는데 의존하고 있기 때문입니다. 
* `Restaurant`와 `Oven`의 결합(coupling)이 이식성을 낮춰, `Oven`을 같이 가져가지 않고는 `Restaurant`를 재사용할 수 없게 합니다. (새로운 프로그램이 `Oven`을 전혀 사용하지 않더라도 말이죠.)

위 예제는 작동하지만, 잘못 설계된 프로그램입니다. 유연하지 않고, 망가지기 쉽고 이식성도 없습니다. 저희는 이것 보다는 잘 할 수 있죠.

- - - -

## Abstraction and Inversion
저희의 예제 프로그램은 개선할 여지가 아주 많습니다. 더 좋은 의존관계 구조를 설계하기 위한 첫걸음으로, 실제 어떤 종류의 추상화가 여기 존재하는지 생각해 보아야 합니다. `Restaurant`는 `Oven`을 `Cook` 메소드를 수행하기 위한 부분으로서 `Oven`을 사용합니다. 이것이 중요한 단서인데, 그 의도가 실제로는 `Oven`과 전혀 관계가 없고 일반적인 요리를 하는데에 있다는 것입니다. 물론 저희 쉐프는 오븐 이외에도 다른 조리법이 있다는 것을 알고있으니 요리하는 기구에 대한 생각을 추상화하여 그녀에게 더 많은 선택지를 줘봅시다. 

```csharp
using System;

namespace dip_2
{
    class Program
    {
        static void Main(string[] args)
        {
            var bakery = new Restaurant("Bakery", new Oven());
            bakery.Cook("cookies");

            var crepery = new Restaurant("Crepery", new Stove());
            crepery.Cook("crepes");
        }
    }

    class Restaurant
    {
        public string Name { get; set; }

        public ICooker Cooker { get; set; }

        public Restaurant(string name, ICooker cooker)
        {
            this.Name = name;
            this.Cooker = cooker;
        }
        
        public void Cook(string item)
        {
            this.Cooker.TurnOn();
            this.Cooker.Cook(item);
            this.Cooker.TurnOff();
        }
    }

    interface ICooker
    {
        bool On { get; set; }

        void TurnOn();

        void TurnOff();

        void Cook(string item);
    }

    class Oven : ICooker
    {
        public bool On { get; set; }

        public void TurnOn()
        {
            Console.WriteLine("Turning on the oven!");
            this.On = true;
        }

        public void TurnOff()
        {
            Console.WriteLine("Turning off the oven!");
            this.On = false;
        }

        public void Cook(string item)
        {
            if (!this.On)
            {
                Console.WriteLine("Oven not turned on.");
            }
            else
            {
                Console.WriteLine("Now baking " + item + "!");
            }
        }
    }

    class Stove : ICooker
    {
        public bool On { get; set; }

        public void TurnOn()
        {
            Console.WriteLine("Turning on the stove!");
            this.On = true;
        }

        public void TurnOff()
        {
            Console.WriteLine("Turning off the stove!");
            this.On = false;
        }

        public void Cook(string item)
        {
            if (!this.On)
            {
                Console.WriteLine("Stove not turned on.");
            }
            else
            {
                Console.WriteLine("Now frying " + item + "!");
            }
        }
    }
}
```

이번 버전의 프로그램에서는 `ICooker`라는 추상화를 만들었고 이는 `Restaurant`와 모든 요리 기구 사이의 공통의 contract의 역할을 하게 됩니다. `Restaurant`에 특정 요리 기구를 하드코딩하는 것 대신, 인스턴스화 시점에 조리 기구를 전달하고 해당 요리 기구의 `Cook` 메소드를 사용합니다. 한편, `Oven` 클래스는 `ICooker` 인터페이스를 구현(implement)하여 일반적인 “조리 기구”의 역할을 수행하도록 합니다. 그리고 다른 기구들도 같은 역할을 할 수 있다는 것을 보이기 위해, 같은 방식으로 `Stove` 클래스를 만들었습니다. 프로그램이 실행되면, 각각 오븐과 스토브를 사용하는 2개의 서로 다른 식당을 같은 Restaurant 클래스를 사용하여 인스턴스화 할 수 있습니다. 두 식당은 예상대로 쿠키와 크레페를 각각 만들게 됩니다.

이전 버전과 비교해 본다면, 몇가지 구조적인 개선점이 보일 것입니다.

* `Restaurant` 클래스는 더이상 `Oven` 클래스에 의존적이지 않습니다. `ICooker` 인터페이스에 정의된 contract을 따르기만 한다면, 다른 조리 기구들을 가진 식당을 원하는대로 만들어낼 수 있다는 것을 의미합니다.
* `Oven` 클래스는 `TurnOn`, `TurnOff`, `Cook` 메소드를 `ICooker`에 정의된 대로 구현하도록 일반화(generalize)되었습니다. 그 결과로 `Restaurant` 클래스에 영향을 미치지 않고 `Oven` 클래스를 변경(예로, 석유 오븐과 전기 오븐 중 어떤 것을 사용할지 정하는 것)할 수 있게 되었습니다. 
* 클래스 간의 결합이 느슨해졌기 때문에, 모든 클래스의 이식성이 향상되었습니다. 각각은 `ICooker` 인터페이스에 의존적이지만, `ICooker`는 추상화이기 때문에 구체적인 구현 없이 쉽게 다른 프로그램으로 이식될 수 있습니다.

당연하게도 이 짧은 프로그램에도 여전히 개선할 여지가 남아있습니다. (아마 홈키친이나 푸드트랙에 사용될 수 있는 `IKitchen` 인터페이스를 구현할 수 있겠죠.) 하지만 DIP 덕분에 유연성, 유지보수성, 재사용성의 측면에서 첫 번째 버전보다 나아진 것은 확실합니다.

- - - -

## TL;DR
마지막 소프트웨어 개발 SOLID 원칙은 DIP입니다. 이는 high level과 low level 모듈이 직접적으로 서로에게 의존성을 가지는 것이 아닌 공통의 추상화에 의존성을 가져야 한다는 원칙입니다. DIP를 사용하면 한 곳에서의 변경이 다른 곳에 미치는 영향을 줄이는 방식으로 의존성을 구성할 수 있기 때문에 프로그램의 유연성과 유지보수성을 높일 수 있습니다. 게다가 DIP는 한 프로그램의 개체를 다른 프로그램에서 사용할 수 있는 정도를 높여줍니다. DIP를 잘 지키기 위한 첫걸음은 프로그램 내의 추상화를 이해하고 상세한 구현을 하드코딩하기 보다는 추상화를 사용하여 개체 간의 contract을 만들어내는 것입니다.

- - - -

이것이 SOLID 원칙에 대한 4개의 시리즈의 끝입니다! 나눴던 이야기들을 즐기고 배운 것이 있었으면 좋겠습니다. 짚고 넘어가야 할 사항이나 추천할만한 사항이 있으면 다른 독자들을 위해서 댓글로 남겨 주시기 바랍니다. 읽어주셔서 감사합니다!

새로운 글이 나올 때마다 알람을 받고 싶다면 Medium, Twitter 에서 저를 팔로우 하시거나 개인 블로그를 구독해주세요. 즐거운 코딩하세요!

- - - -

### References
[1. Paper: The Dependency Inversion Principle; Martin, Robert C.](https://web.archive.org/web/20110714224327/http://www.objectmentor.com/resources/articles/dip.pdf)

[2. Article: DIP in the Wild; Schuchert, Brett L.](https://martinfowler.com/articles/dipInTheWild.html)

[3. Wikipedia: Dependency Inversion Principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle)