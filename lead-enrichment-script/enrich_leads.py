import pandas as pd # For data manipulation
import requests  # For making API requests
from bs4 import BeautifulSoup # For web scraping
import re # For regular expressions (finding patterns in text)

def enrich_leads(): # Main function to enrich leads
    print("Lead enrichment script starting...")

    # Load leads from CSV & set file paths
    input_file = "leads.csv" # Input CSV file with leads
    output_file = "leads_enriched.csv" # Output CSV file for enriched leads

    try:
        df = pd.read_csv(input_file) # Read the CSV file into a DataFrame
        print(f"Loaded {len(df)} leads from {input_file}.") # Print the number of leads loaded
    except FileNotFoundError: #error handling
        print(f"Error: {input_file} not found.")
        return

    # user-agent headers to mimic a browser request
    headers = { # Set up headers to mimic a browser request
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # list to store results
    results = []

    #
    for index, row in df.iterrows(): # Iterate through each lead in the DataFrame
        domain = row["Domain"] # Get the domain from the current row

        if not domain.startswith("http"): # Ensure the domain has the correct URL format
            url = f"https://{domain}" # If not, prepend "https://"
        else:
            url = domain # Use the domain as is

        print(f"\n🔍 Scanning: {domain}...")

        try: #Connect to the site using header, 'timeout=5' means give up if they don't answer in 5 seconds.
            response = requests.get(url, headers=headers, timeout=5) # Make a GET request to the URL with headers and timeout

            if response.status_code == 200: #200 means success
                soup = BeautifulSoup(response.text, "html.parser") # Parse the HTML content of the page

                # Extract emails using regex
                emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.get_text()) #
                emails = list(set(emails)) # Remove duplicates

                # Extract phone numbers using regex
                phones = re.findall(r"\+?\d[\d -]{8,}\d", soup.get_text()) # Simple regex for phone numbers
                phones = list(set(phones)) # Remove duplicates

                print(f"  📧 Found emails: {emails if emails else 'None'}")
                print(f"  📞 Found phones: {phones if phones else 'None'}")

                results.append({ # Append the results to the list
                    "Domain": domain,
                    "Emails": ", ".join(emails) if emails else "None",
                    "Phones": ", ".join(phones) if phones else "None"
                })
            else:
                print(f"  ⚠️ Status Code: {response.status_code}") # Print the status code if not 200
                results.append( #append error status to results
                    {"Domain": domain, "Status": f"Error {response.status_code}", "Emails": "N/A", "Phones": "N/A"})

        except Exception as e: # Handle exceptions (e.g., connection errors, timeouts)
            print(f"  ❌ Connection Failed.")
            results.append({"Domain": domain, "Status": "Dead", "Emails": "N/A", "Phones": "N/A"}) # Append dead status to results

            # === THE EXPORT SECTION (You needed this!) ===
        print("\n💾 Saving data...") # Save the results to a new CSV file
        output_df = pd.DataFrame(results) # Convert the results list to a DataFrame
        output_df.to_csv(output_file, index=False) # Write the DataFrame to a CSV file without the index
        print(f"✅Data saved to '{output_file}'")

enrich_leads()
