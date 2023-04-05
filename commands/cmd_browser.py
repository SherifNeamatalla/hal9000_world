from commands.cmd_interface import ICmd
from util.browse import scrape_text, summarize_text, scrape_links


class CmdBrowser(ICmd):
    def execute(self, cmd_args, cmd_type='search'):
        if cmd_type == 'search':
            return self.browse_website(cmd_args['url'], cmd_args['question'])
        pass

    def browse_website(self, url, question):
        summary = self.get_text_summary(url, question)
        links = self.get_hyperlinks(url)

        # Limit links to 5
        if len(links) > 5:
            links = links[:5]

        result = f"""Website Content Summary: {summary}\n\nLinks: {links}"""

        return result

    def get_text_summary(self, url, question):
        text = scrape_text(url)
        summary = summarize_text(text, question)
        return """ "Result" : """ + summary

    def get_hyperlinks(self, url):
        link_list = scrape_links(url)
        return link_list
