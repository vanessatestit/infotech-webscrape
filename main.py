import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


# Step 1: Fetch the page source
url = 'https://www.infotech.com.hk/itjs/job/fe-search.do?method=feList&sortByField=jjm_activedate&sortByOrder=DESC'
response = requests.get(url)
html_content = response.text

# Step 2: Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')
#print(soup.prettify())

# Step 3: Find all tr elements with multiple class names
elements = soup.find_all(class_=['row1', 'row2'])
count=len(elements)

# Step 4: Extract and print job details
#element_list=[]
df_rows=[]

for element in range(count):
  #element_list.append(elements[element].text.strip().split('\n'))
  df_row=[
    elements[element].text.strip().split('\n')[0], #Key
    elements[element].text.strip().split('\n')[1], #Order Location
    elements[element].text.strip().split('\n')[2], #Job Title/ Category
    "https://www.infotech.com.hk/itjs/job/fe-view.do?method=feView&jjKey="+str(elements[element].text.strip().split('\n')[0][2:]),#Job Hyperlink
    elements[element].text.strip().split('\n')[3], #No of Vacancy
    elements[element].text.strip().split('\n')[4], #Monthly Salary
    elements[element].text.strip().split('\n')[5], #Business
    elements[element].text.strip().split('\n')[6], #Post-quali Exp Yr
    elements[element].text.strip().split('\n')[7], #Published Requirements
    elements[element].text.strip().split('\n')[9] #Last Update
  ]
  df_rows.append(df_row)

df=pd.DataFrame(df_rows, columns=['Key','Order Location','Job Title/ Category','Hyperlink','No of Vacancy','Monthly Salary','Business','Post-quali Exp Yr','Published Requirements','Last Update'])

# Step 5: Filter the dataframe by Last Update > 4 days ago
df['Last Update'] = pd.to_datetime(df['Last Update'], format='%d %b %Y')
four_days_ago = datetime.now() - timedelta(days=4)
#formatted_four_days_ago = pd.to_datetime(four_days_ago.strftime('%d %b %Y'))
filtered_df = df[df['Last Update'] > four_days_ago]

# Step 6: Convert the DataFrame to HTML
html_table = filtered_df.to_html(index=False)

# Step 7: Set up email parameters
from_email = 'vanessachan301@gmail.com'
to_emails = ['vanessachan301@gmail.com','loyu20500@gmail.com']
today = pd.to_datetime(datetime.now().strftime('%d %b %Y'))
formatted_today = today.strftime('%Y-%m-%d')
subject = f"{formatted_today} Infotech IT Job List"
body = f"<h1>Infotech Latest IT Jobs</h1>{html_table}"

# Step 8: Create the email
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = ', '.join(to_emails)  # Join the list of emails into a string #to_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'html'))

# Step 4: Send the email
try:
    # Set up the server
    server = smtplib.SMTP('smtp.gmail.com', 587)  # Use Gmail's SMTP server
    server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
    server.login(from_email, 'eqso hgov kgmk mzgd')  # Use your password or App Password
    server.send_message(msg)  # Send the email
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    server.quit()  # Close the connection
