# # -*- coding:utf-8 -*-
# # /usr/bin/env python
# """
# Author: Albert King
# date: 2020/2/29 21:13
# contact: jindaxiang@163.com
# desc:
# """
# import hashlib
# import json
# import time
#
# import pandas as pd
# from progressbar import ProgressBar
#
#
# def md5(text):
#     hl = hashlib.md5()
#     hl.update(text.encode(encoding='utf-8'))
#     return hl.hexdigest()
#
#
# class SimuAgent:
#     def __init__(self):
#         # RestAgent.__init__(self)
#         self.user_info = None
#         self.df_fundlist = None
#         self.cookies = None
#
#     def login(self, username, password):
#         url = (
#                 "https://passport.simuwang.com/index.php?m=Passport&c=auth&a=login&type=login&name=%s&pass=%s&reme=1&rn=1"
#                 % (username, password)
#         )
#         self.add_headers({"Referer": "https://dc.simuwang.com/"})
#         response = self.do_request(url)
#         if response is None:
#             return None, "登录失败"
#
#         jsonobj = json.loads(response)
#         suc = jsonobj["suc"]
#         msg = jsonobj["msg"]
#
#         if suc != 1:
#             return None, msg
#
#         self.cookies = self.get_cookies()
#
#         self.user_info = jsonobj["data"]
#         return self.user_info, msg
#
#     def prepare_cookies(self, url):
#         response = self.do_request(url, None)
#         if response is not None:
#             cookies = self.get_cookies()
#             return cookies
#         else:
#             return None
#
#     def _get_rz_token(self, time):
#         mk = time * 158995555893
#         mtoken = md5(md5(str(mk))) + "." + str(time)
#         return mtoken
#
#     def _get_fund_list_page(self, page_no):
#         url = (
#                 "https://dc.simuwang.com/ranking/get?page=%s&condition=fund_type:1,6,4,3,8,2;ret:9;rating_year:1;istiered:0;company_type:1;sort_name:profit_col2;sort_asc:desc;keyword:"
#                 % page_no
#         )
#         response = self.do_request(url)
#
#         if response is None:
#             return None, "获取数据失败", None
#
#         jsonobj = json.loads(response)
#
#         code = jsonobj["code"]
#         msg = jsonobj["msg"]
#
#         if code != 1000:
#             return None, msg, None
#
#         df = pd.DataFrame(jsonobj["data"])
#         pageinfo = jsonobj["pager"]
#         return df, "", pageinfo
#
#     def load_data(self):
#         page_no = 1
#         df_list = []
#         df, msg, pageinfo = self._get_fund_list_page(page_no)
#         if df is None:
#             return None, msg
#
#         df_list.append(df)
#         page_count = pageinfo["pagecount"]
#         process_bar = ProgressBar().start(max_value=page_count)
#
#         page_no = page_no + 1
#         while page_no <= page_count:
#             df, msg, pageinfo = self._get_fund_list_page(page_no)
#             if df is None:
#                 return None, msg
#             df_list.append(df)
#             process_bar.update(page_no)
#             page_no = page_no + 1
#
#         self.df_fundlist = pd.concat(df_list)
#         return self.df_fundlist, ""
#
#     def get_fund_list(self):
#         if self.df_fundlist is None:
#             return None, "请先加载数据 load_data"
#
#         return self.df_fundlist, ""
#
#     def _get_sign(self, url, params):
#         str = url
#         for k, v in params.items():
#             str = str + k + params[k]
#
#         sha1 = hashlib.sha1()
#         sha1.update(str.encode("utf8"))
#         sign = sha1.hexdigest()
#
#         return sign
#
#     def _get_token(self, fund_id):
#         sign = self._get_sign("https://dc.simuwang.com/Api/getToken", {"id": fund_id})
#         url = "https://dc.simuwang.com/Api/getToken?id=%s&sign=%s" % (fund_id, sign)
#         self.add_headers({"Referer": "https://dc.simuwang.com/"})
#         response = self.do_request(url)
#         if response is None:
#             return None, "获取数据失败"
#
#         jsonobj = json.loads(response)
#         code = jsonobj["code"]
#         msg = jsonobj["message"]
#
#         if code != 1000:
#             return code, msg
#
#         self.cookies.update(self.get_cookies())
#
#         salt = jsonobj["data"]
#
#         muid = self.user_info["userid"]
#         # str = 'id%smuid%spage%s%s' % (fund_id, muid, page_no, salt)
#         str = "%s%s" % (fund_id, salt)
#         sha1 = hashlib.sha1()
#         sha1.update(str.encode("utf8"))
#         token = sha1.hexdigest()
#
#         return token, ""
#
#     def _get_fund_nav_page(self, fund_id, page_no):
#         muid = self.user_info["userid"]
#         token, msg = self._get_token(fund_id)
#         if token is None:
#             return None, "获取token失败: " + msg, ""
#
#         url = "https://dc.simuwang.com/fund/getNavList.html"
#         self.add_headers(
#             {"Referer": "https://dc.simuwang.com/product/%s.html" % fund_id}
#         )
#         data = {
#             "id": fund_id,
#             "muid": muid,
#             "page": str(page_no),
#             "token": token,
#         }
#         response = self.do_request(
#             url, param=data, cookies=self.cookies, encoding="utf8"
#         )
#         if response is None:
#             return None, "获取数据失败", ""
#
#         jsonobj = json.loads(response)
#         code = jsonobj["code"]
#         msg = jsonobj["msg"]
#
#         if code != 1000:
#             return code, msg, ""
#
#         df = pd.DataFrame(jsonobj["data"])
#         pageinfo = jsonobj["pager"]
#         return df, "", pageinfo
#
#     def _bit_encrypt(self, str, key):
#         cryText = ""
#         keyLen = len(key)
#         strLen = len(str)
#         for i in range(strLen):
#             k = i % keyLen
#             cryText = cryText + chr(ord(str[i]) - k)
#
#         return cryText
#
#     def _bit_encrypt2(self, str, key):
#         cryText = ""
#         keyLen = len(key)
#         strLen = len(str)
#         for i in range(strLen):
#             k = i % keyLen
#             cryText = cryText + chr(ord(str[i]) ^ ord(key[k]))
#
#         return cryText
#
#     def _decrypt_data(self, str, func, key):
#         # return self._bit_encrypt(str, 'cd0a8bee4c6b2f8a91ad5538dde2eb34')
#         # return self._bit_encrypt(str, '937ab03370497f2b4e8d0599ad25c44c')
#         # return self._bit_encrypt(str, '083975ce19392492bbccff21a52f1ace')
#         return func(str, key)
#
#     def _get_decrypt_info(self, fund_id):
#         url = "https://dc.simuwang.com/product/%s.html" % fund_id
#         response = self.do_request(
#             url, param=None, cookies=self.cookies, encoding="utf8"
#         )
#         if response is None:
#             return None, "获取数据失败", ""
#
#         if "String.fromCharCode(str.charCodeAt(i) - k)" in response:
#             decrypt_func = self._bit_encrypt
#         else:
#             decrypt_func = self._bit_encrypt2
#
#         if response.find("return xOrEncrypt(str, ") > 0:
#             tag = "return xOrEncrypt(str, "
#         else:
#             tag = "return bitEncrypt(str, "
#         pos = response.index(tag) + len(tag) + 1
#         key = response[pos: pos + 32]
#         return decrypt_func, key
#
#     def get_fund_nav(self, fund_id, time_elapse=0):
#
#         if self.user_info is None:
#             return None, "请先登录"
#
#         page_no = 1
#         df_list = []
#         df, msg, pageinfo = self._get_fund_nav_page(fund_id, page_no)
#         if df is None:
#             return None, msg
#
#         df_list.append(df)
#         page_count = pageinfo["pagecount"]
#
#         page_no = page_no + 1
#         while page_no <= page_count:
#             try_times = 1
#             while try_times <= 3:
#                 df, msg, pageinfo = self._get_fund_nav_page(fund_id, page_no)
#                 if df is None:
#                     if try_times > 3:
#                         return None, msg
#                     else:
#                         try_times = try_times + 1
#                         continue
#                 else:
#                     df_list.append(df)
#                     break
#             page_no = page_no + 1
#             if time_elapse > 0:
#                 time.sleep(time_elapse)
#
#         df_nav = pd.concat(df_list)
#         df_nav.drop("c", axis=1, inplace=True)
#         df_nav.rename(
#             columns={"d": "date", "n": "nav", "cn": "accu_nav", "cnw": "accu_nav_w"},
#             inplace=True,
#         )
#
#         # 这个网站搞了太多的小坑
#         func, key = self._get_decrypt_info(fund_id)
#         df_nav["nav"] = df_nav["nav"].apply(lambda x: self._decrypt_data(x, func, key))
#         df_nav["accu_nav"] = df_nav["accu_nav"].apply(
#             lambda x: self._decrypt_data(x, func, key)
#         )
#         df_nav["accu_nav_w"] = df_nav["accu_nav_w"].apply(
#             lambda x: self._decrypt_data(x, func, key)
#         )
#         # df_nav['nav'] = df_nav['nav'] - df_nav.index * 0.01 - 0.01
#         # df_nav['accu_nav'] = df_nav['accu_nav'].apply(lambda x: float(x) - 0.01)
#         # df_nav['accu_nav_w'] = df_nav['accu_nav_w'].apply(lambda x: float(x) - 0.02)
#
#         return df_nav, ""
