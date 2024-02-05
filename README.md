# Data Engineering Track - Overview of the project and its purpose
Our project revolves around providing valuable insights into vehicle safety. We aggregate and analyze complaint data from the National Highway Traffic Safety Administration (NHTSA) database, aiming to empower consumers, researchers, and policymakers with comprehensive information about vehicle safety issues.

We employed covert web scraping techniques to extract safety rating data from NHTSA's web pages, revealing insights for a wide range of vehicle models. The extracted data, including safety ratings and complaints, is stored in an SQLite database. SQLite, chosen for its simplicity and seamless integration with Python, provides an efficient solution for storing and retrieving safety-related data.In addition to the core functionalities of our project, we've integrated a robust data visualization component to enhance the user experience and provide clearer insights. This addition allows users to interact with the data in a more visually appealing and comprehensible manner.

The core of our project lies in ETL (Extract, Transform, Load) workflows, where raw data undergoes transformation. The ETL script extracts and transforms data from the web before loading it into the SQLite database, enhancing data integrity and usability.

## Instructions on how to use and interact with the project

## Documentation of the database used and why (e.g. benefits of SQL or NoSQL for this project)
SQLite was selected as the database solution for its pragmatic attributes that align with the project's requirements. Its serverless architecture and minimal configuration demands simplify the implementation process. The single-file storage format enhances portability, enabling easy project sharing and deployment. SQLite's efficiency in managing small to medium-sized datasets is well-suited for the project's focus on vehicle safety data. The native support for Python through the `sqlite3` module facilitates seamless ETL workflows, contributing to the overall project efficiency.In summary, SQLite is chosen for its simplicity, efficiency, and seamless integration, offering a practical and effective solution for the storage and retrieval of safety-related data in this project.

### ETL workflow with diagrams or ERD


### References - Data Sources and Code not yours

Plotly: https://plotly.com/python/basic-charts/

## Authors

Contributors names
Tanner-Brandon-Cindy-Gen

