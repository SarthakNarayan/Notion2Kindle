import re


class MakeClippings():
    def __init__(self, clippings_file, clippings_folder):
        self.clippings_file = clippings_file
        self.clippings_folder = clippings_folder
        self.book_and_author = {}

    def _get_location(self, text):
        """
        Get the location from the text
        """
        split_text = text.split()
        location_index = split_text.index("Location")
        return split_text[location_index + 1]

    def _get_author_and_title(self, text):
        """
        Should be of the form given below otherwise there will be problems
        Sapiens: A Brief History of Humankind (Yuval Noah Harari)
        """
        split_text = re.split(r'\((.*)\)', text)
        title = split_text[0].strip().replace(u'\ufeff', '')
        author = split_text[1]
        return title, author

    def _create_file(self, title):
        file = open("{}/{}.txt".format(self.clippings_folder, title), "a")
        file.close()

    def _print_stats(self):
        print("No of highlights")
        for i in list(self.book_and_author.keys()):
            file = open(
                '{}/{}.txt'.format(self.clippings_folder, i), 'r').readlines()
            print("{} => {}".format(i, len(file)))

    def make_separate_files(self):
        """
        Make separate files out of the single file based on Name of the book
        """
        file = open(self.clippings_file, "r")
        all_lines = file.readlines()
        for i in range(0, len(all_lines), 5):
            title, author = self._get_author_and_title(all_lines[i].strip())
            if author not in self.book_and_author.keys():
                self.book_and_author[title] = author
                self._create_file(title)

            location = self._get_location(all_lines[i+1].strip())
            file = open("clippings/{}.txt".format(title), "a")
            # adding a custom location splitter which can be extracted easily using split
            file.write(all_lines[i+3].strip() +
                       ":loco:{}".format(location)+'\n')
            file.close()

        # for printing the stats like no of highlights for each book
        self._print_stats()
