"""Console script for nin."""
import sys
import click

import sys

import dns.resolver as rs

@click.command()
@click.argument('domain')
def dns(domain):
    ''' DNS解析
    '''
    rts = [
        'CNAME', # 说明当前域名只是一个别名，并非真正等域名。譬如，www.abc.com, mail.abc.com，放在同一个IP下，就可以这么干。
        'A', # IP地址
        'AAAA', # IPv4地址
        'MX', # 邮件服务器
        'TXT', # 记录文本 
        'NS', # 存储DNS到DNS服务器
        'SOA', # 存储有关域到管理员信息
        'SRV', # 记录指定服务器到主机和端口，如IP语音等
        'PTR', # 反响查找中提供域名
    ]

    for record_type in rts:
        try:
            answers = rs.query(domain, record_type) 
            if len(answers) > 0:
                click.secho(record_type +':', fg='green')
                for item in answers:
                    print('', item)
        except rs.NoAnswer:
            pass
        except rs.NoNameservers:
            pass
        except rs.Timeout:
            pass