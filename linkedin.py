import requests
import bs4

url = "https://www.linkedin.com/in/hutton-henry/"

page = requests.get(url)
soup = bs4.BeautifulSoup(page.content, "html.parser")

# Scrape the name
name = soup.find("li", class_="inline t-24 t-black t-normal break-words").get_text()
print("Name:", name)

# Scrape the job title
job_title = soup.find("h2", class_="mt1 t-18 t-black t-normal").get_text()
print("Job Title:", job_title)

# Scrape the company name
company = soup.find("span", class_="text-align-left ml2 t-14 t-black t-normal").get_text()
print("Company:", company)

# Scrape the location
location = soup.find("span", class_="t-16 t-black t-normal inline-block").get_text()
print("Location:", location)