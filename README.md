# LinkGrapher

LinkGrapher is a Python-based web crawler that traverses a given web page and constructs a link graph of the pages it finds. The crawler is implemented using the Scrapy framework and can be customized to handle different types of websites.

The LinkGrapher project also includes a Dockerfile and Docker Compose file for spinning up the scraper and Neo4j database together. This allows for easy deployment and management of the crawler and graph database.

The link graph data is stored in a Neo4j database, and pagerank is calculated using networkx Python library.

LinkGrapher can be used for a variety of purposes, such as analyzing website structures, identifying broken links, or discovering related content.

Feel free to fork and customize this project to suit your needs.

### Prerequisite:
* Install Docker
* Install Docker Compose

## Steps to run on local machine

1. Spin up the application stack

    ```bash
    $ docker compose up --build
    ```

    Wait for the spider to crawl all the pages and create the corresponding graph in the database.
    When the scraper completes the task you should see output as below:

    ![Screenshot of output](Output-Screenshot.png)

    Here we can see the page rank for each page.

2. Check the graph created

    1. Go to [Neo4J Browser](http://localhost:7474/browser/)

    2. Login with your credentials (If you haven't changed creds in docker-compose.yml, they are username: neo4j & passowrd: LdRQvvW8m7BQgq)

    3. Run the query:

    ```neo4j
    neo4j$ MATCH(n) RETURN n as node
    ```


Special Thanks to this [blog post](https://allendowney.github.io/DSIRP/pagerank.html).
