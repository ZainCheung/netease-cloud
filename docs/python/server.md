## 服务器部署 {docsify-ignore-all}

推荐使用宝塔面板，在宝塔应用商店里面有一个Python项目管理器，下载安装，并选择3.0以上版本，推荐3.7.2版本.

### 1. 下载安装Python项目管理器

![](https://s1.ax1x.com/2020/06/28/Ngr2K1.png)

### 2. 新建项目

> 这里的netease-cloud就是这个项目的文件夹,我给放在了/www/wwwroot/路径下了,可见我这里下载安装的是3.7.2版本的python框架选择Python，启动方式也为Python，启动文件选择`main.py`端口不用填，勾选安装模块依赖，是否要开机启动自己随意咯，然后确定。

![](https://s1.ax1x.com/2020/06/28/Ng6lE6.png)

![](https://s1.ax1x.com/2020/06/28/NgsKz9.png)

### 3. 确定运行状态

![](https://s1.ax1x.com/2020/06/28/Ng6egJ.png)

这时候项目就开始在运行了，就可以去项目在文件夹的路径，找到`run.log`即可查看运行日志

部署前也要记得先配置，然后再部署