## install/run scrapyoxy

### install scrapoxy

```
sudo npm install -g scrapoxy
```

### generate configuration file
```
scrapoxy init path/to/conf.json
```

### edit configuration file
```
"commander": {
        "password": "your-scrapoxy-commander-password"
    },
    "instance": {
        "port": 3128,
        "scaling": {
            "min": 1,
            "max": 2
        }
    },
    "providers": {
        "type": "awsec2",
        "awsec2": {
            "accessKeyId": "Your-AWS-Access-Key",
            "secretAccessKey": "Your-AWS-Secret-Access-Key",
            "region": "Your-ec2-instance-region",
            "instance": {
                "InstanceType": "t1.micro",
                "ImageId": "your-image-id",
                "SecurityGroups": [
                    "forward-proxy"
                ]
            }
        },
        ......
    }
}
```
### run scrapoxy daemon service
```
scrapoxy start /path/to/conf.json -d
```

## check scrapoxy proxy
```
scrapoxy test http://localhost:8888
```
or
```
curl --proxy http://127.0.0.1:8888 http://api.ipify.org
```

## access scrapoxy web GUI
<http://localhost:8889>

## configure scrapy
```
# append the following lines to settings.py

# PROXY
PROXY = 'http://127.0.0.1:8888/?noconnect'

# BLACKLISTING
BLACKLIST_HTTP_STATUS_CODES = [ 503 ]

# SCRAPOXY
API_SCRAPOXY = 'http://127.0.0.1:8889/api'
API_SCRAPOXY_PASSWORD = b'your-scrapoxy-commander-password'

DOWNLOADER_MIDDLEWARES = {
	'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None, # turn off the scrapy default http proxy
    'scrapoxy.downloadmiddlewares.proxy.ProxyMiddleware': 100, # load scrapoxy http proxy
    'scrapoxy.downloadmiddlewares.wait.WaitMiddleware': 101,
    'scrapoxy.downloadmiddlewares.scale.ScaleMiddleware': 102, # automate scale instance
    'scrapoxy.downloadmiddlewares.blacklist.BlacklistDownloaderMiddleware': 950, # when website access limit is reached, tell scrapoxyd change instance
}
```
