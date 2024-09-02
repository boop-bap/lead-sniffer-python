<img src="https://schertzanimalhospital.com/wp-content/uploads/2018/03/Schertz_iStock-836716796_medium-1024x639.jpg" alt="Logo of the project" align="right">

# Lead Sniffer

A tool to analyze websites for specific business details like catalogs, business type, and model. It's useful for sniffing out potential clients. First, it browses the provided URLs with the given criteria and returns a detailed description of each site. Then, it analyzes the description text to see if it meets the criteria and provides the results in the specified format.

## Installing / Getting started with docker

```shell
create your own .env file in root with your OPENAI_API_KEY and PORT
```

```shell
sudo docker build -t yourbuildname .
```

```shell
sudo docker run -p 3000:3000 --name yourcontainername --env-file .env yourbuildname
```


## Things to consider

This is the backend for handling provided XLSX files with "Website URL" and "Record ID" as required headers for my use case, since HubSpot exports them that way.

The information is returned in XLSX format.

## Headers added on output 

    model: Literal["Retail", "E-commerce", "Both e-commerce and physical stores", "Physical stores"]
    monthly_or_more_often_published_catalogs: Literal["Yes", "No", "Maybe", "Not sure"]
    type: Literal["B2B", "B2C", "Both B2B and B2C", "Agency"]
    online: Literal["Yes", "No"]

