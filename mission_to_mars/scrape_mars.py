from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import time
from pprint import pprint
import datetime as dt

# define function to execute chromedriver from where it is stored on my computer
def browser_init():
    executable_path = {'executable_path': 'C:\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

# define function that will be activated by the button press, and will perform all the scraping functions
# part 1: Get the title and the body for the first news article of nasa website.
# part 2: Get featured image of NASA website.
# part 3: Get first tweet about mars (from mars wx report) on twitter
# part 4: Take all 4 images and titles from usds website


def scraper():

    #EVerything we scrape goes into a dict so Flask can access it.
    mars_info_dict=dict()
    
    #1a: Specify URL, and send chrome browser there
    try:
        url = 'https://mars.nasa.gov/news/'
        browser = browser_init()
        browser.visit(url_1)
        time.sleep(2)
        html = browser.html
        
        #1b: Scrape the html, and beautifulsoup to parse the name and body from it.
        soup = BeautifulSoup(html, 'html.parser')
        soup_chunk_1 = soup.select_one('ul.item_list li.slide')
        news_title = soup_chunk_1.find("div", class_='content_title').get_text()
        news_body = soup_chunk_1.find("div", class_='article_teaser_body').get_text()
        # print(news_title)
        # print(news_para)

        mars_info_dict['result_title'] = news_title
        mars_info_dict['result_para] = news_para
        # pprint(mars_info_dict)
    except:
        print("Some issue")


    # ----------------------------------------------

    featured_url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_url_2)

    first_click = browser.find_by_id('full_image')
    first_click.click()
    time.sleep(2)

    second_click = browser.find_link_by_partial_text('more info')
    second_click.click()
    time.sleep(2)

    html_2 = browser.html
    soup_2 = BeautifulSoup(html_2, 'html.parser')

    partial_url = soup_2.select_one('figure.lede a img').get('src')
    #print(partial_url)

    full_url = f'https://www.jpl.nasa.gov{partial_url}'
    mars_info_dict['featured_image_url'] = full_url
    # pprint(mars_info_dict)
    # -----------------------------------------------


    weather_url_3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html_3 = browser.html
    soup_3 = BeautifulSoup(html_3, 'html.parser')
    mars_weather_tweet = soup_3.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    mars_weather_tweet
    mars_weather_tweet_text = mars_weather_tweet.find('p', 'tweet-text').get_text()
    mars_info_dict['mars_weather'] = mars_weather_tweet_text.rsplit(" ", 1)[0] + "hpa"
    # pprint(mars_info_dict)

    # ---------------------------------------

    tables = pd.read_html('http://space-facts.com/mars/')
    table_df = tables[0]
    table_df.columns = ['Parameter','Mars', 'Earth']
    table_df.to_html('mars_facts.html', index=False)
    table_df.set_index('Parameter')
    html_table = table_df.to_html(classes="table table-striped")
    #print(html_table)

    # ----------------------------------------------

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    html_hemisphere = browser.html
    soup_hemisphere = BeautifulSoup(html_hemisphere , 'html.parser')


    links = browser.find_by_css("a.product-item h3")
    hemisphere_image_urls = []

    for i in range(len(links)):
        hemisphere = {}

    # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()

    # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']

    # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text

    # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)

    # Finally, we navigate backwards
        browser.back()

        hemisphere_image_urls


    mars_info_dict['hemisphere_image_urls'] = hemisphere_image_urls
    # pprint(mars_info_dict)

    cur_datetime = dt.datetime.utcnow()
    print(cur_datetime)
    mars_info_dict["Date_time"] = cur_datetime
    # pprint(mars_info_dict)

    # print("just before final return of mars_info_dict")

    mars_return_dict =  {
        "News_Title": mars_info_dict["result_title"],
        "News_Summary" :mars_info_dict["result_body"],
        "Featured_Image" : mars_info_dict["featured_image_url"],
        "Weather_Tweet" : mars_info_dict["mars_weather"],
        "Facts" : html_table,
        "Hemisphere_Image_urls": hemisphere_image_urls,
        "Date" : mars_info_dict["Date_time"]
    }

    #print(mars_return_dict)

    return mars_return_dict


# test_result = scraper()
# print(test_result)