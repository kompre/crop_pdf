import os
import subprocess
import click
import sys
import pdfCropMargins


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


def crop_pdf_file(pdf_file, source, destination, margins, threshold, keep_files):
    """Crop a single PDF file."""
    output_dir = destination or source
    output_file = os.path.join(output_dir, os.path.basename(pdf_file))

    # Ensure the destination directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Construct the command to crop PDF using pdfCropMargins
    pdfCropMargins.crop([
        "-p", margins,
        "-t", threshold,
        pdf_file,
        "-o", output_file
    ])    

    click.echo(f'\tCropped: {os.path.relpath(pdf_file):30s} to {os.path.relpath(output_file):30s}')
    if pdf_file != output_file and not keep_files:
        os.remove(pdf_file)


@click.command(help='Crop PDF files and save the cropped files to the destination directory.')
@click.argument('sources', nargs=-1, type=click.Path(exists=True, resolve_path=True))
@click.option('--destination', '-d', help='Output directory for cropped PDFs. Defaults to the same as source.')
@click.option('--margins', '-m', default="5", help='White margin in percentage of remaining border.')
@click.option('--threshold', '-t', default="255", help='threshold for pixel being considered white (0-255).')
@click.option('--keep-files', '-k', is_flag=True, help='Do not delete original PDFs.')
@click.option('--recursive', '-r', is_flag=True, help='Process directories recursively.')
def crop_pdf(sources, destination, margins, threshold, keep_files, recursive):
    """Crop PDF files in the given sources and save the cropped files to the
    destination directory."""
    if not sources and len(sys.argv) == 1:
        click.echo(click.get_current_context().get_help())
        return

    for source in sources:
        if not destination:
            destination = source

        # Ensure the destination directory exists
        os.makedirs(destination, exist_ok=True)

        pdf_files = get_pdf_files(source, recursive=recursive)
        if not pdf_files:
            click.echo(f'No PDF files found in {source}')
            continue
        if os.path.isfile(source):
            source = os.path.dirname(source)
        for pdf_file in pdf_files:
            crop_pdf_file(pdf_file, source, destination, margins, threshold, keep_files)


if __name__ == '__main__':
    crop_pdf()
