import os
import subprocess

def compress_pdf(in_path: str, out_path, power=0, bin_path='gs'):
    # pdf compress quality
    quality = {
        0: '/default',
        1: '/prepress',
        2: '/printer',
        3: '/ebook',
        4: '/screen'
    }
    # check if the input file exist and it's pdf
    if not os.path.isfile(in_path):
        print("Error: Input file not found !")
        return
    
    if in_path.split('.')[-1].lower() != 'pdf':
        print("Error: Input file is not pdf !")
        return

    print("Compressing..")

    command = [bin_path, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                    '-dPDFSETTINGS={}'.format(quality[power]),
                    '-dNOPAUSE', '-dQUIET', '-dBATCH',
                    '-sOutputFile={}'.format(out_path), in_path]

    subprocess.call(command)

    # compression details
    init_size = os.path.getsize(in_path)
    final_size = os.path.getsize(out_path)
    ratio = 1 - (init_size / final_size)
    print("Compression by {0:.0%}.".format(ratio))
    print("Final file size is {0:.1f}MB".format(final_size / 1000000))

