# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/7 15:56
contact: jindaxiang@163.com
desc: AQI 解密函数文件
此部分参考 https://github.com/PKUJohnson/OpenData/tree/master/opendatatools/aqi2
感谢 PKUJohnson 提供的加解密函数
"""
import base64
import hashlib
import re

from Cryptodome.Cipher import AES, DES


def has_month_data(href):
    return href and re.compile("monthdata.php").search(href)


def pkcs7padding(text):
    """
    明文使用 PKCS7 填充
    最终调用 AES 加密方法时, 传入的是一个 byte 数组，要求是 16 的整数倍, 因此需要对明文进行处理
    :param text: 待加密内容(明文)
    :return:
    """
    bs = AES.block_size  # 16
    length = len(text)
    bytes_length = len(bytes(text, encoding="utf-8"))
    # tips：utf-8编码时，英文占1个byte，而中文占3个byte
    padding_size = length if (bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
    padding_text = chr(padding) * padding
    return text + padding_text


def pkcs7unpadding(text):
    """
    处理使用PKCS7填充过的数据
    :param text: 解密后的字符串
    :return:
    """
    length = len(text)
    unpadding = ord(text[length - 1])
    return text[0 : length - unpadding]


def aes_encrypt(key, iv, content):
    """
    AES加密
    key,iv使用同一个
    模式cbc
    填充pkcs7
    :param key: 密钥
    :param content: 加密内容
    :return:
    """
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 处理明文
    content_padding = pkcs7padding(content)
    # 加密
    encrypt_bytes = cipher.encrypt(bytes(content_padding, encoding="utf-8"))
    # 重新编码
    result = str(base64.b64encode(encrypt_bytes), encoding="utf-8")
    return result


def aes_decrypt(key, iv, content):
    """
    AES解密
     key,iv使用同一个
    模式cbc
    去填充pkcs7
    :param key:
    :param content:
    :return:
    """
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # base64解码
    encrypt_bytes = base64.b64decode(content)
    # 解密
    decrypt_bytes = cipher.decrypt(encrypt_bytes)
    # 重新编码
    result = str(decrypt_bytes, encoding="utf8")
    # 去除填充内容
    result = pkcs7unpadding(result)
    return result


def decrypt_response(des_key, des_iv, aes_key, aes_iv, content):
    """
    AES解密
    key,iv使用同一个
    模式cbc
    去填充pkcs7
    :param content:
    :return:
    """
    aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    des = DES.new(des_key, DES.MODE_CBC, des_iv)
    # base64解码
    encrypt_bytes = base64.b64decode(content)
    # 解密
    decrypt_bytes = aes.decrypt(encrypt_bytes)
    decrypt_bytes = base64.b64decode(decrypt_bytes)
    decrypt_bytes = des.decrypt(decrypt_bytes)

    # base64解码
    decrypt_bytes = base64.b64decode(decrypt_bytes)
    # 重新编码
    result = str(decrypt_bytes, encoding="utf8")
    # 去除填充内容
    # result = pkcs7unpadding(result)
    return result


"""
his_aes_client_key = "weJGsdsdf6FxF9=="
his_aes_client_iv = "sewg29nsl="
his_des_key = "sgfsfKsg8723jF=="
his_des_iv = "yfw3wexsd="
his_aes_server_key = "efsdsbafa6xFe8lcg=="
his_aes_server_iv = "o2muxyVs5cwedbQ=="
his_aes_client_key = hashlib.md5(his_aes_client_key.encode(encoding="utf8")).hexdigest()[16:32].encode("utf8")
his_aes_client_iv  = hashlib.md5(his_aes_client_iv.encode(encoding="utf8")).hexdigest()[0:16].encode("utf8")
his_des_key = hashlib.md5(his_des_key.encode(encoding="utf8")).hexdigest()[0:8].encode("utf8")
his_des_iv  = hashlib.md5(his_des_iv.encode(encoding="utf8")).hexdigest()[24:32].encode("utf8")
his_aes_server_key = hashlib.md5(his_aes_server_key.encode(encoding="utf8")).hexdigest()[16:32].encode("utf8")
his_aes_server_iv  = hashlib.md5(his_aes_server_iv.encode(encoding="utf8")).hexdigest()[0:16].encode("utf8")
"""

real_aes_server_key = "tGFsbXNwewZlcg=="
real_aes_server_iv = "w9VydmVswewexbQ=="
real_aes_client_key = "WksdsdflFweFZ=="
real_aes_client_iv = "klsfw9nsp="
real_des_key = "ssfefwksdjskdsj=="
real_des_iv = "skzlkpoi="

real_aes_client_key = (
    hashlib.md5(real_aes_client_key.encode(encoding="utf8"))
    .hexdigest()[16:32]
    .encode("utf8")
)
real_aes_client_iv = (
    hashlib.md5(real_aes_client_iv.encode(encoding="utf8"))
    .hexdigest()[0:16]
    .encode("utf8")
)

real_des_key = (
    hashlib.md5(real_des_key.encode(encoding="utf8")).hexdigest()[0:8].encode("utf8")
)
real_des_iv = (
    hashlib.md5(real_des_iv.encode(encoding="utf8")).hexdigest()[24:32].encode("utf8")
)

real_aes_server_key = (
    hashlib.md5(real_aes_server_key.encode(encoding="utf8"))
    .hexdigest()[16:32]
    .encode("utf8")
)
real_aes_server_iv = (
    hashlib.md5(real_aes_server_iv.encode(encoding="utf8"))
    .hexdigest()[0:16]
    .encode("utf8")
)
