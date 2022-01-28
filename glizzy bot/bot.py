import discord
import requests
import urllib.request
from discord.ext import commands

client = commands.Bot(command_prefix="`", help_command = None)

placehold = []

# Takes in the tuple, converts it into a list, uses join to convert into string
def tuple_to_string(tup):
    for element in tup:
        if element is int or float or complex:
            placehold.append(str(element))
        else:
            placehold.append(element)
    return("".join(placehold))

@client.command()
async def help(ctx, arg):
    if arg == "convert": 
        embedhelp = discord.Embed(title = "convert", description = "This command takes in two currencies and a value. It converts the value from the first currency to the second currency.")
        embedhelp.add_field(name = "Here is a list of ISO codes supported that can be used with the convert command: ", value = "\u200b", inline = False)
        embedhelp.add_field(name = "Fiat Currency", value = ", ".join(fiat), inline = False)
        embedhelp.add_field(name = "Cryptocurrency", value = ", ".join(crypto), inline= False)
        await ctx.send(embed = embedhelp)

@client.event
async def on_ready():
    print("glizzy bot is ready")

@client.command()
async def space(ctx, arg):
    request = requests.get("http://api.open-notify.org/astros.json")
    request = request.json()
    response = request[arg]
    await ctx.send(response)

nomicskey = "f5a8e7287a7ee55d69e028c1d3c54102"
crypto = ["BTC", "ETH", "DOGE", "LCC", "GRLC"]
fiat = ["AED","AFN","ALL","AMD","ANG","AOA","ARS","AUD","AWG","AZN",
"BAM","BBD","BDT","BGN","BHD","BIF","BMD","BND","BOB","BOV","BRL","BSD","BTN","BWP","BYN","BZD",
"CAD","CDF","CHE","CHF","CHW","CLF","CLP","CNY","COP","COU","CRC","CUC","CUP","CVE","CZK",
"DJF","DKK","DOP","DZD",
"EGP","ERN","ETB","EUR",
"FJD","FKP","GBP","GEL","GHS","GIP","GMD","GNF","GTQ","GYD",
"HKD","HNL","HRK","HTG","HUF",
"IDR","ILS","INR","IQD","IRR","ISK",
"JMD","JOD","JPY",
"KES","KGS","KHR","KMF","KPW","KRW","KWD","KYD","KZT",
"LAK","LBP","LKR","LRD","LSL","LYD",
"MAD","MDL","MGA","MKD","MMK","MNT","MOP","MRU","MUR","MVR","MWK","MXN","MXV","MYR","MZN",
"NAD","NGN","NIO","NOK","NPR","NZD",
"OMR",
"PAB","PEN","PGK","PHP","PKR","PLN","PYG",
"QAR",
"RON","RSD","RUB","RWF",
"SAR","SBD","SCR","SDG","SEK","SGD","SHP","SLL","SOS","SRD","SSP","STN","SVC","SYP","SZL",
"TBH","TJS","TMT","TND","TOP","TRY","TTD","TWD","TZS",
"UAH","UGX","USD","USN","UYI","UYU","UYW","UZS",
"VES","VND","VUV",
"WST",
"XAF","XAG","XAU","XBA","XBB","XBC","XBD","XCD","XDR","XOF","XPD","XPF","XPT","XSU","XTS","XUA","XXX",
"YER",
"ZAR","ZMW","ZWL"]

@client.command()
async def convert(ctx, *args):
    value = float(args[0])
    currency1 = args[1].upper()
    currency2 = args[2].upper()

    if currency1 in crypto and currency2 in fiat:
        cryptoreq = requests.get("https://api.nomics.com/v1/currencies/ticker?key=" + nomicskey + "&ids=" + currency1 + "&interval=1d,30d&convert=" + currency2)
        cryptoreq = cryptoreq.json()
        price = float(cryptoreq[0]["price"])
        time = cryptoreq[0]["price_timestamp"]
        date = cryptoreq[0]["price_date"]
        ans = value * price
        embedconvert = discord.Embed(title = str(value) + " " + currency1 + " to " + currency2, description = str(ans) + " " + currency2)
        embedconvert.add_field(name = "Time", value = time, inline = True)
        embedconvert.add_field(name = "Date", value = date, inline = True)
        await ctx.send(embed = embedconvert)
    elif currency1 in fiat and currency2 in crypto:
        cryptoreq = requests.get("https://api.nomics.com/v1/currencies/ticker?key=" + nomicskey + "&ids=" + currency2 + "&interval=1d,30d&convert=" + currency1)
        cryptoreq = cryptoreq.json()
        price = float(cryptoreq[0]["price"])
        time = cryptoreq[0]["price_timestamp"]
        date = cryptoreq[0]["price_date"]
        ans = value / price
        embedconvert = discord.Embed(title = str(value) + " " + currency1 + " to " + currency2, description = str(ans) + " " + currency2)
        embedconvert.add_field(name = "Time", value = time, inline = True)
        embedconvert.add_field(name = "Date", value = date, inline = True)
        await ctx.send(embed = embedconvert)
    elif currency1 in crypto and currency2 not in fiat:
        embedconvert = discord.Embed(title = currency2 + " is not supported or has the wrong ISO code.", description = "Here is a list of possible ISO codes: " + ", ".join(fiat))
        await ctx.send(embed = embedconvert)
    elif currency1 in fiat and currency2 not in crypto:
        embedconvert = discord.Embed(title = currency2 + " is not supported or has the wrong ISO code.", description = "Here is a list of possible ISO codes: " + ", ".join(crypto))
        await ctx.send(embed = embedconvert)
    elif currency1 not in fiat and currency2 in crypto:
        embedconvert = discord.Embed(title = currency1 + " is not supported or has the wrong ISO code.", description = "Here is a list of possible ISO codes: " + ", ".join(fiat))
        await ctx.send(embed = embedconvert)
    elif currency1 not in crypto and currency2 in fiat:
        embedconvert = discord.Embed(title = currency1 + " is not supported or has the wrong ISO code.", description = "Here is a list of possible ISO codes: " + ", ".join(crypto))
        await ctx.send(embed = embedconvert)
    else:
        embedconvert = discord.Embed(title = currency1 + " and " + currency2 + " are not supported or have the wrong ISO code. Here is a list of possible ISO codes:")
        embedconvert.add_field(name = "Fiat Currency", value = ", ".join(fiat), inline = False)
        embedconvert.add_field(name = "Cryptocurrency", value = ", ".join(crypto), inline= False)
        await ctx.send(embed = embedconvert)

client.run("Nzk1NzM2Mzk4NTMwNzQwMjQ0.X_NtRQ.JaUvt7jdnej03xuqRBiu1DIG8Rs")