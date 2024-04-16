import os
from os import path
import subprocess
import click


@click.command()
@click.argument('sources', nargs=1)  # Paths to PDF files or directories
@click.option('--destination', '-d', help='Output directory for cropped PDFs.')
@click.option('--margins', '-m', default=5, help='White margin in pixels.')
@click.option('--keep-files', '-k', is_flag=True, help='Do not delete original PDFs.')
def crop_pdf(sources, destination, margins, keep_files):
    """Crop PDF files in the given sources and save the cropped files to the
    destination directory.

    Args:
        sources (List[str]): Paths to PDF files or directories.
        destination (str): Output directory for cropped PDFs.
        margins (int): White margin in pixels.
        keep_files (bool): Do not delete original PDFs.
    """
    # Set destination directory, default is current directory
    if not destination:
        destination = os.getcwd()

    if isinstance(sources, str):
        sources = [sources]
    
    # Iterate over sources
    for source in sources:
        # If source is a file, get its directory
        if os.path.isfile(source):
            source = os.path.dirname(os.path.abspath(source))

        # Get list of PDF files in source
        pdf_files = [
            os.path.join(root, file) for root, _, files in os.walk(source)
            for file in files if file.endswith('.pdf')]

        # If no PDF files found, print message and break
        if not pdf_files:
            print('### No PDF files found ###')
            break

        # Create output directory with source name
        output_dir = os.path.join(destination, os.path.basename(source))
        os.makedirs(output_dir, exist_ok=True)

        # Print message with margins
        print(f'New cropped files in: (margins={margins})\n')

        # Iterate over PDF files
        for pdf_file in pdf_files:
            # always use / as path separator
            pdf_file = pdf_file.replace(os.sep, '/')
            
            # Create output file path
            output_file = os.path.join(output_dir, *os.path.basename(pdf_file).split(os.sep))
            
            #always use / as path separator
            output_file = output_file.replace(os.sep, '/')
            print(output_file)

            # Crop PDF using pdfcrop and delete original if keep_files is False
            subprocess.run([
                'pdfcrop',
                f'--margins={margins}',
                pdf_file, output_file
                ],
                capture_output=False)

            if pdf_file != output_file and not keep_files:
                os.remove(pdf_file)


        # Print newline
        print('')

if __name__ == '__main__':
    crop_pdf()