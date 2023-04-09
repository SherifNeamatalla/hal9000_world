from langchain.agents import tool, load_tools

from util.browse import scrape_text, summarize_text, scrape_links


def get_hyperlinks(url):
    link_list = scrape_links(url)
    return link_list


def get_text_summary(url, question):
    text = scrape_text(url)
    summary = summarize_text(text, question)
    return """ "Result" : """ + summary


@tool("Browser")
def browse_website(url, question):
    """Browse a google search result and answers a question about it."""
    load_tools()
    summary = get_text_summary(url, question)
    links = get_hyperlinks(url)

    # Limit links to 5
    if len(links) > 5:
        links = links[:5]

    result = f"""Website Content Summary: {summary}\n\nLinks: {links}"""

    return result


browser_tools = [

]
