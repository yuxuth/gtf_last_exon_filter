import queue
import sys

#
# @author: Fabian Friedrich
# 2019.10.09
#

if len(sys.argv) >= 3:

    with open(sys.argv[1], "r") as read_file, open(sys.argv[2], "w") as write_file:
        if len(sys.argv) >= 4:
            maxSize = int(sys.argv[3])
        else:
            maxSize = 1

        queue = queue.Queue(maxSize)
        tmp = read_file.readline()
        array = tmp.split("\t")

        count = 0

        while tmp != "":

            if tmp.startswith("#"):
                write_file.writelines(tmp)
                tmp = read_file.readline()
                array = tmp.split("\t")

            elif array[2] == "exon":
                if queue.full():
                    queue.get()

                queue.put(tmp)

                tmp = read_file.readline()
                array = tmp.split("\t")

            elif 'transcript' == array[2] or 'gene' == array[2]:
                while not queue.empty():
                    write_file.writelines(queue.get())

                write_file.writelines(tmp)
                tmp = read_file.readline()
                array = tmp.split("\t")
            else:
                tmp = read_file.readline()
                array = tmp.split("\t")

        while not queue.empty():
            write_file.writelines(queue.get())

    read_file.close()
    write_file.close()

else:
    print("""
        #############################
        Usage: python3 filter_last_exons.py reading.gtf writing.gtf number_of_exons

        reading.gtf     : your gtf file with all the exons, has to be in the gtf file format
        writing.gtf     : will be generated with only the last exons from the transcripts
        number_of_exons : the amount of exons, automatically set to one
        
        comments (starts with '#') will be copied
        genes, transcripts and exons will be copied
        everything else will be removed
        #############################    
    """)