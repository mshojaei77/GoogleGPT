# GoogleGPT

<p align="center">GoogleGPT is a comprehensive Python program and web application that combines the power of Google search, web scraping, and OpenAI's GPT-3.5-turbo model to provide users with detailed and coherent summaries for their queries. The project is divided into two components: a Python program for command-line usage and a Flask-based web application for a more user-friendly interaction.</p>
<p align="center">
  <a href="https://t.me/v2raycollectorbot">
    <img src="https://github.com/mshojaei77/GoogleGPT/assets/76538971/5fd1dc00-49a1-47f8-9be4-e1a789175e10" alt="GoogleGPT">
  </a>
   </p>


This project is intended for **educational purposes** only. 
Any other use of it, including commercial, personal, or non-educational use, is not accepted!

## Python Program

### Features

- **Search and Summarize**: Conducts a Google search based on user input and retrieves relevant information from the web. It then uses OpenAI's GPT-3.5-turbo to generate a coherent summary.

- **Webpage Parsing**: Utilizes BeautifulSoup for parsing webpages, handling potential edge cases to ensure relevant content extraction.

- **Caching Mechanism**: Implements a caching mechanism to store GPT responses, reducing redundant API calls and improving performance.

### Dependencies

Make sure to install the required dependencies before running the Python program:

```bash
pip install requests beautifulsoup4 openai google nltk
```

### Usage

1. Obtain API Key: Replace `'YOUR API HERE` with your[ OpenAI API key](https://platform.openai.com/api-keys) in the `openai_client` initialization.

2. Run the Program: Execute the `main_program()` function in `google_gpt.py` to start the program. Enter a query when prompted and optionally provide a website URL for more specific results.

3. View Results: The program will display relevant information fetched from webpages and the generated summary by GPT-3.5-turbo.

## Web Application

### Features

- **User-friendly Interface**: The web application offers a simple and intuitive interface where users can enter queries and optional website URLs to retrieve search results.

- **Real-time GPT Summarization**: The application leverages the GPT-3.5-turbo model to generate real-time summaries for user queries, enhancing the efficiency of information retrieval.

- **Result URL Display**: After submitting a query, the web app displays the URL of the top search result, allowing users to directly access the source for more details.

### Dependencies

Ensure you have the necessary dependencies installed before running the web application:

```bash
pip install Flask requests beautifulsoup4 openai google nltk
```

### Running the Web Application

1. Open `app.py` and replace the placeholder `'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'` with your OpenAI API key in the `openai_client` initialization.

2. Run the Web App: Execute `python app.py` in the terminal to start the Flask development server.

3. Access the Web App: Open your web browser and navigate to `http://127.0.0.1:5000/`. The GoogleGPT web application should be accessible.

### Usage

1. Enter Query: Input your query in the designated field.

2. Optional Website URL: Provide a specific website URL (optional) to narrow down the search results.

3. Submit: Click the submit button to trigger the summarization process.

4. View Results: The application will display the top search result URL along with the GPT-generated summaries for the provided query.

### Future Upgrades
1. **Enhanced Frontend**: Improve the frontend by adding more styling, responsiveness, and potentially incorporating AJAX for a smoother user experience.
2. **Deployment**: Explore deployment options to make the web application accessible online, allowing users to access it from anywhere.
   
## GoogleGPT_free

A simplified Python program using OpenAI's GPT-4 (GeekGPT) through the G4F library. Fetches and summarizes information from the web with minimal user interaction.

## Features

- **Search and Summarize**: Utilizes GPT-4 (GeekGPT) for generating summaries based on Google search results.

- **Webpage Parsing**: Extracts relevant content from webpages using BeautifulSoup.

- **Caching Mechanism**: Stores GPT responses to reduce redundant API calls.

## Usage

1. **Run the Program**: Execute `main_program()` in `google_gpt_free.py`.

2. **Enter Query**: Input your query.

3. **Optional Website URL**: Provide a specific website URL (optional).

4. **View Results**: Displays relevant information fetched from webpages and GPT-4 generated summaries.

## Dependencies

```bash
pip install requests beautifulsoup4 g4f google nltk
```
-------------------
Feel free to contribute, report issues, or suggest improvements to make the GoogleGPT project even more user-friendly and reliable.
