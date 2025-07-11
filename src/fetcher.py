import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any

# Define base URLs for the API
EUTILS_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_paper_details(query: str, debug: bool = False) -> List[Dict[str, Any]]:
    """
    Fetches and processes research papers from PubMed based on a query.
    """
    if debug:
        print(f"Executing search with query: {query}")

    # ESearch to get PubMed IDs (PMIDs)
    esearch_url = f"{EUTILS_BASE_URL}esearch.fcgi"
    esearch_params = {
        "db": "pubmed",
        "term": query,
        "retmax": "100"  # Limit results for demonstration
    }
    try:
        response = requests.get(esearch_url, params=esearch_params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        if debug:
            print(f"API request failed: {e}")
        return []

    root = ET.fromstring(response.content)
    id_list = [elem.text for elem in root.findall(".//Id")]

    if not id_list:
        if debug:
            print("No papers found for the given query.")
        return []

    # Step 2: EFetch to get paper details
    efetch_url = f"{EUTILS_BASE_URL}efetch.fcgi"
    efetch_params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "xml"
    }
    try:
        response = requests.get(efetch_url, params=efetch_params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        if debug:
            print(f"API request failed: {e}")
        return []
    
    papers_xml = ET.fromstring(response.content)
    
    # parsing 
    processed_papers = parse_and_filter_papers(papers_xml)
    
    return processed_papers 

def is_non_academic(affiliation: str) -> bool:
    """
    Determine if an affiliation is non-academic (e.g., a company).
    It works by checking for the absence of academic keywords.
    """
    affiliation_lower = affiliation.lower()
    
    # List of keywords that typically indicate an academic or research institution
    academic_keywords = [
        "university", "college", "school of", "institute of", 
        "academic", "hospital", "research center", "laboratory"
    ]

    # If any of these keywords are present, it's likely academic.
    for keyword in academic_keywords:
        if keyword in affiliation_lower:
            return False
            
    # If no academic keywords were found, we'll assume it's non-academic.
    # This method can be improved.
    return True


def parse_and_filter_papers(root: ET.Element) -> List[Dict[str, Any]]:
    """
    Parses the XML root from EFetch and filters for papers with non-academic authors.
    """
    filtered_papers = []
    
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        
        # Safely get publication date
        pub_date_node = article.find(".//PubDate")
        pub_date = pub_date_node.findtext(".//Year", "") + "-" + pub_date_node.findtext(".//Month", "")
        
        corresponding_author_email = "" # Placeholder
        non_academic_authors = []
        company_affiliations = set()

        authors = article.findall(".//Author")
        for author in authors:
            affiliation_info = author.find(".//AffiliationInfo/Affiliation")
            if affiliation_info is not None:
                affiliation_text = affiliation_info.text
                if is_non_academic(affiliation_text):
                    last_name = author.findtext(".//LastName", "")
                    initials = author.findtext(".//Initials", "")
                    author_name = f"{initials} {last_name}".strip()
                    
                    non_academic_authors.append(author_name)
                    company_affiliations.add(affiliation_text)
                    
                    # Check for corresponding author email 
                    email_node = author.find(".//AffiliationInfo/Affiliation")
                    if email_node is not None and '@' in email_node.text:
                         # A simple regex would be more robust here
                        corresponding_author_email = email_node.text

        if non_academic_authors:
            filtered_papers.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(list(company_affiliations)),
                "Corresponding Author Email": corresponding_author_email
            })

    return filtered_papers

