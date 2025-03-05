import requests
from concurrent.futures import ThreadPoolExecutor

def load_proxies(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def check_proxy(proxy):
    try:
        ip, port, login, password = proxy.split(':')
        proxy_url = f'http://{login}:{password}@{ip}:{port}'
        proxies = {"http": proxy_url, "https": proxy_url}
        response = requests.get("http://ip-api.com/json", proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"Рабочий прокси: {proxy}")
            return proxy
    except Exception as e:
        pass
    return None

def save_good_proxies(proxies, filename):
    with open(filename, 'w') as f:
        for proxy in proxies:
            f.write(proxy + '\n')

def main():
    proxies = load_proxies("proxy.txt")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        good_proxies = list(filter(None, executor.map(check_proxy, proxies)))
    
    save_good_proxies(good_proxies, "good_proxy.txt")
    print(f"Проверка завершена. Рабочих прокси: {len(good_proxies)}")

if __name__ == "__main__":
    main()
