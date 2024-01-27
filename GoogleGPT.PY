import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from googlesearch import search
import logging
import nltk
from functools import lru_cache

# Configure logging once at the beginning
logging.basicConfig(filename='program_log.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

openai_client = OpenAI(api_key='YOUR API HERE')

# Dictionary for caching GPT responses
gpt_response_cache = {}

@lru_cache(maxsize=None)
def fetch_webpage_summary(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Handle potential edge cases in webpage parsing
        content = soup.find_all(['p', 'span'])
        if not content:
            logging.warning(f"No relevant content found in {url}")
            return ""

        summary = ' '.join([element.text for element in content])
        return summary.strip()
    except requests.RequestException as e:
        logging.error(f"Error fetching summary from {url}: {e}")
        return ""

def main_program():
    logging.info("Program started")
    query = input("Enter your query: ").strip()
    
    while not query or query.lower() == "exit":
        logging.warning("Invalid query or 'exit' command entered")
        print("Please enter a valid query or type 'exit' to quit.")
        query = input("Enter your query: ").strip()

    website = input("Enter site URL to retrieve search result (Optional): ").strip()
    search_query = f"Site:{website} {query}" if website else query

    relevant_text = fetch_relevant_text(search_query)
    if relevant_text and "Error fetching summary" not in relevant_text:
        generate_gpt_summary(query, relevant_text, token_limit=4096)

    logging.info("Program completed")

def fetch_relevant_text(search_query, num_results=1):
    relevant_text = ''
    for result_count, result in enumerate(search(search_query, num_results=num_results)):
        logging.info(f"Source {result_count + 1} - {result}")
        try:
            summary = fetch_webpage_summary(result)
            summary = summary.strip()
            relevant_text += summary + "\n\n"
            print(f"Website summary fetched from: {result}")
        except Exception as e:
            logging.error(f"Error fetching summary for {result}: {e}")
    return relevant_text

def generate_gpt_summary(query, relevant_text, token_limit=4096):
    logging.info("GoogleGPT: Generating summary")
    logging.info("Relevant Text:\n%s", relevant_text)
    print("\nGoogleGPT Generated Summary:")
    prompt = f"""use this information, along with your knowledge to provide a comprehensive and informative Summary about "{query}" :
    ```
    {relevant_text}
    ```
    """
    sentences = nltk.sent_tokenize(prompt)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= token_limit:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())

    for chunk in chunks:
        try:
            # Check if the GPT response is already cached
            if chunk in gpt_response_cache:
                print("\nCached GPT Response:\n", gpt_response_cache[chunk])
                logging.info("GPT response fetched from cache.")
            else:
                stream = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": chunk,
                        },
                    ],
                    stream=True,
                )

                response_content = ""
                for response_chunk in stream:
                    if response_chunk.choices:
                        choice = response_chunk.choices[0]
                        content = choice.delta.content
                        if content is not None:
                            response_content += content

                # Cache the GPT response
                gpt_response_cache[chunk] = response_content

                # Print GPT response content in a readable format
                print(response_content)
                logging.info("GPT response generated and cached.")
        except Exception as e:
            logging.error(f"Error generating GPT summary for chunk: {e}")

if __name__ == "__main__":
    main_program()
