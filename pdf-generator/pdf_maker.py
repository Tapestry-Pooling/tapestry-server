import json
import re

import requests
from fpdf import FPDF

BATCH_REGEX = r'(\d+)x(\d+).*'

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
        self.code_name = grid_data['codeName']
        self.batch = batch
        self.num_wells, self.num_samples = parse_batch(batch)
        self.make_table()

    def header(self):
        # Set up a logo
        # self.image('snakehead.png', 10, 8, 33)
        self.set_font('Arial', '', 14)
        self.set_text_color(80, 80, 80)
        self.cell(10)
        #self.set_fill_color(128, 113, 113)
        self.cell(60, 5, f'{self.num_samples} Samples', 0)
        self.cell(30)
        #self.set_fill_color(22, 243, 90)
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
        ww = 15
        hh = 10
        self.set_text_color(0, 0, 0)
        for i in range(len(screen_partitions)):
            self.add_page()
            a = screen_partitions[i]
            b = sample_partitions[i] # Sample numbers
            tlist = partition(a, rows_per_table)
            slist = partition(b, rows_per_table)
            for j in range(len(tlist)):
                # Print sample numbers
                self.set_font('Arial', 'B', 12)
                self.set_fill_color(255, 204, 102)
                self.cell(25, hh, f'Samples', 1, fill=True, align='C')
                for x in slist[j]:
                    self.cell(ww, hh, f'{x}', 1, fill=True, align='C')
                self.ln(hh)
                tt = tlist[j]
                if (len(tt)) < rows_per_table:
                    tt = tt + ['' for x in range(rows_per_table - len(tt))]
                self.set_font('Arial', '', 12)
                self.set_fill_color(153, 170, 255)
                #self.set_fill_color(153, 153, 255)
                for k in range(max_l):
                    if k == 0:
                        self.cell(25, hh*max_l, f'Wells', 1, fill=True, align='C')
                    else:
                        self.cell(25, hh)
                    self.set_font('Arial', '', 12)
                    for x in tt:
                        self.cell(ww, hh, x[k], 1, fill=True, align='C')
                    self.ln(hh)
                self.ln(hh)

        
    def footer(self):
        self.set_y(-10)

def create_pdf(batch):
    grid_resp = requests.get(f'https://c19.zyxw365.in/api/grid_data/{batch}').json()
    pdf = CustomPDF(batch, grid_resp)
    pdf.output(f'tab_{batch}.pdf')

batch = '20x1140_v0'
create_pdf(batch)

