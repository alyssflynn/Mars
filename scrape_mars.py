import os
import time
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import splinter
from splinter import Browser
import tweepy
# from config import consumer_key, consumer_secret, access_token, access_token_secret


def scrape():
    executable_path = {'executable_path': '/Users/alyss/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    mars_data = {}
    
    # Scrape nasa news site
    browser.visit("https://mars.nasa.gov/news/")
    html = browser.html
    soup = bs(html, "html.parser")
    
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="rollover_description_inner").text
    
    mars_data["Mars_news_title"] = news_title
    mars_data["Mars_news_summary"] = news_p
    
    # JPL featured image
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    browser.find_by_id("full_image").click()
    browser.is_element_present_by_text("more info", wait_time=1)
    
    html = browser.html
    soup = bs(html, "html.parser")
    img = soup.select_one("img").get("src")
    featured_image_url = "https://jpl.nasa.gov" + img
    
    mars_data["Mars_featured_image"] = featured_image_url
    
    ### Scrape twitter for Mars weather
    # Tweepy API Authentication
    browser.visit("https://twitter.com/marswxreport?lang=en")
    
    html = browser.html
    soup = bs(html, "html.parser")
    latest_tweet = soup.find("div", class_="js-tweet-text-container").text
    
    mars_data["Mars_weather"] = latest_tweet
    
    ### Mars facts
    url_mars_facts = "https://space-facts.com/mars/"
    browser.visit("https://space-facts.com/mars/")
    
    # get table
    facts_table = pd.read_html(url_mars_facts)
    mars_facts_df = facts_table[0]
    mars_facts_df.columns = ["description", "value"]
    #mars_facts_df.select_index("description")
    print(mars_facts_df)
    
    # convert df to html
    mars_html_table = mars_facts_df.to_html(classes="table")
    mars_table = mars_html_table.replace('\n', ' ')
    mars_data["Mars_facts"] = mars_table
    print(mars_data)
    
    ### Mars Hemispheres
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    html =  browser.html
    soup = bs(html, 'html.parser')
    
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"},
    ]
    
    #for i in range(len(hemisphere_image_urls)):
        #time.sleep(5)
        #pass
    
    mars_data['Mars_hemispheres'] = hemisphere_image_urls
    
    browser.quit()
    return mars_data