from bs4 import BeautifulSoup
import requests

def get_top_products():
    url = "https://www.producthunt.com"
    response = requests.get(url)
    # Fetching the content of the URL
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    product_div = soup.find('div', attrs={'data-test': 'homepage-section-0'})
    if not product_div:
        return None
    products = {}
    product_links = product_div.find_all('a')
    for link in product_links:
        is_post = link['href'].startswith('/post')
        text = link.get_text(strip=True)
        u = f"{url}{link['href']}"
        if is_post and text:
            try:
                products[u].append(text)
            except:
                products[u] = [text]
    return products


def format_url_and_values(dict_data):
    result = []                      
    for url, values in dict_data.items():
        formatted_values = ': '.join(values)
        result.append(f"[{formatted_values}]({url})")
    return result