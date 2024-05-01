# Property-Analysis-Dashboard

*Please feel free to contact me if any questions appears: alexanderfrombrest@gmail.com*

### Objective:
Creation of end-to-end batch data pipeline and a dashboard for analysis of Polish real estate market based on https://www.otodom.pl/.

### Problem desciption:  
When preparing to buy a property, thorough analisys of market offers needs to be prepared.
Since there is huge amount of offers even for a singe borough of city, it is very heplfull to have a tool for mass analysis of offers, price per meter changes, general trends on markets.
As a data source the most popular property web page https://www.otodom.pl/ was chosen.
Since the API for that portal is available just for enterprices, a python web-scraper was created.

### Dataset:   

Dataset created by Python web scraper.

### Architecture 

![image](https://github.com/alexanderfrombrest/Property-Analysis-Dashboard/assets/64230396/c555c682-7039-491b-8b5a-3aa8a36d9a88)

### Technologies used:  

Cloud: GCP, dbt Cloud
Workflow orchestration: Mage
Data Warehouse: BigQuery
Visualization: Looker Studio

### Final result:  

https://lookerstudio.google.com/reporting/179c258a-7d7b-409e-8c25-171aa4f2edb4

Pie chart shows the distribution of ownership data, with "full ownership" being most popular category in offers.
Column chart shows the distribution of the price per square meter for primary and secondary markets over time.

![image](https://github.com/alexanderfrombrest/Property-Analysis-Dashboard/assets/64230396/0f671ee4-6a49-4ff6-a67c-ec605466571c)



