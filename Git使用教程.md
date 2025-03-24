# **GIT使用教程**

## 使用前的的配置：

1.进行安装

2.进入GIT BASH进行用户名配置：

```bash
git config --global user.name “用户名”
```

3.进入GIT BASH进行邮箱配置：

```bash
git config --global user.email “邮箱地址”
```

4.进入GIT BASH进行保存用户名与密码：

```bash
git config --global credential.helper store
```

5.进入GIT BASH 查询GIT的配置信息：

```bash
git config --global --list
```



## 创建项目仓库：(在自己选择的仓库文件夹下，打开GIT BASH)

使用linux:

(

```bash
mkdir [目录名]

cd  [目录名]
```

)

```bash
git  init  //在当前地址中，创建一个名为.git的项目仓库(属性为隐藏)
```

```bash
git  init  [repository]  // 在当前地址中，创建一个名为[repository]的项目仓库
```

## 抓取远程仓库中的项目：	

```bash
git clone [https://www.bilibili.com]     //抓取远程仓库到本地仓库
```

 

## 文件提交到本地仓库：

1）提交到暂存区：

```bash
git  add  [文件名]  // git add . 提交全部文件 | git add *.txt 使用通配符
```



2）提交到本地仓库：

```bash
git commit  -m “注释”  // 可以不加-m 直接 git commit 但是会进入到一个交互模式，一般是以VIM编辑的。
```

​	<img src="C:\Users\JG\AppData\Roaming\Typora\typora-user-images\image-20250319212907714.png" alt="image-20250319212907714" style="zoom: 50%;" />



3）显示工作目录和暂存区的状态：

```bash
git status 
```

<img src="C:\Users\JG\AppData\Roaming\Typora\typora-user-images\image-20250319213047367.png" alt="image-20250319213047367" style="zoom:50%;" />

## 添加远程仓库并推送：

1）添加远程仓库：

```bash
	git remote add origin [仓库地址]
```



2）本地仓库上传到远程仓库

```bash
git push origin master    // origin 是远程仓库名称（可更改）， msater 是要推送的本地分支（可更改）
```



## 分支操作：

创建本地分支：

```bash
git branch [分支名]
```



查看本地分支：

```bash
git branch 
```



## 版本回退：

```bash
Git reset --hard [commitID] // 提交记录ID，可以用git log来查看 
```

<img src="C:\Users\JG\AppData\Roaming\Typora\typora-user-images\image-20250319213511009.png" alt="image-20250319213511009" style="zoom:50%;" />
