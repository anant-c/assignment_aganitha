# PubMed Paper Fetcher

A command-line tool to fetch research papers from PubMed, filtering for those with authors affiliated with pharmaceutical or biotech companies.

## Video Demo: https://youtu.be/GsMyritvqKk

## Code Organization

The project is organized into two main parts as per the assignment's bonus requirements:

* `pubmed_paper_fetcher/fetcher.py`: A core Python module containing all the logic for interacting with the PubMed API, parsing data, and filtering results.
* `pubmed_paper_fetcher/cli.py`: A command-line interface built with `argparse` that uses the `fetcher` module to provide a user-friendly program.

## Installation & Execution

This project uses [Poetry](https://python-poetry.org/) for dependency management.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/anant-c/assignment_aganitha.git
    cd pubmed-paper-fetcher
    ```

2.  **Install dependencies:**
    ```bash
    poetry install
    ```

3.  **Run the program:**
    ```bash
    poetry run get-papers-list "your pubmed query here" [options]
    ```

## Usage

**Basic Example:**
```bash
poetry run get-papers-list "crispr gene editing"
```

**Saving to a File:**
```bash
poetry run get-papers-list "oncology pfizer" -f papers.csv
```

**With Debug Output:**
```bash
poetry run get-papers-list "vaccine moderna" -f moderna_papers.csv -d
```

## Tools Used

* **Python 3**: Core programming language.
* **Poetry**: Dependency management and packaging.
* **Requests**: For making HTTP API calls to PubMed.
* **LLM Assistance**: This guide was structured with the help of an LLM to ensure all requirements of the take-home problem were met systematically. 