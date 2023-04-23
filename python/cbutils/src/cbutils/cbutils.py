import glob
import shutil
import os
from pdf2image import convert_from_path, convert_from_bytes


# main entry
def run_help():
    print("Hello !")
    pass


def run_compress():
    print("Hello !")
    pass


def run_folder_pdfs_2_cbz(dir_name):
    full_name = dir_name + "/" + "*.pdf"
    full_list = glob.glob(full_name)
    for file in full_list:
        print('Processing file :'+file)
        run_pdf_2_cbz(file)
    pass


def run_pdf_2_cbz(full_name):
    file_name = os.path.basename(full_name)
    last_name = os.path.splitext(full_name)
    first_name = file_name.strip(last_name[1]).lstrip().rstrip()

    dir_name = os.path.dirname(full_name)
    target_dir = dir_name + '/' + first_name
    os.mkdir(target_dir)
    pages = convert_from_path(full_name, 150, poppler_path=r'./poppler/bin')
    counter = 0
    for page in pages:
        counter_str = f'{counter:04d}'
        page.save(target_dir + '/' + first_name + '_{}.jpg'.format(counter_str), 'JPEG')
        counter += 1
        pass
    new_file = shutil.make_archive(target_dir, 'zip', dir_name, target_dir)
    shutil.move(new_file, dir_name + '/' + first_name + '.cbz')
    shutil.rmtree(target_dir)
    pass


def run_rar_2_zip():
    print("Hello !")
    pass


if __name__ == "__main__":
    folder = 'D:/tmp'
    run_folder_pdfs_2_cbz(folder)
