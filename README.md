# watchdog


### == 背景 ==

参加了一个活动组织, 他们以 discuz 为基础制作了一个论坛用于活动组织和总结

    - 只有登录用户才能看到论坛的各个版块/话题
    - 每周固定时间会发活动帖, 想参加的话需要不停刷新, 直到活动帖出现
    - 点进活动贴, 按格式回帖
    - 次日负责人会一一回复, 告知是否申请成功, 先回贴的优先

**简而言之, 就是用来自动监控想指定的活动贴, 并在活动贴发出的第一时间按格式回贴**


### == 彩蛋 ==

- 支持多人一起申请, 每个用户用一个协程来维护 session
- 简单实现了一个日志, 可以指定日志级别
- 登录如果碰到验证码 -- 小憩一会吧, 暂时没处理


### == 环境 ==

- python 版本

    用 `python 2.7` 开发, 不保证其他版本能正常运行

- 第三方库

    ```
    $ sudo -H pip install -r requirements.txt
    ```

- 配置文件

    ```
    # 按照模板改一下配置文件里的匹配项, .gitignore 目前配置忽略 instance/*ini
    $ cp instance/config.ini.tpl instance/config.ini
    ```


### == 运行 ==

加 `-h` 查看 `Usage`, 暂时只有日志级别一个参数

```
$ ./watchdog.py -h
Usage: watchdog.py [OPTIONS]

Options:
  --log-level [debug|info|warning|error]
                                  Log level  [default: info]
  -h, --help                      Show this message and exit.
```

现在配置了 3 个用户:

- fang: 一次完整的流程
- alpha: 回复一条已经存在的消息
- omicron: 配置缺失

```
$ ./watchdog.py
[INFO] 2017-03-07 12:56:08: <dispatch>-main ready to dispatch
[INFO] 2017-03-07 12:56:08: <WatchDog>-fang init
[INFO] 2017-03-07 12:56:08: <WatchDog>-alpha init
[INFO] 2017-03-07 12:56:08: <WatchDog>-omicron init
[INFO] 2017-03-07 12:56:08: <Auth>-fang init
[INFO] 2017-03-07 12:56:08: <Auth>-alpha init
[ERROR] 2017-03-07 13:00:33: <Auth>-omicron init failed  [<type 'exceptions.KeyError'>|'name']
[ERROR] 2017-03-07 13:00:33: <WatchDog>-omicron init the watchdog  [<type 'exceptions.Exception'>|'name']
[INFO] 2017-03-07 12:56:09: <Auth>-alpha confirm succ
[INFO] 2017-03-07 12:56:09: <Topic>-alpha init
[INFO] 2017-03-07 12:56:09: <Auth>-fang confirm succ
[INFO] 2017-03-07 12:56:09: <Topic>-fang init
[INFO] 2017-03-07 12:56:09: <Topic>-alpha hit the pattern: http://simple.com/forum.php?mod=viewthread&tid=255&extra=page%3D1
[INFO] 2017-03-07 12:56:09: <Post>-alpha init
[INFO] 2017-03-07 12:56:09: <Topic>-fang hit the pattern: http://simple.com/forum.php?mod=viewthread&tid=649&extra=page%3D1
[INFO] 2017-03-07 12:56:09: <Post>-fang init
[INFO] 2017-03-07 12:56:09: <Post>-alpha reply exist already
[INFO] 2017-03-07 12:56:09: <Post>-fang submit succ
[INFO] 2017-03-07 12:56:09: <dispatch>-main all is finished
```

or 你只想看 warn 级别及以上的日志

```
$ ./watchdog.py --log-level=warn
[ERROR] 2017-03-07 13:00:33: <Auth>-omicron init failed  [<type 'exceptions.KeyError'>|'name']
[ERROR] 2017-03-07 13:00:33: <WatchDog>-omicron init the watchdog  [<type 'exceptions.Exception'>|'name']
```


### == 命名 ==

- 登录(Auth)
- 主题(Topic)
- 帖子(Post)


### == TODO ==

- 验证码
