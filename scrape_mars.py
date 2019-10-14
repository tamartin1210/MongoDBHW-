from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_p= mars_news(browser)
    results = {
        "title": news_title, 
        "paragraph": news_p,
        "image_url": image(browser),
        "weather": mars_weather(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemisphere(browser),

    }
    browser.quit()
    print(results)
    return results

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    mars_news_soup = bs(html, 'html.parser')

    # Scrape the first article title and teaser paragraph text; return them
    title = mars_news_soup.find('div', {"class":"content_title"})
    news_title = title.text.strip()
    #print(news_title)
    paragraph = mars_news_soup.find('div', {'class':'article_teaser_body'})
    news_p = paragraph.string.strip()
    #print(news_p)
    return news_title, news_p

def image(browser):
    img_url = 'https://www.jpl.nasa.gov/spaceimages/'
    browser.visit(img_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    expand = browser.find_by_css('a.fancybox-expand')
    expand.click()
    html = browser.html
    soup = bs(html, 'html.parser')
    img = soup.find('img', class_='fancybox-image')['src']
    # pass the path so i can see the actual image 
    featured_image_url = f'https://www.jpl.nasa.gov{img}'
    return featured_image_url

def mars_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    tweet_soup = bs(html, 'html.parser')
    
    # Scrape the tweet info and return
    first_tweet = tweet_soup.find('p', class_='TweetTextSize').text
    return first_tweet
    
def mars_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    #df.columns = ['Element', 'Facts']
     # Convert to HTML table string and return
    return df.to_html()
    
def mars_hemisphere(browser):
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hem_dict = []
    for i in range(1,9,2):
        hemi_dict = {}
        browser.visit(hemisphere_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        links = soup.findAll('a', class_='product-item')
        hemi_name = links[i].text
        #print(hemi_name)
        link_detail = browser.find_by_css('a.product-item')
        link_detail[i].click()
        browser.find_link_by_text('Sample').first.click()
        browser.windows.current = browser.windows[-1]
        html2 = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
        img_soup = bs(html2, 'html.parser')
        img_path = img_soup.find('img')['src']
        
        
        hemi_dict['title'] = hemi_name.strip('Enhanced')
        hemi_dict['img_url'] = img_path
        
        hem_dict.append(hemi_dict)
        #print(results)
    return hem_dict
scrape()