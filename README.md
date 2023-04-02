# LinkGrapher

LinkGrapher is a Python-based web crawler that traverses a given web page and constructs a link graph of the pages it finds. The crawler is implemented using the Scrapy framework and can be customized to handle different types of websites.

The LinkGrapher project also includes a Dockerfile and Docker Compose file for spinning up the scraper and Neo4j database together. This allows for easy deployment and management of the crawler and graph database.

The link graph data is stored in a Neo4j database, and pagerank can be calculated using either the Neo4j graph algorithms library or a custom Python implementation.

LinkGrapher can be used for a variety of purposes, such as analyzing website structures, identifying broken links, or discovering related content.

Feel free to fork and customize this project to suit your needs.
