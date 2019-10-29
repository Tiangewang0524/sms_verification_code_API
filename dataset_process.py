import json, re

with open('D:/city-version-4.json') as f1:
    with open('D:/city_2.json', 'w+', encoding='utf-8') as f2:
        file_json = json.load(f1)
        print(file_json)
        json.dump(file_json, f2, ensure_ascii=False)

with open('D:/city_2.json', 'r', encoding='UTF-8') as f2:
    json2 = json.load(f2)

    with open('D:/jiemaAPI/dataset/province.txt', 'w+') as f3:
        for each in json2['provinceList']:
            pure_province = each['name'].replace('省', '').replace('市', '').replace('自治区', '')
            pure_province = re.sub('壮族|维吾尔|回族', '', pure_province)
            f3.write(pure_province)
            f3.write('\n')

    with open('D:/jiemaAPI/dataset/city.txt', 'w+') as f4:
        for each in json2['provinceList']:
            for each_cell in each['cityList']:
                if each_cell['name'] != '省直辖县级行政区划' and each_cell['name'] != '市辖区' \
                        and each_cell['name'] != '自治区直辖县级行政区划' and each_cell['name'] != '县':
                    pure_city = re.sub('市|朝鲜族自治州|地区|土家族苗族自治州|藏族自治州|彝族自治州|回族自治州|蒙古自治州|'
                                       '|蒙古族|哈尼族|苗族自治州|苗族侗族自治州|布依族|傣族自治州|傣族景颇族自治州|'
                                       '|傈僳族自治州|白族自治州|藏族羌族自治州|哈萨克自治州', '', each_cell['name'])
                    if pure_city == '克孜勒苏柯尔克孜自治州':
                        pure_city = '克州'
                    f4.write(pure_city)
                    f4.write('\n')

# from __future__ import unicode_literals
#
# from pypinyin import lazy_pinyin
#
# a = ['中国人', '啊', '你好', '台湾人']
# b = [''.join(lazy_pinyin(_)) for _ in a]
# print(sorted(b))