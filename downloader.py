import feedparser
import os
import requests
import sys

def main():

	# Parameters

	#rss_url = "http://umd.hosted.panopto.com/Panopto/Podcast/Podcast.ashx?courseid=e8a1cdd7-d37f-4dc3-8d18-a4933fb37780&type=mp4"
	#download_folder = "C:/Users/Siddhartha Harmalkar/Videos"
	print_info = True

	# Take input from user

	rss_url = input("RSS Feed URL: ")

	# Get feed from URL

	feed = feedparser.parse(rss_url)

	if(feed["bozo"]):
		print("Error: Feed data isn't a well-formatted XML. Check URL")
		return

	if(print_info):
		print(get_info(feed))
		print("Items: ")
		print(get_items(feed))

	start = int(input("Enter video number to start at: "))
	end = int(input("Enter video number to end at: "))

	download_folder = input("Download Folder: ") + "/panopto_downloads/" + feed["channel"]["title"].replace(":", "")

	if not os.path.exists(download_folder):
		print("Creating directory '" + download_folder + "\'")
		os.makedirs(download_folder)
	else:
		print("Saving to directory '" + download_folder + "\'")

	for i, item in enumerate(feed["items"]):
		if i >= start-1 and i <= end-1:
			file_name = download_folder + "/" + repr(i+1) + ". " + item["title"].replace(":","").replace("?","") + " (" + item["published"].replace(":",".") + ")" + ".mp4"
			with open(file_name, "wb") as f:
				response = requests.get(item["link"], stream=True)
				total_length = response.headers.get('content-length')

				if total_length is None: # no content length header
					f.write(response.content)
				else:
					dl = 0
					total_length = int(total_length)
					for data in response.iter_content(chunk_size=4096):
						dl += len(data)
						f.write(data)
						done = int(50 * dl / total_length)
						sys.stdout.write("\r %s [%s%s] [%d/%d] (%f%%)" % (item["title"], '=' * done, ' ' * (50-done), dl, total_length, dl/total_length*100) )    
						sys.stdout.flush()
					sys.stdout.write("\n")

def get_info(feed):
	return "Title: '" + feed["channel"]["title"] + "'\nDescription: '" + feed["channel"]["description"] + "'"

def get_items(feed):
	return "\n".join(["\t-" + repr(i+1) + ". " + item["summary"] for i, item in enumerate(feed["items"])])

if __name__ == "__main__":
	main()