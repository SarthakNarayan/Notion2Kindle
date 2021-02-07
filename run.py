from add_to_notion import AddToNotion
from prepare_files import PrepareFiles
from decouple import config

CLIPPINGS = PrepareFiles(path_clippings=config('PATH_CLIPPINGS'))
CLIPPINGS.extract_clippings()

token_v2 = config('TOKEN')
database_url = config('DATABASE_URL')
use_location = True if config('USE_LOCATION') == 'True' else False
type_block = int(config('TYPE_BLOCK'))
book_and_author = CLIPPINGS.book_and_author
clippings_folder = CLIPPINGS.folder_name_extracted_clippings

NOTION = AddToNotion(
    token_v2=token_v2, database_url=database_url, book_and_author=book_and_author, clippings_folder=clippings_folder, use_location=use_location, type_block=type_block)
NOTION.transfer()

# make a copy at the end so that if some error occurs there will be no previous clippings
CLIPPINGS.file_copy()
