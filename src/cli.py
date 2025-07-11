import argparse
import sys
import csv
from .fetcher import fetch_paper_details 

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed with non-academic authors.")
    parser.add_argument("query", type=str, help="The search query for PubMed.")
    
    parser.add_argument(
        "-f", "--file", 
        type=str, 
        help="Specify the filename to save the CSV results."
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Print debug information during execution." 
    )
    
    args = parser.parse_args()

    # Call core logic
    papers = fetch_paper_details(args.query, args.debug)

    if not papers:
        if args.debug:
            print("No matching papers found or an error occurred.")
        return

    # Define the CSV output
    fieldnames = [
        "PubmedID", "Title", "Publication Date", 
        "Non-academic Author(s)", "Company Affiliation(s)", 
        "Corresponding Author Email"
    ] 

    # Write to a file or print to the console
    if args.file:
        output_file = open(args.file, 'w', newline='', encoding='utf-8')
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(papers)
        output_file.close()
        if args.debug:
            print(f"Results saved to {args.file}")
    else:
        # Print to console (stdout)
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(papers)