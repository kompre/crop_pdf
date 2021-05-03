#%%
import os
import subprocess
import inspect
import sys
import click

#%% argomenti di sistema

@click.command(
    # help='''trova tutti i file pdf nella cartella seleziona li ritaglia mantenendo il margine desiderati'''
)
@click.option('--source', '-s', default='.', help='cartella contentente i pdf da croppare')
@click.option('--destination', '-d', help='cartella di salvataggio dei file croppati')
@click.option('--margins', '-m', default=5, help='margine bianco in px')
@click.option('--keep_files', '-k', is_flag=True, default=False, help='non cancella i file originali (nel caso di source diverso da destination)')
def croppdf(source, destination, margins, keep_files):
    # trova i file .pdf nella cartella; lista di os.DirEntry
    fl = list( filter(lambda x: x.is_file and '.pdf' in x.name, os.scandir(source)))

    if not destination:
        destination = source

    out_path = os.path.normpath(os.path.join(os.getcwd(), destination))

    try:
        os.mkdir(out_path)
    except:
        pass

    for f in fl:
        # print(out_path)
        _out_path = os.path.join(out_path, os.path.basename(f))
        print(_out_path)
        subprocess.run([
            'pdfcrop',
            f'--margins={margins}',
            f, _out_path
            ], 
            capture_output=True
            )
        
        if os.path.samefile(source, destination):
            keep_files = True
        
        if not keep_files:
            os.remove(f.path)
