from discord.ext import commands
from selenium import webdriver
import os
import time

bot = commands.Bot(command_prefix="e!")

number = 0


@bot.command(name="doc")
async def on_message(cxt):
    await cxt.send("""
    ***Commandes du bot @EcoleDsc#6148***
    `!moyenne login motdepasse`
    `!devoirs login motdepasse`
    Mettre un espace dans le login : Utiliser # à la place de l'espace
    """)


@bot.command(name="devoirs")
async def on_message(cxt, loginuser, passworduser):
    await cxt.message.delete()

    driver = webdriver.Chrome()
    driver.get("https://www.ecoledirecte.com/login")

    # Login
    login = driver.find_element_by_name("username")
    login.clear()
    login.send_keys(loginuser.replace("#", " "))
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(passworduser)
    driver.find_element_by_id("connexion").click()

    time.sleep(2)
    numberuser = driver.current_url.replace(
        "https://www.ecoledirecte.com/Eleves/", "")
    driver.get(f"https://www.ecoledirecte.com/E/{numberuser}/CahierDeTexte")
    time.sleep(2)

    # Si invalide passe
    if driver.current_url == "https://www.ecoledirecte.com/login?cameFrom=%2FAccueil":
        driver.close()
        await cxt.send("Nom d'utilisateur / Mot de passe invalide")
        pass

    home = driver.find_element_by_id("tab-devoirs-a-venir")
    await cxt.send(home.text)
    driver.close()


@bot.command(name="moyenne")
async def on_message(cxt, loginuser, passworduser):
    await cxt.message.delete()
    driver = webdriver.Chrome()
    driver.get("https://www.ecoledirecte.com/login")

    loginuser = loginuser.replace("#", " ")

    login = driver.find_element_by_name("username")
    login.clear()
    login.send_keys(loginuser)

    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(passworduser)

    driver.find_element_by_id("connexion").click()

    time.sleep(2)
    numberuser = driver.current_url.replace(
        "https://www.ecoledirecte.com/Eleves/", "")
    driver.get(f"https://www.ecoledirecte.com/E/{numberuser}/Notes")
    time.sleep(2)

    # Si invalide passe
    if driver.current_url == "https://www.ecoledirecte.com/login?cameFrom=%2FAccueil":
        driver.close()
        await cxt.send("Nom d'utilisateur / Mot de passe invalide")
        pass

    moyennegenerale = driver.find_element_by_class_name(
        "moyennegenerale-valeur")
    moyennefinale = moyennegenerale.text
    await cxt.send(f"Ta moyenne est de {moyennefinale}", mention_author=False)

    driver.close()


bot.run("TOKEN HERE")
