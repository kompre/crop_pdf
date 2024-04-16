import os
import subprocess
import click


def get_pdf_files(source, recursive=True):
    """Get list of PDF files in the given directory."""
    pdf_files = []
    if recursive:
        for root, _, files in os.walk(source):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
    else:
        if os.path.isdir(source):
            for file in os.listdir(source):
                if file.endswith('.pdf'):
                    pdf_files.append(os.path.join(source, file))
    return pdf_files


def crop_pdf_file(pdf_file, source, destination, margins, keep_files):
    """Crop a single PDF file."""
    # Compute the relative path of the PDF file with respect to the source directory
    relative_path = os.path.relpath(pdf_file, source)

    # Construct the output directory and output file paths
    output_dir = os.path.join(destination, os.path.dirname(relative_path))
    output_file = os.path.join(output_dir, os.path.basename(pdf_file))

    # Replace backslashes with forward slashes in paths
    pdf_file = pdf_file.replace(os.sep, '/')
    output_file = output_file.replace(os.sep, '/')

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    subprocess.run(['pdfcrop', f'--margins={margins}', pdf_file, output_file], capture_output=True)
    click.echo(f'\tCropped: {os.path.relpath(pdf_file):30s} to {os.path.relpath(output_file):30s}')
    if pdf_file != output_file and not keep_files:
        os.remove(pdf_file)


@click.command()
@click.argument('sources', nargs=-1, type=click.Path(exists=True, resolve_path=True))
@click.option('--destination', '-d', help='Output directory for cropped PDFs.')
@click.option('--margins', '-m', default=5, help='White margin in pixels.')
@click.option('--keep-files', '-k', is_flag=True, help='Do not delete original PDFs.')
@click.option('--recursive', '-r', is_flag=True, help='Process directories recursively.')
def crop_pdf(sources, destination, margins, keep_files, recursive):
    """Crop PDF files in the given sources and save the cropped files to the
    destination directory."""
    # Set destination directory, default is current directory
    if not destination:
        destination = os.getcwd()

    for source in sources:
        # Process directories recursively if the recursive option is enabled
        pdf_files = get_pdf_files(source, recursive=recursive)
        if not pdf_files:
            click.echo(f'No PDF files found in {source}')
            continue
        if os.path.isfile(source):
            source = os.path.dirname(source)
        for pdf_file in pdf_files:
            crop_pdf_file(pdf_file, source, destination, margins, keep_files)


if __name__ == '__main__':
    crop_pdf()
