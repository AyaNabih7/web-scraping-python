import scrap_jobes

fields = ['machine learning','data analysis','data science','business intelligence']
data = pd.DataFrame()
for field in fields:
    df = scrap_jobes.scrap(field)
    data = pd.concat([data, df])

scrap_jobes.save_as_csv(data)