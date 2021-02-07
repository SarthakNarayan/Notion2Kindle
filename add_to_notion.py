from notion.client import NotionClient
from notion.block import QuoteBlock, TextBlock
from notion.collection import NotionDate
from tqdm import tqdm
from utilities import getBookCoverUri, no_cover_img
from datetime import datetime


class AddToNotion():
    def __init__(self, token_v2, database_url, book_and_author, clippings_folder, use_location, type_block):
        print("--------------- Transferring Data to Notion ---------------")
        self.available_blocks = [QuoteBlock, TextBlock]
        self.type_block = type_block
        self.client = NotionClient(token_v2=token_v2)
        self.book_and_author = book_and_author
        self.cv = self.client.get_collection_view(database_url)
        self.clippings_folder = clippings_folder
        self.use_location = use_location

    def _logger(self, title):
        print("Transferring data for {}".format(title))

    def _get_all_rows(self):
        """
        Returns a dictionary with the full title as key and id of that block as value
        """
        all_rows = {}
        for row in self.cv.collection.get_rows():
            all_rows[row.full_title] = row
        return all_rows

    def _already_present_insertion(self, title, reference):
        self._logger(title)
        self._write_to_notion(title=title, reference=reference)

    def _write_to_notion(self, title, reference):
        file = open(
            '{}/{}.txt'.format(self.clippings_folder, title), 'r').readlines()
        for line in tqdm(file):
            if self.use_location:
                new_line = "{} ({})".format(line.split(
                    ':loco:')[0], line.split(':loco:')[1].strip())
            else:
                new_line = "{}".format(line.split(':loco:')[0])
            reference.children.add_new(
                self.available_blocks[self.type_block], title=new_line)

    def _new_insertion(self, title):
        self._logger(title)
        row = self.cv.collection.add_row()
        row.name = title.split(':')[0]
        row.author = self.book_and_author[title]
        row.full_title = title
        row.last_synced = NotionDate(datetime.now())
        self._write_to_notion(title=title, reference=row)

    def _get_covers(self):
        all_rows = self.cv.collection.get_rows()
        print("Generating book covers...")
        for record in tqdm(all_rows):
            if record.cover is None:
                result = getBookCoverUri(record.full_title, record.author)
                if result is not None:
                    record.cover = result
                    record.icon = result
                    print("✓ Book Cover has been set for {}".format(
                        record.full_title))
                else:
                    record.cover = no_cover_img
                    record.icon = no_cover_img
                    print(
                        "× Book Cover coulnd't be found. Please replace the placeholder image with original bookcover manually for", record.full_title)

    def transfer(self):
        all_rows = self._get_all_rows()

        for title in self.book_and_author.keys():
            if title in list(all_rows.keys()):
                self._already_present_insertion(
                    title=title, reference=all_rows[title])
            else:
                self._new_insertion(title=title)

        self._get_covers()
