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
        with open(export_dir + rp_csv, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                print(f'\t{row["Title"]} has the identifier {row["ItemNumber"]} and was kept in the {row["LibraryName"]} library.')
                line_count += 1
            print(f'Processed {line_count} lines.')
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
