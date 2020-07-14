import requests
from bs4 import BeautifulSoup
import pickle
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sys



class horoscopSource:
    headers = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'

    def __init__(self,website_name, website_url, website_css_ref,website_header=headers):
        self.name = website_name
        self.url = website_url
        self.ref = website_css_ref
        self.header = website_header
        self.result = ''

    def data_download(self):
        response = requests.get(self.url, headers={'User-Agent' : self.header})
        response_html = response.text
        soup_response = BeautifulSoup(response_html, "html.parser")
        self.result = soup_response.select_one(self.ref).text
        self.result = "".join([s for s in self.result.splitlines(True) if s.strip("\r\n")])

    def data_print(self):
        self.data_download()
        print('#'*30,'\n',self.name,'\n\n',self.result,'\n',sep='',end='')


def store_list(site_list):
    """Store list of website objects"""
    pickling_on = open("site_data.pickle", "wb")
    pickle.dump(site_list, pickling_on)
    pickling_on.close()


def load_list():
    """Load list of website objects for processing"""
    try:
        pickle_off = open("site_data.pickle", "rb")
        site_data_unpickle = pickle.load(pickle_off)
    except FileNotFoundError:
        site_data_unpickle = []
    return site_data_unpickle


def view_horoscop():

    horoscop_window = Toplevel(root)
    horoscop_window.title('Horoscopul zilei')
    horoscop_window.grab_set()
    horoscop_window.geometry("700x600+50+50")
    frame_horoscop = ttk.Frame(horoscop_window)
    frame_horoscop.pack(ipadx=10, ipady=10, fill=BOTH, expand=1, anchor='center')

    def go_back():
        horoscop_window.destroy()

    back_button = ttk.Button(frame_horoscop, text="Inapoi", command=go_back)
    back_button.grid(column=0, row=0, padx=(10, 10), pady=(10, 10), sticky='w')

    title_label1 = ttk.Label(frame_horoscop, text='Horoscopul zilei')
    title_label1.grid(column=1, row=0, padx=(10, 10), pady=(10, 10), columnspan=1, sticky='w')
    title_label1.config(font=('Arial', 20, 'bold'), anchor='center')
    frame_results = ttk.Frame(frame_horoscop)
    frame_results.grid(padx=(10,0), row=1, column=0, columnspan=2)

    text_horoscop = Text(frame_results, width=80, height=30, font=('Arial', 14))
    text_horoscop.pack(side=LEFT, fill=BOTH)
    text_horoscop.config(wrap='word')
    scrollbar = ttk.Scrollbar(frame_results, command=text_horoscop.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    text_horoscop['yscrollcommand'] = scrollbar.set

    site_list = load_list()

    if len(site_list) == 0:
        text_horoscop.insert('1.0','Nu aveti nici un site adaugat.')
    else:
        for site in site_list:
            try:
                site.data_download()
                text = '#'*30 + '\n' + site.name + '\n' + site.result + '\n\n'
            except:
                text = '#'*30 + '\n' + site.name + ' - Eroare - verificati detaliile' + '\n'
            text_horoscop.insert(END,text)

    text_horoscop.config(state=DISABLED)

    frame_start.config(borderwidth=2, relief=RIDGE)


def edit_sources():

    sources_window = Toplevel(root)
    sources_window.title('Editare surse')
    sources_window.grab_set()
    sources_window.geometry("400x330+50+50")
    frame_sources = ttk.Frame(sources_window)
    frame_sources.pack(ipadx=10, ipady=10, fill=BOTH, expand=1, anchor='center')

    site_list = load_list()
    name_list = [site.name for site in site_list]

    def go_back():
        sources_window.destroy()

    def refresh_fields(e):
        for site in site_list:
            if site.name == combobox_sources.get():
                entry_name.delete(0,END)
                entry_url.delete(0,END)
                entry_selector.delete(0,END)
                entry_header.delete(0,END)
                entry_name.insert(0, site.name)
                entry_url.insert(0, site.url)
                entry_selector.insert(0, site.ref)
                entry_header.insert(0, site.header)
                return

    def add_source():
        if entry_name.get() == '':
            messagebox.showerror('Eroare','Numele trebuie completat!')
            return
        elif entry_url.get() == '':
            messagebox.showerror('Eroare','URL trebuie completat!')
            return
        elif entry_selector.get() == '':
            messagebox.showerror('Eroare','Selector trebuie completat!')
            return
        for site in site_list:
            if site.name == entry_name.get():
                messagebox.showerror('Eroare','Numele exista deja in baza de date. Alegeti alt nume!')
                return
        if entry_header.get() == '':
            new_source = horoscopSource(entry_name.get(),entry_url.get(),entry_selector.get())
        else:
            new_source = horoscopSource(entry_name.get(),entry_url.get(),entry_selector.get(),entry_header.get())
        site_list.append(new_source)
        store_list(site_list)
        messagebox.showinfo('Succes','Site-ul a fost adaugat cu succes!')
        entry_name.delete(0, END)
        entry_url.delete(0, END)
        entry_selector.delete(0, END)
        entry_header.delete(0, END)
        name_list = [site.name for site in site_list]
        combobox_sources['values'] = name_list

    def save_source():
        if entry_name.get() == '':
            messagebox.showerror('Eroare','Numele trebuie completat!')
            return
        elif entry_url.get() == '':
            messagebox.showerror('Eroare','URL trebuie completat!')
            return
        elif entry_selector.get() == '':
            messagebox.showerror('Eroare','Selector trebuie completat!')
            return
        for site in site_list:
            if site.name == combobox_sources.get():
                site.name = entry_name.get()
                site.url = entry_url.get()
                site.ref = entry_selector.get()
                site.header = entry_header.get()
                messagebox.showinfo('Succes', 'Site-ul a fost modificat cu succes!')
                entry_name.delete(0, END)
                entry_url.delete(0, END)
                entry_selector.delete(0, END)
                entry_header.delete(0, END)
                break
        name_list = [site.name for site in site_list]
        combobox_sources['values'] = name_list
        combobox_sources.set('')
        store_list(site_list)

    def delete_source():
        response = messagebox.askyesno('Confirmare','Sunteti sigur ca vreti sa stergeti acest site?')
        if (response):
            for site in site_list:
                if site.name == combobox_sources.get():
                    site_list.remove(site)
                    messagebox.showinfo('Succes', 'Site-ul a fost sters!')
                    entry_name.delete(0, END)
                    entry_url.delete(0, END)
                    entry_selector.delete(0, END)
                    entry_header.delete(0, END)
                    break
            name_list = [site.name for site in site_list]
            combobox_sources['values'] = name_list
            combobox_sources.set('')
            store_list(site_list)

    back_button = ttk.Button(frame_sources, text="Inapoi", command=go_back)
    back_button.grid(column=0, row=0, padx=(10, 10), pady=(10, 10), sticky='w')

    title_label1 = ttk.Label(frame_sources, text='Editare surse')
    title_label1.grid(column=1, row=0, padx=(10, 10), pady=(10, 10), columnspan=2, sticky='nsew')
    title_label1.config(font=('Arial', 20, 'bold'), anchor='center')

    label_sources = ttk.Label(frame_sources, text="Alege sursa:")
    label_sources.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky='nsew')

    site_list = load_list()
    name_list = [site.name for site in site_list]
    combobox_sources = ttk.Combobox(frame_sources, values=name_list)
    combobox_sources.grid(row=1, column=1, columnspan=2, sticky='w', padx=(10, 10), pady=(10, 10))
    combobox_sources.bind('<<ComboboxSelected>>', refresh_fields)

    ttk.Label(frame_sources, text="Nume:").grid(row=2, column=0, padx=(10, 10), pady=(10, 2), sticky='nsew')
    ttk.Label(frame_sources, text="URL:").grid(row=3, column=0, padx=(10, 10), pady=(0, 2), sticky='nsew')
    ttk.Label(frame_sources, text="Selector:").grid(row=4, column=0, padx=(10, 10), pady=(0, 2), sticky='nsew')
    ttk.Label(frame_sources, text="Header:").grid(row=5, column=0, padx=(10, 10), pady=(0, 2), sticky='nsew')
    entry_name = ttk.Entry(frame_sources, width=20)
    entry_name.grid(row=2, column=1, columnspan=2, sticky='w', padx=(10, 10), pady=(10, 2))
    entry_url = ttk.Entry(frame_sources, width=20)
    entry_url.grid(row=3, column=1, columnspan=2, sticky='w', padx=(10, 10), pady=(0, 2))
    entry_selector = ttk.Entry(frame_sources, width=20)
    entry_selector.grid(row=4, column=1, columnspan=2, sticky='w', padx=(10, 10), pady=(0, 2))
    entry_header = ttk.Entry(frame_sources, width=20)
    entry_header.grid(row=5, column=1, columnspan=2, sticky='w', padx=(10, 10), pady=(0, 2))

    add_button = ttk.Button(frame_sources, text="Adauga", command=add_source)
    add_button.grid(row=6, column=0, padx=(10, 10), pady=(10, 10), sticky='nsew')
    save_button = ttk.Button(frame_sources, text="Salveaza", command=save_source)
    save_button.grid(row=6, column=1, padx=(10, 10), pady=(10, 10), sticky='nsew')
    delete_button = ttk.Button(frame_sources, text="Sterge", command=delete_source)
    delete_button.grid(row=6, column=2, padx=(10, 10), pady=(10, 10), sticky='nsew')


