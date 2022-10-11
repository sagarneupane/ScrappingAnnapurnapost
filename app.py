
import requests 
from os.path import exists as file_exists


def create_names(search_data):
    error_file_name = f"{search_data}_error_page.txt"
    data_file_name = f"{search_data}.json"
    
    return error_file_name, data_file_name

# Creating unique file name according to search result.
# this is the file where the pages with error are stored.
# error_file_name =  f"{search_data}_error_page.txt"


# Checking if the file with error exists. 
# If it is first time or a new search query the file is not created so checking 
# this will take as if there are no error pages

def read_error_page(error_file_name):
    error_pages_list = []
    if file_exists(error_file_name):

        with open(error_file_name, "r+", encoding="utf-8") as f:
            datas = f.read()
            print(datas)
            for data in datas:
                error_pages_list.append(int(data))
    return error_pages_list


# Into The page changes. The given loop will go upto 1-10 pages.
def search_data_from_url(search_data,error_pages_list):
    articles = {
    }
    for i in range(1,11):

        payload = {
            "title":search_data,
            "page":i
        }
        # Checking if the page number exists in the error_pages list.
        # If it exists it means the search page has some errors so ignoring that 
        # If it doesnot then keep on scrapping the data
        if i not in error_pages_list:
            r = requests.get("https://bg.annapurnapost.com/api/search", params=payload)
            print("visited")
            if r.status_code == 200:
                data = r.json()
                for item in data['data']['items']:
                    key_name = f"article_{item['id']}"
                    articles[key_name] = {
                        "title":item["title"],
                        "author":item["author"],
                        "content":item["content"],
                    }

            else:
                error_pages_list.append(i)
                break
    
    return error_pages_list, articles


# # Giving the file name to store the scrap data.
# file_name = f"{search_data}.json"


# Writing the error page value into the file so that next time we can ignore that page
def create_error_file(error_file_name, error_pages_list):
    with open(error_file_name, "w+") as f:
        for data in error_pages_list:
            f.write(str(data))


# Writing the scrapped data which was in form of dictonary into a json file.

def create_json_data(file_name,articles):
    with open(file_name, "w+", encoding="utf-8") as f:
        import json
        data = json.dumps(articles, indent=4, ensure_ascii=False)
        f.writelines(data)


#Scrap Data 

# search_data = "नेपाली"
# search_data = "दैलेख"
search_data = "नेपालि"
# search_data = "मरभुमि"


error_file_name, data_file_name = create_names(search_data)

error_pages_list = read_error_page(error_file_name)

updated_error_pages , data_to_store = search_data_from_url(search_data,error_pages_list)

create_error_file(error_file_name,updated_error_pages)
# print(data_to_store)
create_json_data(data_file_name,data_to_store)