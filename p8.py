from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import requests

root=Tk()
root.geometry("700x700+300+50")
root.title("💱 Currency Convetor")
root.configure(bg="linen")
root.resizable(False,False)
f=("Arial",40,"bold")

# UI Design
lab_title=Label(root,text="💱 Currency Convetor",font=f,bg="black",fg="white")
lab_title.pack(fill=X)

#Entry frame
frame=Frame(root,bg="#ffffff",bd=2,relief=SOLID)
frame.pack(pady=20,padx=40,fill=X)

lab_amount=Label(frame,text="Amount:",font=("Arial",20,"bold"),bg="white")
lab_amount.grid(row=0,column=0,padx=10,pady=15,sticky="w")
amount_entry=Entry(frame,font=("Arial",20,"bold"),bg="white",fg="black",relief=SOLID)
amount_entry.grid(row=0,column=1,padx=15,pady=15)

lab_from=Label(frame,text="From Currency:",font=("Arial",20,"bold"),bg="white")
lab_from.grid(row=1,column=0,padx=10,pady=15,sticky="w")
from_currency=ttk.Combobox(frame,font=("Arial",20,"bold"),state="readonly",width=18)
from_currency.grid(row=1,column=1, padx=10, pady=15)

lab_to=Label(frame,text="To Currency:",font=("Arial",20,"bold"),bg="white")
lab_to.grid(row=2,column=0,padx=10,pady=15,sticky="w")
to_currency=ttk.Combobox(frame,font=("Arial",20,"bold"),state="readonly",width=18)
to_currency.grid(row=2,column=1, padx=10, pady=15)

#Output
result_var=StringVar()
result_label=Label(root,textvariable=result_var,font=("Arial",20,"bold"),bg="linen",fg="black")
result_label.pack(pady=20)


# Functions

def fetch_currency_list():
	try:
		url="https://api.exchangerate-api.com/v4/latest/USD"
		res=requests.get(url)
		res.raise_for_status()
		data=res.json()
		rates=data.get("rates")
		if not rates:
			raise Exception("Currency Data no available")
		
		symbols=sorted(rates.keys())
		from_currency["values"]=symbols
		to_currency["values"]=symbols
		from_currency.set("INR")
		to_currency.set("USD")
		
	except Exception as e:
		showerror("Issue",e)

#Def convert currency

def convert_currency():
	try:
		amt=float(amount_entry.get())
		from_cur=from_currency.get()
		to_cur=to_currency.get()

		if from_cur=="" or to_cur=="":
			showerror("Input Error","Please select the both Currencies")
			return
		url=f"https://api.exchangerate-api.com/v4/latest/{from_cur}"
		res=requests.get(url)
		res.raise_for_status()
		data=res.json()

		rate=data["rates"].get(to_cur)
		if rate is None:
			raise Exception(f"Conversion rate for {to_cur} not found.")

		converted=amt * rate
		result_var.set(f"{amt:.2f} {from_cur} = {converted:.2f} {to_cur}\n(1 {from_cur} = {rate:.4f} {to_cur})")		


	except ValueError:
		showerror("Invalis input","Please enter a valid number")
	except Exception as e:
		showerror("Conversion error",e)

# Swap currencies

def swap_currencies():
	f=from_currency.get()
	t=to_currency.get()
	from_currency.set(t)
	to_currency.set(f)

#clear all
def clear_all():
	amount_entry.delete(0,END)
	result_var.set("")





#Buttons

btn_convert=Button(root,text="Convert",font=("Arial",25,"bold"),bg="black",fg="red",width=8,command=convert_currency)
btn_convert.place(x=30,y=500)
btn_swap=Button(root,text="Swap",font=("Arial",25,"bold"),bg="black",fg="red",width=8,command=swap_currencies)
btn_swap.place(x=265,y=500)
btn_clear=Button(root,text="Clear",font=("Arial",25,"bold"),bg="black",fg="red",width=8,command=clear_all)
btn_clear.place(x=500,y=500)



# Init
fetch_currency_list()




root.mainloop()