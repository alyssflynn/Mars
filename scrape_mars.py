import os
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
import splinter
from splinter import Browser

def scrape():
    # -------------------------------------
    # Dict for storing new mars data
    mars_data = {}

    # -------------------------------------
    # Setup browser
    executable_path = {'executable_path': './chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # -------------------------------------
    # Scrape nasa news site
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)

    html = browser.html
    soup = bs(html, "html.parser")
    
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="rollover_description_inner").text
    
    mars_data["news_title"] = news_title
    mars_data["news_summary"] = news_p
    
    # -------------------------------------
    # JPL featured image
    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)

    browser.find_by_id("full_image").click()
    browser.is_element_present_by_text("more info", wait_time=5)
    browser.click_link_by_partial_text("more info")

    html = browser.html
    soup = bs(html, "html.parser")

    # Get image source
    img_desc = soup.find("img", class_="main_image").get("title")
    img_src = soup.find("img", class_="main_image").get("src")
    featured_image_url = "https://jpl.nasa.gov" + img_src
    
    mars_data["featured_image_desc"] = img_desc
    mars_data["featured_image"] = featured_image_url
    
    # -------------------------------------
    # Scrape twitter for Mars weather
    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)
    
    html = browser.html
    soup = bs(html, "html.parser")

    latest_tweet = soup.find("div", class_="js-tweet-text-container").text
    mars_data["weather"] = latest_tweet.strip()
    
    # -------------------------------------
    # Mars facts table
    url_facts = "https://space-facts.com/mars/"
    browser.visit(url_facts)

    html = browser.html
    soup = bs(html, "html.parser")

    table = soup.find("table", {"class": "tablepress tablepress-id-mars"}).find_all("tr")

    facts = {}
    for row in table:
        key, value = row.text.strip().split(':')
        facts[key] = value

    # mars_data["facts_table"] = table
    mars_data["facts_dict"] = facts
    
    # -------------------------------------
    # Mars Hemispheres
    url_hemis = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemis)

    html =  browser.html
    soup = bs(html, 'html.parser')

    results = soup.find("div", {"class": "collapsible results"})
    hemispheres = results.find_all("div", {"class": "description"})

    hemisphere_imgs = {}
    for hemi in hemispheres:
        name = hemi.a.h3.text.replace("Enhanced", "").strip()
        img_url = "https://astrogeology.usgs.gov" + hemi.a['href']
        hemisphere_imgs[name] = img_url
     
    mars_data["hemispheres"] = hemisphere_imgs    
    
    # -------------------------------------
    browser.quit()
    return mars_data
