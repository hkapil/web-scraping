#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import all dependencies
import time
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser

# Create global dictionary that can be imported into Mongo

mars_info = {}

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
# URL of page to be scraped
    browser = init_browser()

    nasa_url = 'https://mars.nasa.gov/news'


    # visit the NASA Mars News site and scrape headlines
    browser.visit(nasa_url)
    time.sleep(1)
    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, 'html.parser')

    news_list = nasa_soup.find('ul', class_='item_list')
    first_item = news_list.find('li', class_='slide')
    first_title= first_item.find('div', class_='content_title').text
    first_para = first_item.find('div', class_='article_teaser_body').text
   
    # Dictionary entry from MARS NEWS
    mars_info['news_title'] = first_title
    mars_info['news_paragraph'] = first_para


#JPL Mars Space Images - Featured Image

    jpl_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


    browser.visit(jpl_url)
    time.sleep(1)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

    featured_img = jpl_soup.find('img', class_='fancybox-image')['src']
    img_url = f'https://www.jpl.nasa.gov{featured_img}'
    
    mars_info['featured_image_url'] = img_url 


#Mars weather from twitter

    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'


    browser.visit(mars_weather_url)
    time.sleep(1)

    mars_weather_html = browser.html

    mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')

    mars_weather_text = mars_weather_soup.find('p',class_ ="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    mars_info['weather_text'] = mars_weather_text 

# Mars space facts  

    facts_url = 'http://space-facts.com/mars/'


    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)


    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()

    mars_info['mars_facts'] = data


# Mars Hemispheres  

    mars_hemi_url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)


    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        
    mars_info['hemispheres'] = hemisphere_image_urls

    return mars_info