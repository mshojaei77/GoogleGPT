from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import nltk
from googlesearch import search

app = Flask(__name__)

# Configure OpenAI
openai_client = OpenAI(api_key='YOUR API HERE')

# Dictionary for caching GPT responses
gpt_response_cache = {}

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
            return ""

        summary = ' '.join([element.text for element in content])
        return summary.strip()
    except requests.RequestException as e:
        return ""

def fetch_relevant_text(search_query, num_results=1):
    relevant_text = ''
    for result_count, result in enumerate(search(search_query, num_results=num_results)):
        try:
            summary = fetch_webpage_summary(result)
            summary = summary.strip()
            relevant_text += summary + "\n\n"
        except Exception as e:
            pass
    return relevant_text

def generate_gpt_summary(query, relevant_text, token_limit=4096):
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

    gpt_responses = []
    for chunk in chunks:
        try:
            if chunk in gpt_response_cache:
                gpt_responses.append(gpt_response_cache[chunk])
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

                gpt_response_cache[chunk] = response_content
                gpt_responses.append(response_content)
        except Exception as e:
            pass

    return gpt_responses


@app.route('/', methods=['GET', 'POST'])
def index():
    result_url = None
    gpt_responses = []

    if request.method == 'POST':
        query = request.form['query']
        website = request.form['website']

        search_query = f"Site:{website} {query}" if website else query
        relevant_text = fetch_relevant_text(search_query)
        
        if relevant_text and "Error fetching summary" not in relevant_text:
            result_url = list(search(search_query, num_results=1))[0]
            gpt_responses = generate_gpt_summary(query, relevant_text, token_limit=4096)

    return render_template('index.html', result_url=result_url, gpt_responses=gpt_responses)



if __name__ == '__main__':
    app.run(debug=True)
