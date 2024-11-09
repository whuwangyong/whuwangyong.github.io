本项目是基于Hugo搭建的静态博客。

### GitHub Action
最近发现GitHub Pages支持直接部署Hugo源文件，GitHub Action会进行编译和发布。这就简单很多。在此之前，我是在本地编译，并且使用了多个分支来存储源码和编译后的静态文件，脚本写得也很复杂。原来这套做法移到[github.io-old](https://github.com/whuwangyong/github.io-old)仓库留个备份。

### 辅助脚本
GitHub Action会调用publish.py脚本，该脚本实现了以下功能：
- 提交新增博文的URL到bing，提高博文被bing收录的速度
- 提交关键字索引文件到algolia，实现站内搜索

### 主题
本博客使用的Hugo主题为[FixIt](https://github.com/hugo-fixit/FixIt)，以submodule的形式引入项目。

主题更新：
```bash
git submodule update --remote [--merge]
git add .
git commit -m "upgrade theme"
git push
```
第一次克隆带有子模块的项目，首先需要初始化子模块：
```bash
git submodule update --init [--recursive]
```
