import sys
import os
import csv


def parse_rp_exports(export_directory):
    """Convert a directory containing a RecordPoint CSV file and SharePoint
    binary files into Archivematica-ready transfer directories.
    """

    try:
        export_dir = sys.argv[1]
        if export_dir[-1] != "/":
            export_dir += "/"
    except FileNotFoundError:
        print("Error: cannot find data directory.")
        return

    files = os.listdir(export_dir)
    if len(files) == 0:
        print("Error: the directory does not contain any files.")
        return

    rp_csv = None
    for file in files:
        if file[:34] == "SharePoint-Disposition-Trigger-CSV":
            rp_csv = file
            break
    if rp_csv is None:
        print("Error: cannot find a SharePoint-Disposition-Trigger CSV file.")
        return

    try:
        with open(export_dir + rp_csv, mode='r') as rp_csv_file:
            csv_reader = csv.DictReader(rp_csv_file)
            file_count = 0

            if not os.path.exists('transfers'):
                os.makedirs('transfers')

            '''
            TODO: slice out RP export directory name from export_dir to use
            as Archivematica transfer directory name: 'transfers/2021-03-02_10-24/metadata.csv'
            '''

            with open('metadata.csv', mode='w') as archivematica_csv_file:
                csv_writer = csv.writer(archivematica_csv_file, delimiter=',')
                csv_writer.writerow(['dc.title', 'dc.identifier', 'dc.identifier', 'dc.creator', 'dc.contributor', 'dc.date', 'dc.format', 'dc.description', 'record category', 'vital record', 'location', 'content version', 'content type name', 'created date', 'file size', 'file type', 'last modified', 'library name', 'site name', 'streamhash', 'document type'])

                #TODO: seperate try/except blocks for read & write

                for row in csv_reader:
                    # files with 'Destroy' retention are listed in the CSV file
                    # but are not included in the export directory.
                    if row["Title"] in files:

                        #TODO: write row to metadata.csv

                        print(f'\t{row["Title"]} has the identifier {row["ItemNumber"]} and was kept in the {row["LibraryName"]} library.')
                        #TODO: add file move to AM transfer directory

                        #TODO: try to sort files by SharePoint library
                        file_count += 1
                print(f'Added {file_count} files to ...') #TODO add tranfer directory name

                # TODO add `-d` flag to command and function parameters. Delete
                # the RP transfer directory if set.

    except Exception as e:
        print("Error: cannot parse the SharePoint-Disposition-Trigger CSV file: " + str(e))


if __name__ == "__main__":
    """To run the script, provide the export directory's relative location as
    a parameter e.g. `python rm-2-am.py data/2021-03-02_10-24`
    """

    try:
        parse_rp_exports(str(sys.argv[1]))
    except IndexError:
        print("Error: no directory name given.")
