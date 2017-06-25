import feedparser
import os
import requests
import sys

def main():

	# Parameters

	rss_url = "http://umd.hosted.panopto.com/Panopto/Podcast/Podcast.ashx?courseid=e8a1cdd7-d37f-4dc3-8d18-a4933fb37780&type=mp4"
	download_folder = "C:/Users/Siddhartha Harmalkar/Videos/panopto_downloads"
	print_info = True

	# Get feed from URL

	feed = feedparser.parse(rss_url)

	if(feed["bozo"]):
		print("Error: Feed data isn't a well-formatted XML. Check URL")
		return

	if(print_info):
		print(get_info(feed))
		print("Items: ")
		print(get_items(feed))

	download_folder += "/" + feed["channel"]["title"].replace(":", "")

	if not os.path.exists(download_folder):
		print("Creating directory '" + download_folder + "\'")
		os.makedirs(download_folder)
	else:
		print("Saving to directory '" + download_folder + "\'")

	for i, item in enumerate(feed["items"]):
		file_name = download_folder + "/" + repr(i+1) + ". " + item["title"].replace(":","") + " (" + item["published"].replace(":",".") + ")" + ".mp4"
		print(file_name)
		with open(file_name, "wb") as f:
			print("Downloading '" + item["title"] + "' to: " + file_name)
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
					sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
					sys.stdout.flush()

def get_info(feed):
	return "Title: '" + feed["channel"]["title"] + "'\nDescription: '" + feed["channel"]["description"] + "'"

def get_items(feed):
	return "\n".join(["\t-" + item["summary"] for item in feed["items"]])

if __name__ == "__main__":
	main()