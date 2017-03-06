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


### == 运行环境 ==

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


### == 一些命名 ==

- 主题(Topic)
- 帖子(Post)


### == TODO ==

- 验证码
