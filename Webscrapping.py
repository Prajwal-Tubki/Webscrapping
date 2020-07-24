import requests
from bs4 import BeautifulSoup
import pandas

oyo_url = "https://www.oyorooms.com/hotels-in-bangalore//?page="

for page_num in range(1, page_num_MAX):
    req = requests.get(oyo_url+i)
    content = req.content

    soup=BeautifulSoup(content,"html.parser")

    all_hotels=soup.find_all("div" , {"class":"oyo-row"})
    scraped_info_list=[]

    for hotels in all_hotels:
        hotel_dict={}
        hotel_dict["address"]=hotels.find("div", {"class":"listingHotelDescription__hotelAddress"}).text
        try:
            hotel_dict["rating"]=hotels.find("div",{"itemprop":"aggregateRating"}).text
        except AttributeError:
            pass

        hotel_dict["price"]=hotels.find("div",{"class":"listingPrice"}).text

        parent_amenities_element=hotel.find("div", {"class":"amenityWrapper"})

        amenities_list=[]
        for amenities in parent_amenities_element.find_all("div", {"class":"amenityWrapper__amenity"}):
            amenities_list.append(amenities.find("span",{"class":"d-body-sm"})).text.strip()

        hotel_dict["amenities"]= ','.join(amenities_list[:-1])

        scrapped_info_list.append(hotel_dict)

        #print(hotel_address,hotel_rating,hotel_price)
dataFrame = pandas.Dataframe(scraped_info_list)
dataFrame.to_csv("Oyo.csv")
