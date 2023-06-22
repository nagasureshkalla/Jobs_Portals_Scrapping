
import requests



# url = 'https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}'
url = 'https://api.telegram.org/bot--APIKEY--/sendMessage?chat_id=@daily_nagu_jobs&text=Hello from Suresh'


x = requests.post(url)

print(x.text)

