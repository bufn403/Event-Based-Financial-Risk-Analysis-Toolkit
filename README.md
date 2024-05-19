# Event-Based Financial Risk Analysis

## Introduction
Welcome to the Event-Based Financial Risk Analysis Toolkit! This is a web-based and command line application designed to assist investors, financial analysts, and portfolio managers by providing an alternative approach to risk analysis. Traditional financial risk analysis heavily relies on historical financial data and statistical models. Our toolkit integrates qualitative data, such as news events and company filings, to enhance risk assessment.

Our method determines a company’s exposure to risk by assessing whether a headline or event is semantically similar to risks mentioned in the company’s filings. This is achieved through natural language processing techniques, detailed in the methodology section. In addition to the web-based toolkit, we have developed a command-line application for generating, building, and querying detailed knowledge graphs. These graphs visualize relationships between companies, their attributes, and risk factors, enhancing investors’ ability to make informed decisions.

Our toolkit aims to be integrated alongside the general quantitative approach and help the investor approach news events and qualitative information. We hope to provide utility when an event occurs and an investor is looking to query which companies have listed a concern in their risk factors.

## Intended Audience
Our toolkit is tailored for:
- Investors
- Financial analysts
- Portfolio managers


## Motivation & Goals
The primary objective of this toolkit is to help investors connect events to company risk factors. By providing a structured and automated way to correlate events with their potential financial impacts, we aim to enhance the decision-making process for investors.

The goal for the toolkit is to be able to list companies given a specific headline or news event. Additionally, when provided with a dataset of news events and company risk filings, the toolkit has a feature be able to prepare a knowledge graph with the appropriate connections. We chose to make this toolkit as a web application because we wanted to emphasize a full working experience to the investor, rather build than a set of disconnected tools. Another useful feature added to the toolkit is the ability to download the SEC-10K filing data directly from the web application, as it’s used by the toolkit in sentiment analysis and can provide more context to the user. In addition to the web-based toolkit, we developed a command line application that can build, query, and encode a more detailed knowledge graph than the one present in the web application. Finally, the last piece of the web-based toolkit is a visualization of the knowledge graph that connects companies and nodes together. The user can click on a company or event to extract more information. This has its applications with allowing investors to visualize more complex relationships. The next sections will elaborate on the functionalities and implementations of the tools.

This is a set of tools that each serve their own purpose to an investor that is particularly interested in a company’s risk. From the headline sentiment analysis, risk text downloader, to the knowledge graph, we intended for each of these to have utility for an investor and aid in their decision-making.

### Web Application Features
- **Financial Event Risk Analysis:** 
The primary page is the financial event risk analysis tool, which is used to evaluate how different companies are affected by a headline in a calendar year. The user has three dropdowns that affect which risk filings are evaluated: the filing year, the company farma french sector, and the semantic evaluation metric. Once the user clicks the analyze button, a table will be populated, with each row representing a company. An entry in the table will either have a semantic similarity labeled high, medium, or low and will be colored green, yellow, and red respectively. 
- **SEC 10-K Risk Text Downloader:** 
This feature provides a resource for downloading the risk sections of SEC 10-K documents for various companies. The interface allows users to search for company risk filings by entering a stock ticker or selecting a sector from a dropdown menu. The page displays a table listing various companies, their corresponding sector classifications, and links to view stock charts. Additionally, users can download risk filings in CSV format for each company, enabling easy access to historical risk text data.
- **Knowledge Graph:** 
The Knowledge Graph feature is a comprehensive visualization tool. It displays various companies categorized by sector, such as Consumer, Manufacturing, HiTec, Health and Medical, Energy, and Other. The events impacting these companies are color-coded by type, including General, Weather, Political, Economy, Energy, and Business events. The interface allows users to filter data by sector and event type, as well as to adjust the minimum number of connections displayed on the graph. The interactive graph visualizes the relationships and risk factors associated with different companies. The user can click on a company node to get a list of all the risk factors. Similarly, the user can click an event to will display a list of all the companies connected to it, indicating they are at high risk to the particular event.


### Detailed Knowledge Graph Features
This detailed knowledge graph serves as a Python application that can be used to build, populate, query, and export our knowledge graph. The program uses a Python library called rdflib to store the nodes and edges in an RDF graph. This allows the graph to be easily stored and exported into different formats. The application also keeps track of commonly used nodes (commonly referred to as objects) and edges (commonly referred to as predicates) using Python dictionaries for consistency.

