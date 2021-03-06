#%%
import os
from os import path
import subprocess
import inspect
import sys
import click

#%% argomenti di sistema

@click.command(
    # help='''trova tutti i file pdf nella cartella seleziona e li ritaglia mantenendo il margine desiderati'''
)
# @click.option('--source', '-s', default='.', help='cartella contentente i pdf da croppare')
@click.argument('source', nargs=-1)
@click.option('--destination', '-d', help='cartella di salvataggio dei file croppati')
@click.option('--margins', '-m', default=5, help='margine bianco in px')
@click.option('--keep_files', '-k', is_flag=True, default=False, help='non cancella i file originali (nel caso di source diverso da destination)')
def croppdf(source, destination, margins, keep_files):
    """
    trova tutti i file pdf nella cartella seleziona e li ritaglia mantenendo il margine desiderato.
    È possibile specificare:
        - un file pdf
        - più file pdf
        - la cartella dove risiedono i file

    """
    filename = '' 
    # verifica se source è un file invece che una cartella
    
    for src in source:

        if os.path.isfile(src):
            filename, _ = os.path.splitext(os.path.basename(src))
            src = os.path.dirname(os.path.abspath(src))
            # print(filename, source)
        
        # trova i file .pdf nella cartella; lista di os.DirEntry
        filtro = filename + '.pdf'
        fl = list( filter(lambda x: x.is_file and filtro in x.name, os.scandir(src)))
        if len(fl) == 0:
            return print('### file pdf non trovati ###')



        if not destination:
            destination = src

        out_path = os.path.normpath(os.path.join(os.getcwd(), destination))
        # print(out_path)

        try:
            os.mkdir(out_path)
        except:
            pass

        print(f'New cropped file in: (margins={margins})\n')
        for f in fl:
            # print(out_path)
            _out_path = os.path.join(out_path, os.path.basename(f))
            print(f'{_out_path}')
            subprocess.run([
                'pdfcrop',
                f'--margins={margins}',
                f, _out_path
                ], 
                capture_output=True
                )
            
            if os.path.samefile(src, destination):
                keep_files = True
            
            if not keep_files:
                os.remove(f.path)
        print('')

# croppdf('./t.txt', destination='.', margins=5, keep_files=False)
