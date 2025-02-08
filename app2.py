from googleapiclient.discovery import build
import pandas as pd

def google_search(search_term, api_key, cse_id, **kwargs):
    """
    Performs a Google search using the Custom Search API and returns the results.
    """
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def save_to_excel(results, filename):
    """
    Saves the search results into an Excel file.
    """
    # Create a DataFrame from the results
    df = pd.DataFrame(results)
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)
    print(f"Results saved to {filename}")

def main():
    # User input
    search_query = input("Enter your search query: ")
    num_results = int(input("Enter the number of results to fetch: "))
    
    # Your API key and Search Engine ID from Google Cloud Console
    API_KEY = 'AIzaSyA6oqqvyQVwCWm0AiqOU6c_Xb-PntM-y7U'  # Replace with your API key
    SEARCH_ENGINE_ID = 'f488d83a7d87b448f'  # Replace with your Search Engine ID
    
    # Fetch search results
    results = google_search(search_query, API_KEY, SEARCH_ENGINE_ID, num=10)
    
    # Prepare data for Excel
    data = []
    for result in results:
        data.append({
            'Title': result['title'],
            'Link': result['link'],
            'Snippet': result.get('snippet', '')
        })
    
    # Save to Excel
    filename = f"google_search_results_{search_query.replace(' ', '_')}.xlsx"
    save_to_excel(data, filename)

if __name__ == "__main__":
    main()