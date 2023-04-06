import json
import os

from duckduckgo_search import ddg
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from commands.cmd_interface import ICmd


class CmdGoogle(ICmd):
    def execute(self, cmd_args, cmd_type='search'):
        if cmd_type == 'search':
            return self.search(cmd_args)
        pass

    def search(self, cmd_args):
        if os.getenv("GOOGLE_API_KEY"):
            return self.google_official_search(cmd_args["input"])
        else:
            return self.google_search(cmd_args["input"])

    @staticmethod
    def google_search(query, num_results=8):
        search_results = []
        for j in ddg(query, max_results=num_results):
            search_results.append(j)

        return json.dumps(search_results, ensure_ascii=False, indent=4)

    @staticmethod
    def google_official_search(query, num_results=5):

        try:
            # Get the Google API key and Custom Search Engine ID from the config file
            api_key = os.getenv("GOOGLE_API_KEY")
            custom_search_engine_id = os.getenv("CUSTOM_SEARCH_ENGINE_ID")

            # Initialize the Custom Search API service
            service = build("customsearch", "v1", developerKey=api_key)

            # Send the search query and retrieve the results
            result = service.cse().list(q=query, cx=custom_search_engine_id, num=num_results).execute()

            # Extract the search result items from the response
            search_results = result.get("items", [])

            # Create a list of only the URLs from the search results
            search_results_links = [item["link"] for item in search_results]

        except HttpError as e:
            # Handle errors in the API call
            error_details = json.loads(e.content.decode())

            # Check if the error is related to an invalid or missing API key
            if error_details.get("error", {}).get("code") == 403 and "invalid API key" in error_details.get("error",
                                                                                                            {}).get(
                "message", ""):
                return "Error: The provided Google API key is invalid or missing."
            else:
                return f"Error: {e}"

        # Return the list of search result URLs
        return search_results_links
