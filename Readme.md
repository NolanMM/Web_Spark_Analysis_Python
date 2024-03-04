<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
  </a>
  <p align="center">
    <br />
    <a href="https://github.com/NolanMM/Web_Spark_Analysis_Python"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://webanalysisspark-6b94ca80dba0.herokuapp.com/">View Demo</a>
    ·
    <a href="https://github.com/NolanMM/Web_Spark_Analysis_Python/issues">Report Bug</a>
    ·
    <a href="https://github.com/NolanMM/Web_Spark_Analysis_Python/issues">Request Feature</a>
  </p>
</div>

<details>
  <summary><b>Table of Contents</b></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#prerequisites">Usage</a></li>
      </ul>
    </li>
    <li><a href='#database-setup-and-configuration'>Database Setup and Configuration</a></li>
    <li><a href="#technologies">Technology</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

[![Product Name Screen Shot][product-screenshot]](https://webanalysisspark-6b94ca80dba0.herokuapp.com/)

Welcome to our Flask Python web application designed to create insightful summary reports, complete with charts, based on input YouTube usernames. This innovative tool harnesses the power of the YouTube API to collect relevant data and provide users with comprehensive analyses of their channel's performance.

With just a few simple steps, users can input their YouTube username, and our application will swiftly gather essential information, such as views, likes, comments, and more. Leveraging this data, our app generates intuitive charts and graphs that offer valuable insights into the channel's growth, engagement, and audience demographics.

Whether you're a content creator seeking to understand your audience better or a marketing professional aiming to optimize your YouTube strategy, our web app provides actionable intelligence to drive informed decision-making. Our user-friendly interface ensures a seamless experience, allowing users to access detailed reports effortlessly.

Harness the power of data-driven decision-making with our Flask Python web application, and unlock the full potential of your YouTube channel today! :smile: :smile: :smile:

</br>
<div align="center">

### Built With

[![python][python]][python-url] [![Flask][Flask]][Flask-url] [![Gunicorn][Gunicorn]][Gunicorn-url] [![Heroku][Heroku]][Heroku-url] [![Spark][Spark]][Spark-url] [![Youtube][Youtube]][Youtube-url] [![SQLite][SQLite]][SQLite-url] [![GitHub][GitHub]][GitHub-url] [![MIT License][license-shield]][license-url] [![Contributors][contributors-shield]][contributors-url] [![Issues][issues-shield]][issues-url]

</div>

</br>

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Installation

_The Instruction for installing and set up the project locally._

### Prerequisites

1. Before running the code examples, we have to clone the repository to your local machine:

* Git Clone: Clone the repository to your local machine:
  
  ```bash
    git clone https://github.com/NolanMM/Web_Spark_Analysis_Python.git
  ```

2. Before running the code examples, make sure you have the virtual enviroment is installed and be ready to use:
We need to create a new `Python 3.11` virtual enviroment for this project.

* If you want to create a new virtual enviroment, you can use the following command in the terminal of the project directory:

  * In Windows or Linux, you can use the following command:
  
  ```bash
    python -m venv venv
  ```

  * Then, you can activate the virtual enviroment by using the following command:
  
  ```bash
    venv\Scripts\activate
  ```

  * In MacOs, you can use the following command:
  
  ```bash
    python3 -m venv venv
  ```

  * Then, you can activate the virtual enviroment by using the following command:
  
  ```bash
    source venv/Scripts/activate
  ```

* Make sure the virtual environment needed for project is activate with corresponding project directory, you can use the following command:

  * In Windows or Linux, you can use the following command:
  
  ```bash
    venv\Scripts\activate
  ```

  * In MacOs, you can use the following command:
  
  ```bash
    source venv/Scripts/activate
  ```

* Install requirements.txt: Automatically installed dependencies that needed for the project:
  
  ```bash
    pip install -r requirements.txt
  ```

</br>

### Usage

To use the code examples in this repository, follow these steps:

1. Install the required dependencies as mentioned in the [Prerequisites](#prerequisites) section.

2. Run the following command in the terminal to start the server:

```bash
  gunicorn app:app
```

</br>

### Database Setup and Configuration

To create the new database for this repository, follow these steps:

1. Double-check if `/instance/SparkWeb.db` file is existed in the project directory. If yes, delete it.

2. Run the `Database_Handle/Create_Table.py` in the terminal to start the server:

```bash
  python Database_Handle/Create_Table.py
```

To create the new database for this repository, follow these steps:

1. Double-check if `/instance/SparkWeb.db` file is existed in the project directory. If yes, delete it.

2. Run the `Database_Handle/Create_Table.py` in the terminal to create new instance of the database for the project:

```bash
  python Database_Handle/Create_Table.py
```

To check all the data and columns with data type in the database of this repository, follow these steps:

1. Double-check if `/instance/SparkWeb.db` file is existed in the project directory. If not, create a new one by steps above.

2. Run the `Database_Handle/DoubleCheckTable.py` in the terminal to clear all the data in the database of the project:

```bash
  python Database_Handle/DoubleCheckTable.py
```

To clear all the data in the database of this repository, follow these steps:

1. Double-check if `/instance/SparkWeb.db` file is existed in the project directory. If not, create a new one by steps above.

2. Run the `Database_Handle/Clear_Table.py` in the terminal to clear all the data in the database of the project:

```bash
  python Database_Handle/Create_Table.py
```

</br>

### Technologies

Before running the code examples, make sure you have the following dependencies installed:

* [Flask](Flask-url): A micro web framework written in Python. You can install it via pip:
  
  ```bash
  pip install flask
  ```

* [Flask-SqlAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/): : An extension for Flask that adds support for SQLAlchemy, a powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python. You can install it via pip:

  ```bash
  pip install flask-sqlalchemy
  ```

* [Google Youtube APIs](https://developers.google.com/youtube/v3): APIs provided by Google for interacting with YouTube services, such as uploading videos, retrieving video metadata, and managing playlists. You can install the Python client library via pip:

  ```bash
  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
  ```

* [Pyspark](Spark-url): A unified analytics engine for large-scale data processing built on top of Apache Spark. You can install it via pip:
  
  ```bash
  pip install pyspark
  ```

* [Gunicorn](https://gunicorn.org/):  A Python WSGI HTTP Server for UNIX. You can install it via pip:

  ```bash
  pip install gunicorn
  ```

* [Boostrap](https://getbootstrap.com/):  Bootstrap is a popular front-end framework for building responsive and mobile-first websites and web applications:

  ```bash
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
  ```

</br>

## Roadmap

This is a list of features that we are planning to add in the future:

* [ ] Continuous Development on Advanced Analytics
* [ ] Instagram and Twitter APIs Integration for Social Media Analytics
* [ ] Facebook and LinkedIn APIs Integration for Social Media Analytics
* [ ] Implement and improve the test coverage
* [ ] Files Downloaded Support
* [ ] Improve the User Interface
* [ ] Improve the User Experience
* [ ] Add more features to the platform
* [ ] Improve the performance of the platform
* [ ] Language Support
  * [ ] Vietnamese

</br>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

NolanM - Minh Nguyen - [@Gmail](https://twitter.com/your_username) - <minhlenguyen02@gmail.com>

Project Link: [https://github.com/NolanMM/Web_Spark_Analysis_Python](https://github.com/NolanMM/Web_Spark_Analysis_Python)

<!-- MARKDOWN LINKS & IMAGES -->
[python]: https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/downloads/release/python-3120/

[Flask]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/2.0.x/

[Gunicorn]: https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white
[Gunicorn-url]: https://github.com/

[Heroku]: https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white
[Heroku-url]: https://www.heroku.com/

[Spark]: https://img.shields.io/badge/Apache%20Spark-FDEE21?style=flat-square&logo=apachespark&logoColor=black
[Spark-url]: https://spark.apache.org/

[Youtube]: https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white
[Youtube-url]: https://www.youtube.com/

[SQLite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://www.sqlite.org/

[GitHub]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white
[GitHub-url]: https://github.com/

[contributors-shield]: <https://img.shields.io/github/contributors/NolanMM/Web_Spark_Analysis_Python.svg?style=for-the-badge>
[contributors-url]: <https://github.com/NolanMM/Web_Spark_Analysis_Python/graphs/contributors>
[license-shield]: <https://img.shields.io/github/license/NolanMM/Web_Spark_Analysis_Python.svg?style=for-the-badge>
[license-url]: <https://github.com/NolanMM/Web_Spark_Analysis_Python/blob/master/LICENSE.txt>
[issues-shield]: <https://img.shields.io/github/issues/NolanMM/Web_Spark_Analysis_Python.svg?style=for-the-badge>
[issues-url]: <https://github.com/NolanMM/Web_Spark_Analysis_Python/issues>
[product-screenshot]: documents/images/demo.png
