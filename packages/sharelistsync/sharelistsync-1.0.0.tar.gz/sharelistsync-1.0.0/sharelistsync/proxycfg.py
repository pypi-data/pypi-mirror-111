from urllib import parse
import os


def set_proxy(config):
    if config["useproxy"]:
        encodedpass = parse.quote(config['password'])
        proxystr = f"" + config['protocol'] + "://" + config['username'] + ":" + encodedpass + "@" + config['server']
        os.environ['HTTP_PROXY'] = os.environ['HTTPS_PROXY'] = proxystr
