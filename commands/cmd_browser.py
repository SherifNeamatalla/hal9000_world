from commands.cmd_interface import ICmd
from util.browse import scrape_text, summarize_text, scrape_links


class CmdBrowser(ICmd):
    def execute(self, cmd_args, cmd_type='search'):
        if cmd_type == 'search':
            return browse_website(cmd_args['url'], cmd_args['question'])


def get_hyperlinks(url):
    link_list = scrape_links(url)
    return link_list


def get_text_summary(url, question):
    text = scrape_text(url)
    summary = summarize_text(text, question)
    return """ "Result" : """ + summary


def browse_website(url, question):
    summary = get_text_summary(url, question)
    links = get_hyperlinks(url)

    # Limit links to 5
    if len(links) > 5:
        links = links[:5]

    result = f"""Website Content Summary: {summary}\n\nLinks: {links}"""

    return result