- **Building and Populating the Knowledge Graph:** 
The first functionality is building and populating the knowledge graph. We have developed two functions to accomplish that. The first allows the user to pass in a company ticker, which the program then takes to retrieve information fromthat company from the yfinance API. The information obtained from that API is used to create attribute edges for thatcompany. This information includes things like different types of risk, the location of the company’s headquarters, and the company’s sector. The second function also allows the user to pass in a company ticker. It determines if the company already exists in the knowledge graph and adds it if it doesnot exist in the graph. Then, we use the provided ticker and extract its SEC 10-K filing sentences, its related risk factor, and the filing year that sentence is taken from our dataset. Using the same process in the semantic similarity analysis, the SEC 10-K filing sentences and related risk factors are used to connect companies to types of risk they might be vulnerableto, with the corresponding text segment that has the highest similarity score. The filing year of these sentences is used as an additional query parameter and provides a time context tothe risk factors and sentences.

- **Querying and Exporting Knowledge Graph:** 
The detailed knowledge graph library also has three types of built-in queries that a user can make: query companies that meet a condition, query a specific company by ticker, and query SEC-10K filing sentences that meet a condition. The first query type, allows the user to query companies that are in a certain sector, or industry, or have a specific risk factor. This returns a list of companies and their tickers that meet those criteria. The second query allows you to get more information on a company from their ticker and returns a list of the attributes–sector, industry, headquarters location, risk, etc. Finally, the third query finds all SEC-10K filing sentences that meet a condition and returns them as a list. These are not the only queries that can be done on the knowledge graph. Since the knowledge graph is stored in an RDF graph from rdflib which has a built-in function for queries, a user can also pass in custom queries. The library also has two functions to export the knowledge graph into various file formats such as Turtle, JSON-LD, and RDF/XML.


### Folders

