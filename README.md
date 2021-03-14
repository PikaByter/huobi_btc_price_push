# 监测火币BTC价格，并推送到微信（2021.3.14）

### 项目介绍：



### 如何使用:

* 将项目下载到本地

* 安装好**python**和**pip**，**cd**进目录并执行代码，安装依赖：

  ```shell
  pip install -r requirements.txt
  ```

* 按照项目介绍中的方法，申请一个方糖推送的key并绑定微信，打开fangtang_push.py，填写到对应位置：
  
  ```shell
  from util.my_urllib import mypost
  
  # 自己去申请一个
  API_Key=""
  
  # 封装方糖推送服务
  ...
  ```

* 配置好科学上网，确保能够访问火币的API站点

* cd进项目目录，执行

  ```
  python run.py
  ```

  

