# Brochure Generator

The **Brochure Generator** is a Python-based application that takes a website URL, fetches all its links, retrieves relevant data from the pages, and creates a short brochure about the company in markdown format. This application uses web scraping to gather content and utilizes a language model (LLM) to process the information into a readable brochure.

## Test It Out
[Test it on HuggingFace Spaces](https://huggingface.co/spaces/onurnsfw/brochures_generator) with your own GROQ_API_KEY

## Preview
![alt text](https://github.com/OnurAsimIlhan/brochures_generator/blob/main/br.png)
## Features

- **Website Scraping**: Fetches and processes the content of a website to retrieve the relevant details, excluding irrelevant pages like terms of service and privacy policies.
- **LLM Integration**: Uses a powerful language model (e.g., Groq, Llama, Mixtral) to create summaries and generate a well-structured brochure in markdown format.
- **Gradio Interface**: A simple user interface that allows you to input the company name, website URL, select an LLM model, and provide your Groq API key.
- **Markdown Output**: Generates the brochure in markdown format, making it easy to share and edit.

## Requirements

- Python 3.7+
- Install the required Python libraries using pip:

  ```bash
  pip install requests beautifulsoup4 langchain-groq gradio
  pip install -r requirements.txt