- **src/**
    > The src folder contains the main applications of the research project. Within this folder, there will be a folder containing all the code for the React frontend, Flask backend, and finally the Python code for the Detailed Knowledge Graph. This folder comprises of the integral parts to the overall application.

- **docs/**
    > The docs folder contains the final deliverable report of this paper as well as the references in the a bib file. You can view the final report document for more detailed information about this project.

- **data/**
    > The data folder contains the nested folder for all the companies' historical risk text, organized by the farma french five industry sector that they are located in. Additionally, the labeled_events.csv is the file used for builindg the webpage knowledge graph. It contains the companies, years, events, as well as the corresponding classification of the events.

- **notebooks/**
    > The notebooks folder contains various Jupyter notebooks for data gathering, data cleaning, or utilities. You can view and run each jupyter notebook individually in order to explore the use case for each file.


## Installation & Usage

To clone and set up the project, follow the following steps.

First, clone the project repository.

```
git clone https://github.com/bufn403/Event-Based-Financial-Risk-Analysis-Toolkit.git
```

### Getting Started

Please ensure you are logged in on [GitHub](https://github.com) and have permissions to create a repository.

#### Requirements
- You must have **npm** correctly installed in order to run the frontend React application
- You need a Python version of at least **3.9** in order to run the backend Flask application
    - Optionally, you can utilize virtual environments by using this command:
    ```python3 -m venv venv```


### Running Python Notebooks

#### 1. SEC Web Scraper
To run `SEC Scraper.ipynb`:
```
jupyter notebook notebooks/SEC\ Scraper.ipynb
```

**NOTE:** This notebook can take hours to process and will use up gigabytes of storage if you fully intend to scrape all the companies in the NAICS file. However, I implemented it so that you can stop scraping and recontinue at any point.

This notebook will output a nested folder of companies organized by their farma french 5 industry sector. They are all CSV files and are named based on the company's stock ticker.

#### 2. NLP Event Classification
To run `NLPEventClassification.ipynb`:
```
jupyter notebook notebooks/NLPEventClassification.ipynb
```

This notebook uses the "Response" column of the **events.csv** file and creates a new row for the classification. The output is another CSV with the additional classification column.

#### 3. Utility: Text Helper
To run `text_helper.ipynb`:
```
jupyter notebook notebooks/text_helper.ipynb
```

This function was developed as a utility for determining the size of the risk factors from the company CSV. It can be used to help you debug the application if you encounter any problems. You can also use it to evaluate if you are correctly segmenting the risk factors and cleaning the text.

### Web Application
In order to have a fully working web application, you **must** have **both the frontend and backend** fully operational and ensure that the endpoints are correctly configured. In this application, note that the local port the flask application is assumed to take is ```5000```.


#### 1. Frontend React Application

First, you need to ensure that you have installed the necessary libraries to run the React application.

**Note:** The frontend application has an environment variable that determines if the fetch endpoints will be taken from production or from local. If you want to test in your local development server, the frontend must be configured to **dev**.

Ensure that this is in the environment variables!
```const environment = "dev"```

**You must have npm installed for this part!**

Run the following code in order to install all the packages. 
```
npm install
```

After you should have correctly installed all the necessary npm packages to run your application. To run the application, ensure that you are in the base directory of the application, and all you need to do is run:

```
npm start
```


Finally, open `http://localhost:5000` in your web browser.

#### 2. Backend Flask Application
First, you need to ensure that you have installed the necessary libraries to run the Flask application.

```
pip install -r requirements.txt
```

**Optionally:** You can also decide to create a virtual environment instead of using your own python environment.

Once you have successfully installed all of the necessay libraries, you can now run the application. Ensure that you are in the same direction that app.py is located in and run:

```
flask run
```


Once the application is running, you should be able to see any API requests made to the backend through the terminal.

#### 3. Full Application

In order to run the full application, you need to have successfully completed the previous two steps and have both the React app and Flask app running.

**Tip:** You can ensure the flask applicaiton is running by using the base "/" endpoint, which will return the text "API is Online!" along with a ```200``` status code.

Finally, if everything is correctly configured and set up, you should be able to interact with the frontend application and be able to make API GET requests to the backend.


### Detailed Knowledge Graph

The Detailed Knowledge Graph feature allows users to build, populate, query, and export comprehensive knowledge graphs. It utilizes the `rdflib` Python library to store nodes and edges in an RDF graph format, ensuring compatibility with various export formats.

#### Building and Populating the Knowledge Graph

The application provides functions to:
- **Retrieve Company Data:** By passing a company ticker, the program retrieves information from the yfinance API, creating attribute edges for the company (e.g., risk types, headquarters location, sector).
- **Add Company Data:** It verifies if the company exists in the graph and adds it if not. It then extracts SEC 10-K filing sentences and related risk factors, connecting companies to vulnerabilities with the highest similarity scores, using the filing year for time context.

#### Querying and Exporting the Knowledge Graph

Three built-in query types are available:
1. **Query Companies:** Retrieve companies in a sector, industry, or with specific risk factors.
2. **Query Specific Company:** Get detailed information on a company by its ticker.
3. **Query SEC-10K Sentences:** Find filing sentences meeting specific conditions.

Additionally, custom queries can be made using rdflib's built-in function. The knowledge graph can be exported into various formats like Turtle, JSON-LD, and RDF/XML.


## Contributing
We welcome contributions to enhance the toolkit. Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## Contact
For any inquiries or issues, please contact us:
- Rodz Andrie Amor: [ramor12@umd.edu](mailto:ramor12@umd.edu)
- Keshav Ganapathy: [keshavg@umd.edu](mailto:keshavg@umd.edu)
- Sash Lamba: [sash19@umd.edu](mailto:sash19@umd.edu)
- Sakshi Gholap: [sgholap@umd.edu](mailto:sgholap@umd.edu)
- The-Vinh Calix Tran-Luu: [tranluu@umd.edu](mailto:tranluu@umd.edu)

<!-- 1. **Create new repository from template**

    The <span style="color:#3EACAD">template</span> is a [GitHub template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template); in other words, you can generate a new GitHub repository with the same files and folders to use as the starting point for your project.

    > 🌟 [Create new repository from **template**](https://github.com/worldbank/template/generate)

    ```{figure} docs/images/github-template.png
    ---
    ---
    ```

    Now, give your repository a name, choose the **visibility** (Public or Private) and click **Create repository from template**.

    ```{figure} docs/images/github-template-create.png
    ---
    ---
    ```

    *Voilà!* The repository has been created with the same files and folders of the <span style="color:#3EACAD">template</span>.

    ```{seealso}
    For additional information, see the [GitHub documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
    ```



4. **Review and update README files**

> 🌟 `https://<your-github-username>.github.io/<your-project-name>`

For example, see this <span style="color:#3EACAD">template</span> as a live demo.

> 🌟 [worldbank.github.io/template](http://worldbank.github.io/template) (Live Demo)

### Adding Content

The <span style="color:#3EACAD">template</span> is created as a [Jupyter Book](https://jupyterbook.org/intro.html) - an open-source project to build beautiful, publication-quality books and documents from computational content. Let's see below how to add, execute and publish new content for your project.

#### Table of Contents

When ready to publish the *documentation* on [GitHub Pages](https://pages.github.com/), all you need to do is edit the [table of contents](#table-of-contents) and add and/or update content you would like to display. [Jupyter Book](https://jupyterbook.org) supports content written as [Markdown](https://daringfireball.net/projects/markdown/), [Jupyter](https://jupyter.org) notebooks and [reStructuredText](https://docutils.sourceforge.io/rst.html) files and the `docs/_toc.yml` file controls the [table of contents](#table-of-contents) of your book.

The <span style="color:#3EACAD">template</span> comes with the [table of contents](#table-of-contents) below as an example.

```yaml

format: jb-book
root: README

parts:

- caption: Documentation
    numbered: True
    chapters:
  - file: notebooks/world-bank-api.ipynb
- caption: Additional Resources
    chapters:
  - url: <https://datapartnership.org>
        title: Development Data Partnership
  - url: <https://www.worldbank.org/en/about/unit/unit-dec>
        title: World Bank DEC
  - url: <https://www.worldbank.org/en/research/dime>
        title: World Bank DIME

```

```{seealso}
[Jupyter Book Structure and organize content](https://jupyterbook.org/en/stable/basics/organize.html)
```

#### Dependencies

The next step is ensure your code is maintainable, reliable and reproducible by including
any dependencies and requirements, such as packages, configurations, secrets (template) and additional instructions.

The <span style="color:#3EACAD">template</span> suggests to use [conda](https://docs.conda.io/) (or [mamba](https://mamba.readthedocs.io/en/latest/)) as environment manager and, as [conventional](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html), the environment is controlled by the `environment.yml` file.

The `environment.yml` file is where you specify any packages available on the [Anaconda repository](https://anaconda.org) as well as from the Anaconda Cloud (including [conda-forge](https://conda-forge.org)) to install for your project. Ensure to include the pinned version of packages required by your project (including by Jupyter notebooks).

```yaml
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - bokeh=2.4.3
  - pandas=1.4.3
  - pip:
    - requests==2.28.1
```

To (re)create the environment on your installation of [conda](https://conda.io) via [anaconda](https://docs.anaconda.com/anaconda/install/), [miniconda](https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/) or preferably [miniforge](https://github.com/conda-forge/miniforge), you only need to pass the `environment.yml` file, which will install requirements and guarantee that whoever uses your code has the necessary packages (and correct versions). By default, the <span style="color:#3EACAD">template</span> uses [Python 3.9](https://www.python.org).

```shell
conda env create -n <your-environment-name> -f environment.yml
```

In case your project uses Python, it is *strongly* recommended to distribute it as a [package](https://packaging.python.org/).

```{important}
The <span style="color:#3EACAD">template</span> contains an example - the [datalab](https://github.com/worldbank/template/tree/main/src/datalab) Python package - and will automatically find and install any `src` packages as long as `pyproject.yml` is kept up-to-date.
```

```{seealso}
[Conda Managing Environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
```

#### Jupyter Notebooks

[Jupyter Notebooks](https://jupyter.org) can be beautifully rendered and downloaded from your book. By default, the <span style="color:#3EACAD">template</span> will render any files listed on the [table of contents](#table-of-contents) that have a notebook structure. The <span style="color:#3EACAD">template</span> comes with a Jupyter notebook example, `notebooks/world-bank-api.ipynb`, to illustrate.

```{important}
Optionally, [Jupyter Book](https://jupyterbook.org) can execute notebooks during the build (on GitHub) and display **code outputs** and **interactive visualizations** as part of the *documentation* on the fly. In this case, Jupyter notebooks will be executed by [GitHub Actions](https://github.com/features/actions) during build on each commit to the `main` branch. Thus, it is important to include all [requirements and dependencies](#dependencies) in the repository. In case you would like to ignore a notebook, you can [exclude files from execution](https://jupyterbook.org/en/stable/content/execute.html#exclude-files-from-execution).
```

```{seealso}
[Jupyter Book Write executable content](https://jupyterbook.org/en/stable/content/executable/index.html)
```
-->
