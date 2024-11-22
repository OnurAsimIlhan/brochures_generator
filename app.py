## Creating Brochure App that takes a website, fetches all links and retrieves data from all and then creates a brochure with all the data
from bs4 import BeautifulSoup
import requests
import json
import gradio as gr
from langchain_groq import ChatGroq
import os
# A class to represent a Webpage

class Website:
    """
    A utility class to represent a Website that we have scraped, now with links
    """

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""
        links = [link.get('href') for link in soup.find_all('a')]
        self.links = [link for link in links if link]

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

## Check whether the links are relevant or not
def get_links_system_prompt(website):
    link_system_prompt = "You are provided with a list of links found on a webpage. \
    You are able to decide which of the links would be most relevant to include in a brochure about the company, \
    such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
    link_system_prompt += "You should respond in JSON as in this example, do not say anything else:"
    link_system_prompt += """
    {
        "links": [
            {"type": "about page", "url": "https://full.url/goes/here/about"},
            {"type": "careers page": "url": "https://another.full.url/careers"}
        ]
    }
    """
    return link_system_prompt

def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

def get_relevant_links(url, llm):
    website=Website(url)
    messages = [
        ("system", get_links_system_prompt(website)),
        ("human", get_links_user_prompt(website))
    ]
    result = llm.invoke(messages)
    return json.loads(result.content)

def get_all_details(url, llm):
    result = "Landing page:\n"
    result += Website(url).get_contents()
    links = get_relevant_links(url, llm)
    print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result

def get_brochure_system_prompt():
    system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
    and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
    Include details of company culture, customers and careers/jobs if you have the information."
    return system_prompt

def get_brochure_user_prompt(company_name, url, llm):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url,llm)
    user_prompt = user_prompt[:20_000] # Truncate if more than 20,000 characters
    return user_prompt

def create_brochure(company_name, url, llm_choice, groq_api_key):
    # Set the Groq API key dynamically
    os.environ["GROQ_API_KEY"] = groq_api_key
    llm = ChatGroq(model=llm_options[llm_choice])
    messages = [
        ("system", get_brochure_system_prompt()),
        ("human", get_brochure_user_prompt(company_name, url, llm))
    ]
    # Process the stream and return the result
    return llm.invoke(messages).content


llm_options = {
    "Gemma2":"gemma2-9b-it",
    "LLama": "llama-3.2-3b-preview",
    "Mixtral": "mixtral-8x7b-32768"
}

# Gradio interface
demo = gr.Interface(
    fn=create_brochure,
    inputs=[
        "text",  # Company name input
        "text",  # URL input
        gr.Dropdown(choices=list(llm_options.keys()), label="Select LLM"),  # LLM selection
        gr.Textbox(type="password", label="Enter Groq API Key")  # API Key input
    ],
    outputs="markdown",  # Output format
    title="Brochure Generator",
    description="Generate brochures by selecting a company name, URL, and LLM. Provide your Groq API Key."
)

demo.launch()