if __name__ == '__main__':

    root = Tk()
    root.title('Horoscopul zilei')
    root.geometry("400x330+50+50")

    frame_start = ttk.Frame(root)
    frame_start.pack(ipadx=10, ipady=10, fill=BOTH, expand=1, anchor='center')
    logo = PhotoImage(file='scorpio4.gif').subsample(2,2)
    ttk.Label(frame_start, image=logo).grid(column=0, row=0, padx=(10, 10), pady=(10, 10), columnspan=3, sticky='n')

    title_label = ttk.Label(frame_start, text='Horoscopul zilei')
    title_label.grid(column=0, row=1, padx=(10, 10), pady=(10, 10), columnspan=3, sticky='nsew')
    title_label.config(font=('Arial', 20, 'bold'), anchor='center')

    view_button = ttk.Button(frame_start, text="Horoscop", command=view_horoscop)
    view_button.grid(column=0, row=2, padx=(10, 10), pady=(10, 10), sticky='nsew')

    edit_button = ttk.Button(frame_start, text="Editare surse", command=edit_sources)
    edit_button.grid(column=1, row=2, padx=(10, 10), pady=(10, 10), sticky='nsew')

    exit_button = ttk.Button(frame_start, text="Exit", command=lambda: sys.exit())
    exit_button.grid(column=2, row=2, padx=(10, 10), pady=(10, 10), sticky='nsew')

    frame_start.config(borderwidth=2, relief=RIDGE)

    root.mainloop()
