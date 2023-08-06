def split_dict(str, segment_separator='\n', kv_separator=':'):
    """
    根据字符串分离出字典
    :param str: 字符串
    :param segment_separator: kv对之间的分隔符
    :param kv_separator: key和value的分隔符
    :return: 字典
    """
    d = {}
    ss = str.split(segment_separator)
    for s in ss:
        kv = s.split(kv_separator)
        d[kv[0].strip()] = kv[1].strip()
    return d


if __name__ == '__main__':
    # 试着解析chrome_cookie
    print(split_dict(
        '''BAIDUID=76CCA07A563CF5D93006995C481CCEDA:FG=1; BIDUPSID=76CCA07A563CF5D93006995C481CCEDA; PSTM=1571044577; ISSW=1; ISSW=1; BDUSS=G5hTEkwT29Ka35qRXJLWVVMMWlsdnAwRHlaR1VlRlRoflJIRU1VSTUwdU9ZdDlkSVFBQUFBJCQAAAAAAAAAAAEAAAD~NEsM0fS54s~CsLK-srXE1u0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI7Vt12O1bdda; MCITY=-%3A; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; COOKIE_SESSION=4751402_0_4_2_8_19_1_1_4_1_0_0_345975_0_0_0_1586248084_0_1593679432%7C9%230_0_1593679432%7C1; BD_HOME=1; H_PS_PSSID=32095_1427_31671_32140_31253_32046_32231_32110_31639; delPer=0; BD_CK_SAM=1; PSINO=6; sug=3; sugstore=0; bdime=0; H_PS_645EC=1ab5VG%2FG9jiOJIrNdMC0jsBRj%2FNT3pH54y9i6F5YG4EBRcH47ZqD0hvTaRI; ORIGIN=2'''
        , ';', '='))
    # 试着解析chrome_post参数
    print(split_dict(
        '''prod: pc_his
from: pc_web
json: 1'''))
    pass
