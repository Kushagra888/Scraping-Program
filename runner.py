import scrapy
import csv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Products.spiders.Amazon import AmazonSpider

f = open('Input_Amazon.csv', 'r')
read = csv.DictReader(f, delimiter = ',')

p_names = []
low_prs = []
high_prs = []
brands = []
p_cons = []
p_fltrs = []

for col in read:
    nm = col.get('product_name')
    if nm == '':
        nm = None
    p_names.append(nm)

    lp = col.get('low_price')
    if lp == '':
        lp = None
    low_prs.append(lp)

    hp = col.get('high_price')
    if hp == '':
        hp = None
    high_prs.append(hp)

    bn = col.get('brand_name')
    if bn == '':
        bn = None
    brands.append(bn)

    cn = col.get('condition')
    if cn == '':
        cn = None
    p_cons.append(cn)

    pf = col.get('product_filter')
    if pf == '':
        pf = None
    p_fltrs.append(pf)

process = CrawlerProcess(settings=get_project_settings())

#create log files append only
#create a new file for each day

process.crawl(AmazonSpider, product_names=p_names, low_prices=low_prs, high_prices=high_prs, brand_names=brands, conditions=p_cons, product_filters=p_fltrs)
process.start()

f.close()

#try..catch block
# Write a program to read input from text file or database.
# input example: seach criteria, price range, brand name, new/used, customer rating, [website name] for scraping.
# how many pages we need to scrape
# store Output in the database or CSV file
# date and time when scraping has run, machine name where it was run, Product Name, Product price, URL, seller name (Amazon, flipcart, or third party), images.
# ML
# Build ML model using relevency alogorithm to get the best match.
