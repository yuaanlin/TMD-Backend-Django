# TMD - 物联网 DDL 提示灯

TMD (Too Many Deadlines) 是浙江大学 2019 级计算机专业的学生林沅霖 (学号 3190106167) 在 2020 短学期课程《Arduino 作品设计》制作的期末作品。本次提交与展示的作品由三个模块构成，除了 Arduino 作品本体以外，还包含了配套的后端服务器以及手机App。

---

## 设计理念

大学生通常同时被作业、考试、学生组织等等的大量 deadlines 所弄的焦头烂额，因此我希望可以透过一个书桌上优雅的装饰品来在生活中协助大学生处理这样子的问题。TMD 的主体是三条由磨砂灯罩盖住的 LED 灯条，灯条在程序的控制下显示出不单调却也不会影响注意力的视觉效果。

<img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/7704bd14-abab-4efb-b465-4b1a1dde8f4f/red.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20200907%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20200907T033727Z&X-Amz-Expires=86400&X-Amz-Signature=29c496c6140a089b6b9bf25b3d4481516e45706b967adf79b8e51a5e894242df&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22red.jpg%22"  width="450" />            |  <img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/baa5ae23-8eef-4348-b46b-116cf859459e/green.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20200907%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20200907T033745Z&X-Amz-Expires=86400&X-Amz-Signature=54ad8dbea0782081befb0fe209866b775315dee7a77f7e4606d1e4e95e8a5478&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22green.jpg%22"  width="450" />
:-------------------------:|:-------------------------:
在 Deadline 只剩不到一天，灯会显示红色  |  Deadline 还有超过一个星期，灯会显示绿色

---

## 作品特色

1. 灯条的高度和颜色会随着 ddl 的**剩余时间有所变化**，方便用户了解情况。
2. 使用**手势传感器**来进行操作，无需和装置本体由直接接触，增进了便利性。
3. 数据保存在**线上数据库**，透过开放的 API 可以从**多个不同的平台**对数据进行查询与操作。
4. 透过**限制最高亮度**以及降低**灯泡密度**的方式有效的压低了功率要求，即使是 USB 电源也能直接使用，也可以视需求调整参数来用更高功率的电源得到更好的视觉效果。
5. 试图采用了 MVC 模式进行开发，作品中的灯条和 LCD 屏幕相当于是视图层 (View) ，视图层的显示内容直接反映了名为 State 的类里面的数据，因此该类相当于是模型层 (Model)，而该类的 public functions 用于操控模型中的数据，相当于是控制器 (Controller)，控制器除了修改 State 内的数据外，也负责调控何时应该渲染视图层的哪些部位。
6. 数据传递的格式选用了能够在各种编程语言及执行环境都易于处理的 Json 格式，对本作品的系统提供了高度扩展性。

---

## 作品视频连接

