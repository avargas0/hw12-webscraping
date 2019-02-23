
#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
import time
import datetime
import re

def init_browser():
        executable_path = {'executable_path': 'chromedriver.exe'}
        return Browser('chrome', **executable_path, headless=False)

def mars_scrape():
        #Create empty dictionary
        mars_dict=dict()

        #NASA Mars News    
        url='https://mars.nasa.gov/news/'
        browser = init_browser()
        browser.visit(url)
        html=browser.html

        #Create BeautifulSoup object; parse with 'html.parser'
        soup=BeautifulSoup(html, 'html.parser')
        #print(soup.prettify())

        #JPL Featured Image 
        img_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(img_url)
        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(5)
        browser.click_link_by_partial_text('more info')

        #Pull the latest news article
        news_slide = soup.select_one('ul.item_list li.slide')

        #Get latest news article title
        news_title = news_slide.find("div", class_='content_title').get_text()
        print('News title is ' + news_title)

        #Get latest news article paragraph
        news_p= news_slide.find('div', class_="article_teaser_body").get_text()
        print('The news paragraph is ' + news_p)


        #Find the image URL for the current Featured Mars Image
        html=browser.html
        soup_img=BeautifulSoup(html,'html.parser')
        fig=soup_img.find('figure', class_='lede')
        partial_img=fig.find('a')['href']
        featured_image_url = 'https://www.jpl.nasa.gov' + partial_img
        print(featured_image_url)
        browser.quit()

        #Add Mars news title, paragraph, and image URL to dictionary
        from pprint import pprint
        mars_dict['Mars News Title']=news_title
        mars_dict['Mars News Paragraph']=news_p
        mars_dict['Mars Featured Image (URL)']=featured_image_url
        pprint(mars_dict)


        #Mars Wather
        #Visit Twitter; scrape latest Mars weather tweet
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)

        weather_url='https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)
        html=browser.html
        soup_weather=BeautifulSoup(html, 'html.parser')

        #Save tweet to variable, print
        mars_weather=soup_weather.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
        mars_weather

        #Add to Mars dictionary
        mars_dict['Mars Weather']=mars_weather
        pprint(mars_dict)

        #Visit Mars Facts site; scrape the table containing facts
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)

        facts_url='http://space-facts.com/mars/'
        marsFacts_df=pd.read_html(facts_url)
        marsFacts_df=marsFacts_df[0]
        #marsFacts_df

        #Rename columns
        marsFacts_df.columns = ['Mars Facts', 'Values']

        #Use Pandas to convert data to HTML table string
        marsFacts_df.to_html('mars_facts.html', index=False)

        ##Reset index
        marsFacts_df.set_index('Mars Facts')

        #New HTML version of Mars facts table
        marsFacts_html = marsFacts_df.to_html(classes='mars_facts table table-striped')

        #Add to Mars dictionary
        mars_dict['Mars Facts Table ']=marsFacts_html
        pprint(mars_dict)

        #Obtain hi-res images for each of Mars' hemispheres
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)

        hems_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

        browser.visit(hems_url)
        time.sleep(5)
        html=browser.html
        soup_hems=BeautifulSoup(html,'html.parser')

        #Parse soup object to get images of hemispheres 
        class_collapse=soup_hems.find('div', class_='collapsible results')
        images=class_collapse.find_all('div', class_='item')

        #Loop to find title & image URLs
        hem_urls=list()
        img_urls=list()
        titles=list()

        for image in images:
                hem_title=image.h3.text
                titles.append(hem_title)

                image_href='https://astrogeology.usgs.gov'+image.find('a', class_='itemLink product-item')['href']

                browser.visit(image_href)
                time.sleep(5)
                html=browser.html
                soup_hems_img=BeautifulSoup(html, 'html.parser')
                hem_img_url=soup_hems_img.find('div', class_='downloads').find('li').a['href']
                #print('Hem Image URL: '+ hem_img_url)
                img_urls.append(hem_img_url)

                #Create dictionary
                hems_dict=dict()
                hems_dict['title']=hem_title
                hems_dict['img_url']=hem_img_url
                hem_urls.append(hems_dict)

        #Print lists
        print(hem_urls)
        print(img_urls)
        print(titles)

        #Add to Mars dictionary
        mars_dict['Mars Hemisphere Image URLs']=hem_urls
        pprint(mars_dict)

        #Print complete Mars dictionary
        print('Mars dictionary')
        mars_dict = {
                'Mars News Title': news_title,
                'Mars News Paragraph': news_p,
                'Mars Featured Image (URL)': featured_image_url,
                'Mars Weather': mars_weather,
                'Mars Facts Table': marsFacts_html,
                'Mars Hemisphere Image URLs': img_urls,
                }
        return mars_dict

#mars_scrape()

