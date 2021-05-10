# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    hemispheres_data = scrape_hemi_imgs(browser)
    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now(),
          "hemispheres": hemispheres_data,
    }

    #Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url= 'https://redplanetscience.com'
    browser.visit(url)

    #Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    #Begin scrape:
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_= 'article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images

def featured_image(browser):
    #Script to gather images
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #Parse the reulting html with soup
    html= browser.html
    img_soup = soup(html, 'html.parser')

    try:
        #Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ### Table facts
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html(classes = "table table-striped")

#Challenge code: Scrape Full Res Mars Hemisphere imgs
def scrape_hemi_imgs(browser):
    # Use browser to visit the URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    linked = browser.links.find_by_partial_text('Enhanced')
    hemisphere_urls = [link['href'] for link in linked]

    for link in hemisphere_urls:
        browser.visit(link)
        html= browser.html
        hemi_soup = soup(html, 'html.parser')
        #make temp dict
        temp = {}
        #get pic url
        sample_href = hemi_soup.find('div', class_='downloads').find('ul').find('li').find('a')['href']
        temp['img_url'] = f'https://marshemispheres.com/{sample_href}'
        #get hermisphere title
        hemi_name = hemi_soup.find('h2', class_='title').text
        temp['title'] = hemi_name
        #append to list
        hemisphere_image_urls.append(temp)

    # Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls


if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())
