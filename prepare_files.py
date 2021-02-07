import os
from shutil import rmtree, copyfile
from make_clippings import MakeClippings


class PrepareFiles():
    def __init__(self, path_clippings):
        print("--------------- Preparing the files ---------------")
        # file names
        self.folder_name_extracted_clippings = "clippings"
        self.folder_name_previous_clippings = "donotdelete"
        self.path_clippings = path_clippings
        self.path_previous_clippings = "{}/PreviousClippings.txt".format(
            self.folder_name_previous_clippings)
        self.path_difference_file = "diff.txt"

        self.book_and_author = {}
        self.diff_clippings_used = False

    def _make_folder(self):
        """
        Make a clippings folder in which all the extracted clippings will go. If already present from previous run it will
        be deleted and an empty folder will be made.
        """
        if os.path.exists(self.folder_name_extracted_clippings):
            rmtree(self.folder_name_extracted_clippings)
        os.mkdir(self.folder_name_extracted_clippings)

    def file_copy(self):
        """
        At the end copy the clippings file that was provided and save it inside donotdelete folder.
        """
        if os.path.exists(self.folder_name_previous_clippings):
            rmtree(self.folder_name_previous_clippings)
        os.mkdir(self.folder_name_previous_clippings)
        copyfile(self.path_clippings, self.path_previous_clippings)

    def _diff_clippings(self):
        """
        Generate diff.txt between the new file provided and the previous file saved.
        Some assumptions have been made
        - The new file provided will always have more clippings than the previous one
        - Once your clippings have been synced try not to delete them in kindle as it create problems for the new highlights
        - Some new ones might be missed because of the nature of the code
        """
        # this will decide if diff.txt has to be used or the given file
        self.diff_clippings_used = True

        file_recent = open(self.path_clippings, mode="r").readlines()
        file_previous = open(self.path_previous_clippings,
                             mode="r").readlines()
        file_diff = open(self.path_difference_file, mode="w+")
        for i in range(len(file_previous), len(file_recent)):
            file_diff.write(file_recent[i])

    def _extract(self):
        """
        Calls the MakeClippings to populate the clippings folder 
        """
        path_to_be_extracted = self.path_difference_file if self.diff_clippings_used else self.path_clippings
        make_clippings = MakeClippings(
            clippings_file=path_to_be_extracted, clippings_folder=self.folder_name_extracted_clippings)
        make_clippings.make_separate_files()
        self.book_and_author = make_clippings.book_and_author
        if self.diff_clippings_used:
            os.remove("diff.txt")

    def extract_clippings(self):
        """
        This function is used to call all the functions
        """
        # make a folder named clippings in which all the clippings will be stored
        self._make_folder()
        # check if PreviousClippings.txt is present or not
        if os.path.exists(self.path_previous_clippings):
            self._diff_clippings()
        # extract the clippings to the clippings folder
        self._extract()

