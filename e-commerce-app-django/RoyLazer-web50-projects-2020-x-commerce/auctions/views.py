from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User, Products, Categories, Watchlist, comments
from django import forms




class CreateNew(forms.Form):
    pname = forms.CharField(label="Choose a title for your listing", widget=forms.TextInput(attrs={'placeholder': 'Insert title....','class':'mb-4 form-control'}))
    pimage = forms.CharField(label="Put your image link here", widget=forms.TextInput(attrs={'placeholder': 'Insert image link....','class':'mb-4 form-control'}))
    pbid = forms.IntegerField(label="Insert the first bid", widget=forms.NumberInput(attrs={'placeholder': 'Insert initial bid....','class':'mb-4 form-control'}))
    pdescription = forms.CharField(label="Write a description", widget=forms.Textarea(attrs={'placeholder': 'Insert a comment.....','class':'form-control mb-4'}))
    pcategory = forms.CharField(label="Write a Category for your product", widget=forms.TextInput(attrs={'placeholder': 'Examples: Kitchen, Office, Home....','class':'mb-4 form-control'}))
    #pcategory = forms.ChoiceField(label="Category", choices = tuple(Categories.objects.values_list('id', 'category_name')), widget=forms.Select(attrs={'class':'mb-4 form-control'}) ) // this is to populate the categories
    pactive = forms.BooleanField(label = "Active the listing", initial=None, widget=forms.CheckboxInput(attrs={'class':'mb-4'}))
class listingForm(forms.Form):
    pbid = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'class':'mb-4 form-control 50'}))

class commentForm(forms.Form):
    pcomments = forms.CharField(label="Write a comment", widget=forms.Textarea(attrs={'placeholder': 'Insert a comment.....','class':'form-control mb-4'}))


def index(request):
    return render(request, "auctions/index.html",{
        "elements":Products.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def watchlist(request):
    user = Watchlist.objects.filter(user_id=request.user.id)
    return render(request, "auctions/watchlist.html",{
             "elements": user
    })


def create_view(request):
    if request.method == "POST":
        form = CreateNew(request.POST)
        if form.is_valid():
            pname = form.cleaned_data["pname"]
            pimage = form.cleaned_data["pimage"]
            pbid = form.cleaned_data["pbid"]
            pdescription = form.cleaned_data["pdescription"]
            pcategory = form.cleaned_data["pcategory"]
            pactive = form.cleaned_data["pactive"]
            try:
                findcategory = Categories.objects.filter(category_name=pcategory)
                if findcategory.count() == 0:
                    newCategory(pcategory)
                rcategory = Categories.objects.get(category_name=pcategory)
                ruser = User.objects.get(pk=request.user.id)
                prod = Products(name_product=pname, image=pimage,bid = pbid,owner= ruser,last_user_bid = ruser,description=pdescription, category=rcategory , active=pactive)
                prod.save()
                return render(request, "auctions/index.html",{
                    "elements":Products.objects.all()
                })
            except:
                return render(request, "auctions/error.html",{
                    "error":"Error, Insert correct information"
                })
    return render(request, "auctions/create.html",{
        "form":CreateNew
    })

def newCategory(category_name):
    new = Categories(category_name = category_name)
    new.save()


def categories(request):
    elements = Categories.objects.all()
    return render(request, "auctions/categories.html",{
        "elements": elements
    })

def filter(request, category_name):
    objects  = Products.objects.filter(category=category_name)
    return render(request, "auctions/index.html",{
             "elements": objects
    })



def listings(request, product_id):
    #Know if the user is the owner of the product and display the active checkbox
    ID = request.user.id
    prod = Products.objects.filter(id = product_id, owner = ID)
    owner = None;
    status = None;
    if prod.count() > 0:
        owner = True;
    isWinner = Products.objects.filter(id=product_id,last_user_bid = ID)
    if isWinner.count() > 0:
        status = True;

    if request.method == "POST":
        if 'watchList' in request.POST: #If watchlist is pressed
            addUser = User.objects.get(pk=request.user.id)
            addProduct = Products.objects.get(id=product_id)
            query = Watchlist.objects.filter(product_id=addProduct, user_id=addUser)
            if query.count() == 0:
                watchlist = Watchlist(product_id=addProduct, user_id=addUser)
                watchlist.save()
                user = Watchlist.objects.filter(user_id=request.user.id)
                return render(request, "auctions/watchlist.html",{
                  "elements": user
                 })
            else:
                return render(request, "auctions/error.html",{
                    "error":"Item already in your watchlist"
                })        
        elif 'placeBid' in request.POST: #If place bid is pressed
           # element =  Products.objects.filter(id=product_id)
            return render(request, "auctions/listing.html",{
                "elements": Products.objects.filter(id=product_id),
                "bidForm": listingForm,
                "commentForm": commentForm,
                "comments": comments.objects.filter(product_id=product_id),
                "isOwner": owner,
                "status": status
     
            })
    return render(request, "auctions/listing.html",{
        "elements": Products.objects.filter(id=product_id),
        "bidForm": listingForm,
        "commentForm": commentForm,
        "comments": comments.objects.filter(product_id=product_id),
        "isOwner": owner,
        "status": status
    })

def newBid(request, product_id):
        if request.method == "POST":
            form = listingForm(request.POST)
            if form.is_valid():
                newbid = form.cleaned_data["pbid"]
                Product = Products.objects.get(id=product_id)
                oldbid = Product.bid
            
                if newbid > oldbid:
                    Products.objects.filter(id=product_id).update(bid=newbid,last_user_bid = request.user.id)
                    return redirect(listings, product_id=product_id)
                else:
                 return render(request, "auctions/error.html",{
                    "error":"Please, place a bid bigger than the actual one"
                })



def newComment(request, product_id):
    if request.method == "POST":
        form = commentForm(request.POST)
        if form.is_valid():
            commment = form.cleaned_data["pcomments"]
            ruser = User.objects.get(pk=request.user.id)
            productid = Products.objects.get(id=product_id)
            thiscomment = comments(user_id=ruser, product_id=productid,comment=commment)
            thiscomment.save()
            return redirect(listings, product_id=product_id)         
            
    return redirect(listings, product_id=product_id)

def active(request, product_id):
    if request.method == "POST":
        if 'deactivebut' in request.POST:
            Products.objects.filter(id=product_id).update(active=False)
        elif 'activebut' in request.POST:
            Products.objects.filter(id=product_id).update(active=True)
        return redirect(listings, product_id=product_id)

    return redirect(listings, product_id=product_id)
