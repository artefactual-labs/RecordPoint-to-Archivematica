import sys
import os
import csv
import shutil


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

    try:
        files = os.listdir(export_dir)
    except FileNotFoundError:
        print("Error: that data directory does not exist.")
        return

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

    # Parse out the SharePoint transfer directory name to use for the
    # Archivematica transfer sub-directory name. Look for the last
    # (sub)directory in the supplied directory path.
    transfer_dir = export_dir[:-1]  # Remove the last slash on the path.
    reverse_transfer_dir = transfer_dir[::-1]
    try:
        slash = reverse_transfer_dir.index("/")  # find the last slash on path
        transfer_dir = 'data/archivematica-transfers/' + transfer_dir[-slash:] + '/'
    except ValueError:
        # No path slash found. The transfer directory is on the same path as
        # this script.
        transfer_dir = 'data/archivematica-transfers/' + export_dir
    if not os.path.exists(transfer_dir + '/metadata'):
        os.makedirs(transfer_dir + '/metadata')

    try:
        with open(export_dir + rp_csv, mode='r') as rp_csv_file:
            csv_reader = csv.DictReader(rp_csv_file)
            file_count = 0

            # TODO: try to sort files into archivematica-transfer directories
            # by SharePoint sites

            # Create metadata.csv file for writing RecordPoint values.
            with open(transfer_dir + '/metadata/metadata.csv', mode='w') as archivematica_csv_file:
                csv_writer = csv.writer(archivematica_csv_file, delimiter=',')
                csv_writer.writerow(['dc.title', 'dc.identifier', 'dc.identifier', 'dc.creator', 'dc.contributor', 'dc.date', 'dc.format', 'dc.description', 'record category', 'vital record', 'content type name', 'library name', 'site name', 'location', 'content version', 'file size', 'file type', 'created date', 'last modified', 'streamhash'])

                for row in csv_reader:
                    if row["Title"] in files:
                        '''Files with 'Destroy' retention are listed in the CSV
                        file but are not included in the export directory.
                        Therefore, only write new rows if a SharePoint file is
                        present in the transfer.
                        '''

                        csv_writer.writerow(['objects/' + row["Title"], row["ItemNumber"], row["UniqueId"], row["Author"], row["Editor"], row["TrueDocumentDate"], row["Format"], row["DocumentType"], row["RecordCategory"], row["VitalRecord"], row["ContentTypeName"], row["LibraryName"], row["SiteName"], row["Location"], row["ContentVersion"], row["File_x0020_Size"], row["File_x0020_Type"], row["Created_x0020_Date"], row["Last_x0020_Modified"], row["StreamHash"]])

                        # Move SharePoint file to AM transfer directory
                        shutil.copy(export_dir + row["Title"], transfer_dir + row["Title"])

                        file_count += 1
                print(f'Added {file_count} files to ' + transfer_dir)

    except Exception as e:
        print("Error: cannot parse or move the files: " + str(e))


if __name__ == "__main__":
    """To run the script, provide the export directory's relative location as
    a parameter e.g.
    `python rm-2-am.py data/sharepoint-exports/2021-03-02_10-24`
    """

    # TODO: add a `-d` flag and delete the sharepoint-export directory if it
    # is set to TRUE.

    try:
        parse_rp_exports(str(sys.argv[1]))
    except IndexError:
        print("Error: no directory name given.")
