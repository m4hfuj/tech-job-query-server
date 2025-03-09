# Tech Job Query Server

A Flask-based REST API server that provides analytics and insights about technical job listings in Bangladesh. The server scrapes job data from BDJobs, processes it, and serves analyzed information about job requirements, skills, and educational qualifications.

## Features

- Job domain classification using AI (FLAN-T5 model)
- Real-time job data analytics
- Educational qualification analysis
- Programming language and framework requirements analysis
- Firebase integration for data persistence
- Cross-origin resource sharing (CORS) support

## Prerequisites

- Python 3.x
- Firebase account and credentials
- Chrome WebDriver (for Selenium)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/m4hfuj/tech-job-query-server.git
cd tech-job-query-server
```

## Data Analysis Features

- Education Analysis: Categorizes educational requirements into Bachelors, Masters, Diploma, and Others
- Programming Languages: Identifies and ranks required programming languages
- Frameworks: Analyzes framework requirements across job listings
- Job Domain Classification: Uses AI to classify jobs into specific domains like Web Development, Software Development, etc.


## Technology Stack

- Flask (Web Framework)
- Firebase (Database)
- Selenium (Web Scraping)
- BeautifulSoup4 (HTML Parsing)
- Pandas (Data Analysis)
- Hugging Face Transformers (AI Classification)
- LangChain (AI Pipeline)


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

