#%%
import requests
#%%
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Cookie': 'bblastvisit=1691629747; bblastactivity=0; bbuserid=70435; bbpassword=e3568aa461353bc9fbe451fbf728b7ae; _ga=GA1.1.185467891.1691629758; _ga_96WY22B0PN=GS1.1.1705402447.36.1.1705403580.10.0.0; __gads=ID=2e0a7b0d6b8dd2b5:T=1691629774:RT=1705402996:S=ALNI_MaxYR18Pmhx3KA9AZkU0wMxBRfBNw; __gpi=UID=00000c29df4c9c71:T=1691629774:RT=1705402996:S=ALNI_MZ7fi_fLZ8fSatF2NW17SzZFEDM3g; uuid=8297300f-19a9-4e14-a3b8-c889cb6f609a; cf_clearance=P2b6ZmCxp862pR95ZiVOINCk.VqBEDCBF.gfpL0v894-1705330568-1-AdaIlvYc4I54B2GT5DnfYoPI2LyIvqvX1MDCA69/YLLVc4HDfg0ylZDhWdBP+k48l5ioSwNyyELJvmBLAMP5VQU=; _gcl_au=1.1.833134077.1699756130; bbsessionhash=5387e29b64e2edbbffa7f06b54950eb3; vbseo_loggedin=yes'
    }
folder = "C:/Users/pt88/Documents/NinjaTrader 8/db/replay/"
count = 1
for i in range(2238, 2243):
    url = f"https://nexusfi.com/local_links.php?action=jump&catid=28&id={i}"
    response = requests.get(url, headers=HEADERS)

    print(response.ok)
    print(response.status_code)
    filepath = folder + f"ES 06-20.7z.00{count}"
    count += 1

    with open(filepath, mode="wb") as f:
        f.write(response.content)
