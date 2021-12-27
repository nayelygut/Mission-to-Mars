
# Import Splinter and Beautiful soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)
# set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p
# ### JPL Space Images Featured Image
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ### Mars Facts
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df
df.to_html()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres
# 1. Use browser to visit the URL
url = 'https://marshemispheres.com/'
browser.visit(url)
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
img_soup = soup(html, 'html.parser')
for i in range(4):
    hemispheres={}
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # Find image title
    img_elem = img_soup.select_one('div.collapsible.results')
    title = img_elem.find_all('h3')[i].text
    # Find the hemisphere link
    find_narrow = img_soup.select('div.description')[i]
    hem_url_rel = find_narrow.find_all('a', class_='itemLink product-item')[0].get('href')
    # Make full url
    hem_url = f'https://marshemispheres.com/{hem_url_rel}'
    # Visit the other link
    browser.visit(hem_url)
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # get the image link
    img_narrow = img_soup.select_one('div.wrapper')
    img_href = img_narrow.find('a', target='_blank').get('href')
    img_url = f'https://marshemispheres.com/{img_href}'
    # Add image and title pairs to dictionary
    hemispheres["image_url"]=img_url
    hemispheres["title"]=title
    hemisphere_image_urls.append(hemispheres)
    i += 1
    browser.back()
# 5. Quit the browser
browser.quit()

