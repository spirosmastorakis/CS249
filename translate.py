import csv,sys

def translate_input(path):
    with open(path[0], "r") as fi, open(path[1], 'w') as fo:
        reader = csv.reader(fi)
        next(fi)
        for row in reader:
            print row[0]
            paperid_list = row[1].split(" ")
            pair_list = [[int(row[0]), int(elem)] for elem in paperid_list]

            transformed_list = list(sum(pair_list, []))            
            
            for i,val in enumerate(transformed_list):
                # print val
                if i%2 == 1:
                    fo.write(str(val) + '\n')
                else:
                    fo.write(str(val) + ' ')
            

def main(argv):
    if len(argv) != 1 + 2:
        print >> sys.stderr, 'Usage : %s Target.csv Transformed.txt' % (argv[0],)
        return -1
    
    translate_input((argv[1],argv[2]))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))