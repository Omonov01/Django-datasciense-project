from django.shortcuts import render
from .models import Product,Purchase
import pandas as pd
from .utils import get_simple_plot
from .forms import PurchaseForm
# Create your views here.
def chart_select_view(request):
    error_message = None
    df = None
    graph = None
    price = None
    product_df = pd.DataFrame(Product.objects.all().values())
    purchase_df = pd.DataFrame(Purchase.objects.all().values())
    product_df["product_id"] = product_df["id"]
   
    
    if purchase_df.shape[0] > 0:
        df = pd.merge(product_df,purchase_df,on="product_id").drop(["id_y","date_y"],axis=1).rename({"id_x":"id","date_x":"date"},axis=1)
        price = df["price"]
        if request.method == "POST":
            chart_type = request.POST.get('sales')
            date_from = request.POST["date_from"]
            date_to = request.POST["date_to"]
            df["date"] = df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
            df2 = df.groupby("date",as_index=False)['total_price'].agg("sum")
            # print(df["date"])
            if chart_type != "":
                if date_from != "" and date_to != "":
                    df = df[(df['date']>date_from) & (df["date"]<date_to)]
                    df2 = df.groupby("date",as_index=False)['total_price'].agg("sum")
                    # print(df2)
                    # print(df)
                graph = get_simple_plot(chart_type, x=df2['date'],y=df2['total_price'],data=df)
            else:
                error_message = "Iltimos jadval turini aniq tanlang va sanalarni to'iq kiriting"

    else:
        error_message = "Databaseda malumot topilmadi"
        

    context = {
        # "products":product_df.to_html(),
        # "purchase":purchase_df.to_html(),
        # "df":df.to_html(),
        "graph":graph,
        "price":price,
        "error_message":error_message,
    }
    return render(request,"products/main.html",context)

def add_purchase_view(request):
    form = PurchaseForm(request.POST or None)
    added_message = None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.salesman = request.user
        obj.save()

        form = PurchaseForm()
        added_message = "Savdo natijalari qo'shildi"

    context = {
        "form":form,
        "added_message":added_message,
    }
    return render(request,"products/add.html",context)
