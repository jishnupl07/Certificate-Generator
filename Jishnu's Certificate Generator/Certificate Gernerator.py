from reportlab.pdfgen import canvas as pdf_canvas
from PyPDF2 import PdfReader, PdfWriter
import csv
import os
from tkinter import *
from tkinter import messagebox

def generate_certificate():
    global window
    Create_Btn.destroy()

    # Determine the size of the template PDF
    template_pdf_path = r'Certificate Template\certificate_template.pdf'
    with open(template_pdf_path, 'rb') as template_file:
        template_reader = PdfReader(template_file)
        template_page = template_reader.pages[0]
        pdf_width = template_page.mediabox.width
        pdf_height = template_page.mediabox.height

    # Create and configure canvas

    canvas = Canvas(window, bg="#FFD4B7", width=pdf_width, height=pdf_height)
    canvas.pack(expand=True, fill=BOTH)

    frame1 = Frame(canvas, bg="#371F11")
    canvas.create_window((0, 0), window=frame1, anchor='nw')

    # Add a scrollbar
    scrollbar = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Configure canvas to use scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Coordinates for text (x, y) and font size
    name_coords = (350, 300)
    class_coords = (550, 300)
    position_coords = (650, 300)
    font_size = 20

    # Read the CSV file using the csv module
    csv_file_path = r'Certificate_details.csv'  # Ensure the correct path to your CSV file

    # Open the CSV file
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the header row

        # Count the number of rows
        row_count = sum(1 for row in reader)
        csvfile.seek(0)
        next(reader)  # Skip the header row again

        # Process each student
        for row_index, row in enumerate(reader):
            student_name = row[0]  # Assuming 'Name' is the first column
            student_class = row[1]  # Assuming 'Class' is the second column
            student_position = row[2]  # Assuming 'Position' is the third column

            label1 = Label(frame1, text=student_name, bg="#371F11", fg="white")
            label2 = Label(frame1, text=student_class, bg="#371F11", fg="white")
            label3 = Label(frame1, text=student_position, bg="#371F11", fg="white")

            label1.grid(row=row_index, column=0, padx=40, pady=5)
            label2.grid(row=row_index, column=1, padx=40, pady=5)
            label3.grid(row=row_index, column=2, padx=40, pady=5)

            # Create a temporary PDF to hold the text overlay
            temp_text_pdf_path = 'temp_text.pdf'
            c = pdf_canvas.Canvas(temp_text_pdf_path, pagesize=(pdf_width, pdf_height))
            c.setFont("Helvetica", font_size)

            # Draw text on the canvas at the specified coordinates
            c.drawString(name_coords[0], name_coords[1], student_name)
            c.drawString(class_coords[0], class_coords[1], student_class)
            c.drawString(position_coords[0], position_coords[1], student_position)
            c.save()

            # Merge the template PDF with the text PDF
            with open(template_pdf_path, 'rb') as template_file, open(temp_text_pdf_path, 'rb') as temp_file:
                template_reader = PdfReader(template_file)
                temp_reader = PdfReader(temp_file)
                writer = PdfWriter()

                # Add the template page
                template_page = template_reader.pages[0]

                # Create a new page for the text overlay
                temp_page = temp_reader.pages[0]

                # Merge the pages
                template_page.merge_page(temp_page)
                writer.add_page(template_page)

                # Save the new PDF with the student's name in the filename
                output_filename = rf"Generated Certificates\{student_name}_Certificate.pdf"
                with open(output_filename, 'wb') as output_file:
                    writer.write(output_file)

    messagebox.showinfo('Generation Status', 'Certificates Generated Successfully')
    
    # Cleanup temporary PDF
    os.remove('temp_text.pdf')
    
    # Create the back button
    back_button = Button(window, text="BACK", command=lambda: [canvas.destroy(), create_window()])
    back_button.pack(side = LEFT,padx = 30)
    close_button = Button(window,text = 'CLOSE',command = lambda: [window.destroy()])
    close_button.pack(side = RIGHT,padx = 30)


def create_window():
    global window, Create_Btn

    if "window" in globals():
        window.destroy()
        
    window = Tk()
    window.title("Jishnu's Certificate Generator")
    window.geometry('400x300')
    window.resizable(False, False)
    window.config(bg='#FFD4B7')
    Create_Btn = Button(window, text='Generate Certificates',font = ('Helvatica',15), command=generate_certificate)
    Create_Btn.place(x=200, y=150, anchor=CENTER)
    close_button = Button(window,text = 'CLOSE',command = lambda: [window.destroy()])
    close_button.place(x = 200, y = 250,anchor = CENTER)
    window.mainloop()

create_window()
