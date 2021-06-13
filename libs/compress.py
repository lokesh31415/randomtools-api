import os
import subprocess

class CompressionException(Exception):
    """
    Raised when an error occured in compression logic.
    """    
    def __init__(self, message="Compression failed !") -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message

def compress_pdf(in_path: str, out_path: str, power: int=0, bin_path='gs'):
    """
    Uses GhostScript program to perform PDF compression.

    Args:
        in_path (str): Complete path of the input file.
        out_path (str): Path to store the output file.
        power (int, optional): Compression quality. Defaults to 0.
        bin_path (str, optional): Path of the ghostscript to use. Defaults to 'gs'.

    Raises:
        CompressionException: when input file not found.
        CompressionException: when output file not found.
        CompressionException: when system not able to run the ghostscript command.

    Returns:
        Tuple(float, float): 'final_size_mb' - compressed file size in Mega Bytes, 'ratio' - compression ratio.
    """      

    if power not in [0, 1, 2, 3, 4]:
        power = 0

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
        raise CompressionException("Input file not found !")
        
    if in_path.split('.')[-1].lower() != 'pdf':
        raise CompressionException("Input file is not pdf !")

    try:
        command = [bin_path, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                        '-dPDFSETTINGS={}'.format(quality[power]),
                        '-dNOPAUSE', '-dQUIET', '-dBATCH',
                        '-sOutputFile={}'.format(out_path), in_path]
        subprocess.call(command)
    except Exception as e:
        raise CompressionException(message="Error in executing ghostscript !")

    # compression details
    init_size = os.path.getsize(in_path)
    final_size = os.path.getsize(out_path)
    ratio = 1 - (init_size / final_size)
    final_size_mb =  final_size / 1000000
    return final_size_mb, ratio