[https://www.bilibili.com/video/BV1nh411X7hZ](https://www.bilibili.com/video/BV1nh411X7hZ?p=1&share_medium=iphone&share_plat=ios&share_source=QQ&share_tag=s_i&timestamp=1599391274&unique_k=sfDGEN)

---

## 作品源码

完整源码由于内容较多，本章节统一给出 Github 的代码仓库链接。

1. Arduino 源码

    [https://github.com/ken20001207/TMD-Arduino](https://github.com/ken20001207/TMD-Arduino)

2. 后端源码

    [https://github.com/ken20001207/TMD-Backend](https://github.com/ken20001207/TMD-Backend)

3. App源码

    [https://github.com/ken20001207/TMD-App](https://github.com/ken20001207/TMD-App)

---

## 制作过程

---

### 建立后端服务

首先，我从后端服务开始建立，后端的部分我选用了 Python 的 Django 框架进行搭建，并且选择了属于 NoSQL 类型的 MongoDB 数据库来保存数据。在建立后端的过程中我遇到了几个问题：

1. **后端服务无法连线到数据库**

    由于 Django 默认支持的数据库是四种 SQL 类型的数据库，但我选择的是属于 NoSQL 的 MongoDB，因此我必须修改默认的数据库配置，经过一段时间的研究以后，我得知了我必须透过 MongoEngine 这个套件才能从 Django 内连线到 MongoDB 的数据库。

    但 MongoEngine 配置好了以后，却一直没办法透过数据库的地址连接，经过了又一段时间的调试，我发现到了因为我申请的 MongoDB 官方提供的线上数据库服务 MongoDB Atlas 内建开启了数据库集群 (Replica Set) 的功能，因此我没有办法透过其中一个子节点的地址去连接，而是必须透过 SRV 记录去动态获取应该链接的数据库位置，这才终于正式连上了数据库。

    ```python
    # TMD-Backend/TMDBackend/settings.py

    # 默认的数据库设置为空
    DATABASES = {'default': {'ENGINE': ''}}

    # 使用 SRV 记录连线到 MongoDB
    connect('todos', host='mongodb+srv://<userID>:<password>@cluster0.wrbwz.gcp.mongodb.net', connect=False)
    ```

2. **数据库保存数据的时区问题**

    我发现到当我用 ISO8601 时间格式传递一个 DDL 进入数据库后，存入的值和我当时发送的值不一样了，一开始以为是 MongoEngine 的 Bug，仔细观察后才发现其实存入的时间是相同的，但保存在数据库的时间统一使用 UTC 时间，因此存入的值会比输入的值少了八个小时。

    问题又来了，虽然保存在数据库的时间和输入的时间相同，只是不同时区而已，但从数据库取出数据时，Python 却把这个时间当成是当前本地时区的时间了。换言之，在取出时间的同时，时间的值少了 8 个小时。我本来想通过正规的时区转换的方式解决这个问题，但是在花了太多时间，最后决定直接手动增加 8 个小时来调回正确的时间。

    ```python
    # TMD-Backend/todos/views.py

    @api_view(['GET', 'POST', 'DELETE'])
    def todo_list(request):
        if request.method == 'GET':
            todos = Todo.objects.all()

            response_data = []
            for todo in todos:
    						
    						# 加 8个小时手动调回本地时间
                ddl = (todo.deadline.astimezone(pytz.timezone('Asia/Taipei')) **+
                       timedelta(hours=8))**.astimezone(pytz.timezone('Asia/Taipei'))

                ddl_string = ddl.strftime("%Y/%m/%d %H:%M")

                response_data.append(
                    dict(id=str(todo.id), title=todo.title,
                         ddl=ddl_string, status=getStatus(todo)
                         ))

            response_data.sort(key=getTimedeltaSec, reverse=True)

            return JsonResponse(response_data, safe=False)
    ```

### 开发 Arduino 作品本体

在建立完一个可用的后端以后，我开始着手建立 Arduino 的本体，Arduino 部分的开发顺序是：我一开始先设计了灯效程式（因为周边器件都还没寄到），接着我决定试着用 MVC 模式进行开发，因此我建立了一个名为 State 的类。

> 「每当 State 中的数据发生改变，视图层就必有某个对应的地方发生改变」

我遵照这这样的原则去设计剩下的程序，例如哪些变量应该被放在 State 这个类里面，然后 State 里面的每个函数当他操作了某个变量以后，应该呼叫哪些程序来重新渲染视图等等 ...

**Model**

```cpp
// TMD-Arduino/Mega2560/model.cpp

State::State() {
		// 当前载入的待办数据，默认最多保存 10 个
    todoDatas = new Todo[10];

		// 记录了当前载入了几个
    todoAmount = 0;

		// 当前显示哪个
    displayTodoIndex = 0;

		// 当前灯应该亮几颗
    shouldLightNum = 5;

		// 当前的灯效模式
    LedMode = DisplayMode::SWIPE_DOWN;
    
		// 动画帧数变量，会不断的更新来推进动画的渲染
		aniVal = 0;

		// 当前显示的颜色
    red = 0;
    green = 0;
    blue = 0;
}
```

**其中一个 Controller 示例**

```cpp
// TMD-Arduino/Mega2560/model.cpp

// 切换当前显示的 Todo
void State::setDisplayTodoIndex(int index) {
    if (todoAmount != 0) {
        if (index < todoAmount) {
            displayTodoIndex = index;
        } else {
            displayTodoIndex = todoAmount - 1;
        }

        Serial.print("Switch displaying Todo index to ");
        Serial.print(displayTodoIndex);
        Serial.print(" (");
        Serial.print(todoDatas[displayTodoIndex].title);
        Serial.println(")");

        printTextLCD(lcd, todoDatas[displayTodoIndex].title,
                     todoDatas[displayTodoIndex].ddl);

        setLEDMode(DisplayMode::NORMAL);

        if (strcmp(todoDatas[displayTodoIndex].status, "ONE_DAY_LEFT") == 0) {
            setShouldLightNum(50);
            setDisplayColor(255, 0, 0);
        } else if (strcmp(todoDatas[displayTodoIndex].status,
                          "ONE_WEEK_LEFT") == 0) {
            setShouldLightNum(25);
            setDisplayColor(255, 170, 0);
        } else {
            setShouldLightNum(10);
            setDisplayColor(0, 255, 0);
        }
    }
}
```

在实作Arduino 的过程中，也遇到了几个难以处理的问题，其中大部分是硬体造成的问题：

1. **Arduino Uno 板的内存不足**

    在接上 ESP8266 以后，服务器的数据成功的从 ESP8266 透过软串口被传送过来 Uno 板内，并且顺利的完成了处理，被存入了 State 中。但当我接上手势传感器以后，LCD 却开始显示大量的乱码，有时还能从乱码中看出一点我保存在变量中但毫无关联的数据。

    原来没有手势传感器是正常的，接上以后反而坏掉了，因此我的第一直觉便是我买到了瑕疵品，劣质的手势传感器使我本来的功能无法正常运作了。但当我开启一个空白的项目以后，单独测试以后发现手势传感器也是可以正常使用的，这时我整个人都傻了，完全没有头绪。

    这个问题想了一个星期左右，最后我发现到当我上传代码到板子时，记录显示全域变量使用了 89% 的内存，其实也很多了但因为没超过 100% 所以没发生错误，但在执行过程中，当 ESP8266 传了数据进来以后内存就直接超过 Uno 板的限制了。因此我就马上又买了一张 Mega2560，然后上传原来的代码上去，果然正常运行了。

2. **手势传感器效果不如预期**

    经过测试发现，手势传感器必须在一个很狭窄范围内才能准确识别到。同时，环境光似乎也对感测器造成了一定程度的影响。

    再来就是，原先买器件时只记得麻烦卖家帮我焊上排针，忘了和他说应该焊在背面，结果排针和感测器居然焊在了同一侧，严重影响了使用。

3. **LED 灯条导致供电不足**

    在选购灯条时，有三种灯泡密度可以选，我想着为了达到最好的视觉效果，就选了最密集的每米144颗灯泡的灯条，寄来接上电以后才发现，Arduino 的 5V 输出根本连一条都无法供应，但当时已经没有足够的时间购买另外的灯条或是购买外接电源模块了。

    因此我做出的解决方案便是直接将这个灯条透过程序的方式降低为每米36颗灯泡（每4颗亮一颗），同时再去限制灯泡发亮的最高亮度，在可接受范围内透过牺牲视觉效果换来了能耗的优化。

    ```cpp
    // TMD-Arduino/Mega2560/model.cpp

    switch (getLEDMode()) {
            case DisplayMode::NORMAL:

                for (int i = 0; i < 3; i++) {
                    strips[i].clear();

                    int up_pos = aniVal / (255 / shouldLightNum);

    								// 透过 j += 4 的方式来减少同时亮起的灯泡数量
                    for (int j = 0; j < shouldLightNum; j += 4) {
                        double pos_diff =
                            1 - ((double)abs(j - up_pos) / (double)shouldLightNum);
    										
    										// 透过 MAX_BRIGHTNESS 来限制最高亮度
                        color = Adafruit_NeoPixel::Color(
                            green * MAX_BRIGHTNESS * pos_diff,
                            red * MAX_BRIGHTNESS * pos_diff,
                            blue * MAX_BRIGHTNESS * pos_diff);

                        strips[i].setPixelColor(j, color);
                    }

                    strips[i].show();
                }

                break;
    ```

### 开发 Demo 用的 App

最后为了拍摄作品影片，我决定开发一个简易的 App 用来对数据库的 DDL 做一些操作。在开发上我选用使用 Typescript 语言编写的 React Native 前端框架。同时，因为已经有了现成的后端服务以及完善的 API 接口，App 在开发起来非常高效。

<img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/f049f4fa-662f-44ab-b976-f91ffd293465/iVBORw0KGgoAAAANSUhEUgAABS0AAAo4CAYAAAC8JoKAAABgmlDQ1BzUkdCIElFQzYxOTY2LTIu-2_3.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20200907%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20200907T040610Z&X-Amz-Expires=86400&X-Amz-Signature=39b09977b024295651de4d369a9da674541e40cb202fb5e54061103d3b21a625&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22iVBORw0KGgoAAAANSUhEUgAABS0AAAo4CAYAAAC8JoKAAABgmlDQ1BzUkdCIElFQzYxOTY2LTIu-2_3.png%22"  width="300" /> | <img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/c145bc16-6278-4c88-9e59-4a324873d3ed/iVBORw0KGgoAAAANSUhEUgAABS0AAAo4CAYAAAC8JoKAAABgmlDQ1BzUkdCIElFQzYxOTY2LTIu-2_2.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20200907%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20200907T040648Z&X-Amz-Expires=86400&X-Amz-Signature=334a6b693e7f381d2c9609f7decffd94d9f04d057c9d302195e7c19f3f59e4f9&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22iVBORw0KGgoAAAANSUhEUgAABS0AAAo4CAYAAAC8JoKAAABgmlDQ1BzUkdCIElFQzYxOTY2LTIu-2_2.png%22"  width="300" /> | <img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/db0fca5d-00ff-4f15-bb15-4557373bc170/iVBORw0KGgoAAAANSUhEUgAABS0AAAo4CAYAAAC8JoKAAABgmlDQ1BzUkdCIElFQzYxOTY2LTIu-2.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20200907%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20200907T041243Z&X-Amz-Expires=86400&X-Amz-Signature=a8bd92b717748238c5d503e3bf4821b69f18a40468473fdeda5e8c6f9ec49937&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22iVBORw0KGgoAAAANSUhEUgAABS0AAAo4CAYAAAC8JoKAAABgmlDQ1BzUkdCIElFQzYxOTY2LTIu-2.png%22"  width="300" />
:-------------------------:|:-------------------------:|:-------------------------:
TMD App 的 DDL 列表 | TMD App 可以刪除 DDL | TMD App 可以新增 DDL

## 实际使用情况

---

实际使用以后主要有以下问题可以改进：

1. 面包线过于冗长，使得整体设备被大量的线覆盖，可以透过将目前的线路设计制作成电路板，来避免这个影响观感的问题。
2. 手势传感器方向错误，导致操作起来不够人性化，也导致了手势传感器无法固定在作品本体上面的问题。可以透过重新焊接排针的方式解决这个问题。
3. 线上版本的数据更动后 Arduino 需要手动刷新，不够及时。可以透过在 ESP8266 新增轮询（Polling）机制来以固定间隔向服务器索取新数据，或是透过 Websocket 等能够建立持续连线的通讯方式来将 Arduino 与服务器建立即时数据沟通机制。
4. LCD 屏幕的长度限制过小，且无法显示中文。可以透过更换更大片且支持中文显示的 LCD 屏幕来解决这个问题。

## 特别感谢 Credits

---

这边特别感谢以下的套件开发者及社群（以字典序排列）：

Too Many Deadlines is use the following packages (in alphabetical order):

[Adafruit_NeoPixel](https://github.com/adafruit/Adafruit_NeoPixel) 用于驱动 LED 灯条

[ArduinoJson](https://github.com/bblanchon/ArduinoJson) 用于处理 Json 数据

[Datetime Picker](https://github.com/react-native-community/datetimepicker) 日期时间选择模块

[Django](https://github.com/django/django) 后端框架

[Django Rest Framework](https://github.com/encode/django-rest-framework) 用于建立 Restful 服务

[Django Rest Framework Mongo Engine](https://github.com/umutbozkurt/django-rest-framework-mongoengine) 用于连接 MongoDB 数据库

[Expo](https://github.com/expo/expo)  React Native 前端框架

[Gesture_PAJ7620](https://github.com/Seeed-Studio/Gesture_PAJ7620) 用于驱动手势传感器

[MsTimer2](https://github.com/PaulStoffregen/MsTimer2) 用于定时呼叫渲染函数

[New-LiquidCrystal](https://github.com/fmalpartida/New-LiquidCrystal) 用于透过 I2C 界面控制 LCD

[React Native Easy Grid](https://github.com/GeekyAnts/react-native-easy-grid) 用于使用网格系统进行界面排版
