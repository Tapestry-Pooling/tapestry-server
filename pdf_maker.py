import json
import re
import os
import requests
# https://pyfpdf.readthedocs.io
from fpdf import FPDF

BATCH_REGEX = r'(\d+)x(\d+).*'
PDF_ROOT = f"{os.path.expanduser('~')}/pdfs"
# COLORS
BLACK = (0, 0, 0)
DARK = (64, 64, 64)
WHITE = (255, 255, 255)
LIGHT_GREY = (151, 151, 151)
GRAY = (240, 240, 240)

def parse_batch(batch):
    mat = re.match(BATCH_REGEX, batch)
    if mat:
        return int(mat[1]),int(mat[2])
    return None

def partition(l, n):
    return [l[i * n:(i + 1) * n] for i in range((len(l) + n - 1) // n )]

class CustomPDF(FPDF):
    def __init__(self, batch, grid_data):
        # Landscape mode
        FPDF.__init__(self, orientation='L', unit='mm', format='A4')
        self.grid_data = grid_data['gridData']
        self.code_name = grid_data['codename']
        self.batch = batch
        self.num_wells, self.num_samples = parse_batch(batch)
        self.make_table()

    def header(self):
        # Set up a logo
        # self.image('snakehead.png', 10, 8, 33)
        self.set_font('Arial', '', 14)
        self.set_text_color(80, 80, 80)
        self.cell(10)
        self.cell(60, 5, f'{self.num_samples} Samples', 0)
        self.cell(30)
        self.cell(30, 5, f'{self.num_wells} Wells', 0)
        self.cell(30)
        self.cell(30, 5, f'Matrix: {self.code_name}', 0)
        # Add a page number
        self.cell(40)
        page = f'Page {self.page_no()}'
        self.cell(20, 5, page, 0, 0)
        # Line break
        self.ln(15)
    
    def make_table(self):
        g = [a['screenData'] for a in self.grid_data]
        samples = list(range(1, len(g)+1))
        max_l = max(len(c) for c in g)
        tables_per_page = 3 if max_l < 4 else 2
        rows_per_table = 15
        screen_partitions = partition(g, tables_per_page * rows_per_table)
        sample_partitions = partition(samples, tables_per_page * rows_per_table)
        ww = 17
        hh = 10
        self.set_text_color(*BLACK)
        for i in range(len(screen_partitions)):
            self.add_page()
            a = screen_partitions[i]
            b = sample_partitions[i] # Sample numbers
            tlist = partition(a, rows_per_table)
            slist = partition(b, rows_per_table)
            # Border color
            self.set_draw_color(*LIGHT_GREY)

            for j in range(len(tlist)):
                # Print sample numbers
                self.set_font('Arial', 'B', 11)
                self.set_text_color(*WHITE)
                self.set_fill_color(*DARK)
                self.cell(25, hh, f'Samples', 1, fill=True, align='C')
                for x in slist[j]:
                    self.cell(ww, hh, f'{x}', 1, fill=True, align='C')
                self.ln(hh)
                tt = tlist[j]
                self.set_fill_color(*GRAY)
                self.set_text_color(*BLACK)
                for k in range(max_l):
                    if k == 0:
                        self.cell(25, hh*max_l, f'Wells', 1, fill=True, align='C')
                    else:
                        self.cell(25, hh)
                    self.set_font('Arial', '', 12)
                    for i, x in enumerate(tt):
                        self.set_fill_color(*(GRAY if i%2 == 1 else WHITE))
                        if len(x) < max_l:
                            if type(x) == str:
                                x = []
                            x += ['' for _ in range(max_l - len(x))]
                        self.cell(ww, hh, x[k], 1, fill=True, align='C')
                    self.ln(hh)
                self.ln(20)

def create_pdf(batch):
    grid_resp = requests.get(f'https://c19.zyxw365.in/api/grid_data/{batch}').json()
    code_name = grid_resp['codename']
    pdf = CustomPDF(batch, grid_resp)    
    pdf.output(get_pdf_location(batch))

def get_pdf_location(batch):
    return f'{PDF_ROOT}/batch_{batch}_Sheet.pdf'

def generate_pdfs():
    batches = requests.get(f'https://c19.zyxw365.in/api/debug_info').json()['matrix_labels']
    for b in batches:
        print(f'Batch : {b}')
        create_pdf(b)

if __name__ == "__main__":
    generate_pdfs()
