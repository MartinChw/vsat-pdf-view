from flask import abort


def args_strip(args, check_list=[]):
    new_args = {}
    for key in args.keys():
        if args.get(key) is not None and isinstance(args.get(key), str):
            new_args[key] = args.get(key).strip()
        if key in check_list:
            if args.get(key) is None or args.get(key) == '':
                raise Exception(key + "不能为空")
    return new_args
