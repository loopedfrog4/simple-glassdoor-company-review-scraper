#import the libraries
import os
import time

import numpy as np
import pandas as pd
import math

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

#create a function to scrape any Glassdoor company review page
#the code still works when I run it on 7 Sep, 2021, but the html content of Glassdoor webpages changes all the time
#please inspect the webpage and make the necessary changes to the html tags if any of the list returns empty
def review_scraper(url):
  #scraping the web page content
  hdr = {'User-Agent': 'Mozilla/5.0'}
  req = Request(url,headers=hdr)
  page = urlopen(req)
  soup = BeautifulSoup(page, "html.parser") 

  #define some lists
  Summary=[]
  Date_n_JobTitle=[]
  Date=[]
  JobTitle=[]
  OverallRating=[]
  Pros=[]
  Cons=[]  

  #get the Summary
  for x in soup.find_all('h2', {'class':'mb-xxsm'}):
    Summary.append(x.text)

  #get the Posted Date and Job Title
  for x in soup.find_all('span', {'class':'middle common__EiReviewDetailsStyle__newGrey'}):
    print(x)
    Date_n_JobTitle.append(x.text)

  #get the Posted Date
  for x in Date_n_JobTitle:
    Date.append(x.split(' -')[0])

  #get Job Title
  for x in Date_n_JobTitle:
    JobTitle.append(x.split(' -')[1])

  #get Overall Rating
  for x in soup.find_all('span', {'class':'ratingNumber'}):
    OverallRating.append(float(x.text))

  #get Pros
  for x in soup.find_all('span', {'data-test':'pros'}):
    Pros.append(x.text)

  #get Cons
  for x in soup.find_all('span', {'data-test':'cons'}):
    Cons.append(x.text)

  #putting everything together
  # Reviews = pd.DataFrame(list(zip(Summary, Date, OverallRating, Pros, Cons)), 
  #                        columns = ['Summary', 'Date', 'OverallRating', 'Pros', 'Cons'])

  data = {
    "Summary": Summary,
    "Job Title": JobTitle,
    "Date": Date,
    "Overall Rating": OverallRating,
    "Pros": Pros,
    "Cons": Cons
  }

  Reviews = pd.DataFrame(data)
  print(Reviews.to_string())
  
  return Reviews

#paste/replace the url to the first page of the company's Glassdoor review in between the ""
# input_url="https://www.glassdoor.sg/Reviews/Shopee-Reviews-E1263091" Shopee URL
# input_url="https://www.glassdoor.sg/Reviews/Lazada-Reviews-E578726" Lazada URL
input_url="https://www.glassdoor.sg/Reviews/Accenture-Reviews-E4138.htm"

# input_url+"_P"+str(x)+".htm?sort.sortType=RD&sort.ascending=false"

#scraping the first page content
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(input_url+"_P"+str(1)+".htm?sort.sortType=RD&sort.ascending=false",headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, "html.parser") 

#check the total number of reviews
# countReviews = soup.find('div', {'data-test':'pagination-footer-text'}).text
# countReviews = float(countReviews.split(' Reviews')[0].split('of ')[1].replace(',',''))
countReviews = 1000
print("Number of Reviews: ")
print(countReviews)

#calculate the max number of pages (assuming 10 reviews a page)
countPages = math.ceil(countReviews/10)
print("Number of pages: ")
print(countPages)

#I'm setting the max pages to scrape to 3 here to save time
# maxPage = 3 + 1
#uncomment the line below to set the max page to scrape (based on total number of reviews)
maxPage = countPages + 1
print("Number of pages to scrape: ")
print(maxPage)

# https://www.glassdoor.sg/Reviews/Amazon-Reviews-E6036_P2.htm?sort.sortType=RD&sort.ascending=false

#scraping multiple pages of company glassdoor review
output = []
output = review_scraper(input_url+"_P"+str(1)+".htm?sort.sortType=RD&sort.ascending=false")
for x in range(2,maxPage):
  url = input_url+"_P"+str(x)+".htm?sort.sortType=RD&sort.ascending=false"
  print("Current url:" + url + str(x))
  output = output.append(review_scraper(url), ignore_index=True)
  print(output)

#display the output
print(output.to_string())
output.to_csv("Accenture.csv", sep="\t")