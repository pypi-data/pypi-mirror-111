import argparse
import logging
from itertools import chain
import json
import yaml
from flatten_dict import unflatten
from dict_recursive_update import recursive_update
from weworkapi.CorpApi import CorpApi, CORP_API_TYPE


def merge_message_argfields(message, fields):

    # transform -a'touser=xxx agentid=xxx' to [touser=xxx, argentid=xxx]
    fields = [ fld.split() for fld in fields]

    # flatten the fields list,
    # [[touser=xxx, agentid=xxx], msgtype=text] -> [touser=xxx, agentid=xxx, msgtype=text]
    fields = list(chain(*fields))

    # convert the k=v list to dict
    flat_dict = dict([tuple(fld.split(sep='=', maxsplit=1)) for fld in fields])

    # unflatten the dict
    # ie. {'event.task_id': 'xxx'} -> {'event': {'task_id': xxx}}
    unflat = unflatten(flat_dict, splitter='dot')

    # recursive update the message dict with the unflatten arg fiedls
    return recursive_update(message, unflat)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--corpid', required=True, help='企业微信的企业ID')
    parser.add_argument('-s', '--secret', required=True, help='企业微信内应用的Secret')
    parser.add_argument('-t', '--token_cache', help='access_token的本地缓存文件')
    parser.add_argument('-a', '--field', action='append',
                        help='消息体字段，格式为K=V，添加或覆盖参数message中字段的值，例如 touser=xxx, interactive_taskcard.task_id=xxx')
    parser.add_argument(
        '-f', '--format', choices=['json', 'yaml'], default='json', help='参数message文本的格式')
    parser.add_argument('-m', '--message', help='向企业微信应用发送的消息文本')
    parser.add_argument('-l', '--level', choices=['DEBUG', 'INFO', 'WARNING',
                        'ERROR', 'FATAL', 'CRITICAL'], default='INFO', help='logging level')

    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.level))
    logging.debug(args)
  
    message = dict()
    if args.format == 'json':
        message = json.loads(args.message)
    elif args.format == 'yaml':
        message = yaml.safe_load(args.message)
    message = merge_message_argfields(message, args.field)

    token_cached = None

    # Read access_token from cache file
    if args.token_cache:
        try:
            with open(args.token_cache, mode='r', encoding='utf-8') as f:
                token_cached = f.readline()
        except Exception as e:
            logging.warning(e)

    # Send message using CorpApi
    corpapi = CorpApi(args.corpid, args.secret)
    corpapi.access_token = token_cached
    corpapi.httpCall(CORP_API_TYPE['MESSAGE_SEND'], message)
    logging.info(f'MESSAGE_SEND[{message}]')

    # access_token changed, Write new access_token to cache file
    if args.token_cache and token_cached != corpapi.access_token:
        try:
            with open(args.token_cache, mode='w', encoding='utf-8') as f:
                f.write(corpapi.access_token)
            logging.info(f'Update {args.token_cache} with new refresh token')
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    main()
