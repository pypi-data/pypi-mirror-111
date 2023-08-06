import flask;from googlesearch import search;import requests
class metaserver():
	def __init__(self,**kwargs):
		try:
			port = int(kwargs["port"])
		except KeyError:
			port = 8000
		finally:
			ip = requests.get("https://api.ipify.org").content.decode();print(f"Hello there!\nYou launched meta search! \nIf you wonder where I can find my metasearch api end point just wait until your browser open \nand wait until you get lots of output! and that time is to refresh browser!\n Or if you want to access with public IP address you can go to https://{ip}:{port}");import webbrowser;webbrowser.open("http://localhost:{}".format(port));return self.run(int(port))
	app = flask.Flask("Meta Search")

	def run(self,port=80):
		self.app.run(host="0.0.0.0",port=port)
	@app.route('/',methods=["POST","GET"])
	async def main():
		info = ""
		for x in flask.request.headers:
			info += f"{x}\n"
		print("Info of client:\n{}".format(info))
		try:
			query = flask.request.headers.get("search")
			if query == None:
				return {"Result":[None]},400
		except KeyError:
			return {"Result":[None]},400
		else:
			result = search(query,num_results=10000);return {"Result":True,"Query":result,"Advertising":"Thank you for using metasearch! Please visit https://github.com/dumb-stuff/Meta-search for github repository and https://pypi.org/project/metasearch !"},202 # Modify num_results to be what the heck ever you want
print("Default port is 8000 for work fine on every oses. You can modify at start of server by do \nmetaserver(port=your port can be string or integer)")