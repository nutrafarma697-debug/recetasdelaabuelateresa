import urllib.request
import re

url = 'https://streamable.com/qzoxer'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'"(https://[A-Za-z0-9\-\.]+\.streamable\.com/video/[^"]+)"', html)
    
    if match:
        video_url = match.group(1).replace('&amp;', '&')
        print("Found URL:", video_url)
        print("Downloading...")
        urllib.request.urlretrieve(video_url, "video.mp4")
        print("Download complete: video.mp4")
    else:
        # Another pattern common in streamable: meta property og:video:url
        match2 = re.search(r'property="og:video:url"\s+content="([^"]+)"', html)
        if match2:
            video_url = match2.group(1).replace('&amp;', '&')
            print("Found URL via OG:", video_url)
            print("Downloading...")
            urllib.request.urlretrieve(video_url, "video.mp4")
            print("Download complete: video.mp4")
        else:
            print("No video URL found in HTML.")
except Exception as e:
    print("Error:", e)
