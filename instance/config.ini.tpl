[DEFAULT]
; global
domain = http://simple.com/

; for auth
login_page_url = http://simple.com/member.php?mod=logging&action=login
login_submit_url = http://simple.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LmJvv&inajax=1
login_referer_url = http://simple.com/./
login_succ_flag = 欢迎
formhash_regex = formhash" value="(\w+)"

; for topic
topic_page_url = http://simple.com/forum.php?mod=forumdisplay&fid=2
;; time unit is seconds
topic_interval = 1

; for post
post_max_retry = 3
post_reply_args_regex = name=\"{}\".*?value=\"([^\"]+)
post_reply_url_regex = id=\"fastpostform\".*?action=\"([^\"]+)


; ===============================
; the follow thing is custom
; you need change is each time
; ===============================
post_regex = <a href="([^"]*).*?3.11/12.*?休闲


[fang]
name = fang
passwd = 123456

; ===============================
; the follow thing is custom
; you need change is each time
; ===============================
msg = 我来啦

[dou]
; you can rewrite any one in DEFAULT
topic_page_url = http://simple.com/forum.php?mod=forumdisplay&fid=51

name = dou
passwd = 654321

; ===============================
; the follow thing is custom
; you need change is each time
; ===============================
msg = 沙发 啦啦啦
