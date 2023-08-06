import discord
import random
import sys

from Calculator import Calculator
from SendImage import ImageSender
from Meme import Memes
from DocumentSender import DocumentSender
from DatabaseConnector import DatabaseConnector

class MyClient(discord.Client):

    # Einloggen auf den Server
    async def on_ready(self):
        # Rückmeldung in der Konsole, ob der Bot erfolgreich hinzugefügt wurde
        print("Loged in successfully! Beep boop.")

    # Erhalte Inhalt für die Hilfe aus einer txt-Datei
    def get_help_text(self, name):
        # Öffnet die Datei zum Lesen des Inhalts
        with open (name, "r") as myfile:
            # Liest den Inhalt der Datei
            data=myfile.read()
            # Gibt den gelesenen Inhalt zurück
            return data

    # Wenn eine Nachricht im Channel gepostet wird
    async def on_message(self, message):
        
        DatabaseConnector.insert_user_into_database(message.author)

        DatabaseConnector.insert_message_into_database(message.content, message.author, message.channel)

        message.content = message.content.lower()

        # Prüft ob die Nachricht vom Bot ist
        if message.author == self.user:
            # Return als Abbruch
            return
        # Prüft ob die Nachricht einen bestimmten Inhalt hat
        if message.content.startswith("hello bot"):
            # Wartet bis die Nachricht gesendet wurde
            await message.channel.send("Hello " + str(message.author))

        if (message.content.startswith("!r")):
            await self.execute_commands(message)

        # Rückmeldung in der Konsole, ob jemand eine Nachricht geschrieben hat
        print("Message from " + str(message.author) + ": " + str(message.content))

    # Gibt Hilfe zurück
    async def send_help(self, message):    
        # Rückmeldung in der Konsole, ob jemand Hilfe benötigt
        print("help requested from " + str(message.author))
        # Sendet die Hilfe Nachricht
        embed=discord.Embed(title = "Help", description = self.get_help_text("./help/help.txt"), color=0x0433ff)
        embed.set_author(name="Discord_Bot_IHK")
        embed.set_thumbnail(url="https://img.icons8.com/color/48/000000/help--v1.png")
        await message.channel.send(embed=embed)

    # Gibt Hilfe für Kommandos zurück
    async def send_help_commands(self, message):    
        # Rückmeldung in der Konsole, ob jemand Hilfe benötigt
        print("help requested from " + str(message.author))
        # Sendet die Hilfe Nachricht
        embed=discord.Embed(title = "Commands Help", description = self.get_help_text("./help/help_commands.txt"), color=0x0433ff)
        embed.set_author(name="Discord_Bot_IHK")
        embed.set_thumbnail(url="https://img.icons8.com/color/48/000000/help--v1.png")
        await message.channel.send(embed=embed)

        # Gibt Hilfe für Kommandos zurück
    async def send_help_stats(self, message):    
        # Rückmeldung in der Konsole, ob jemand Hilfe benötigt
        print("help requested from " + str(message.author))
        # Sendet die Hilfe Nachricht
        embed=discord.Embed(title = "Stats Help", description = self.get_help_text("./help/help_stats.txt"), color=0x0433ff)
        embed.set_author(name="Discord_Bot_IHK")
        embed.set_thumbnail(url="https://img.icons8.com/color/48/000000/help--v1.png")
        await message.channel.send(embed=embed)
                
    async def delete_messages(self, message, amount):
        amount += 1
        messages = await message.channel.history(limit=amount).flatten()

        try:
            for i in messages:
                await i.delete()
                print(str(i.content) + " deleted")
        except:
            print("error occured while deleting messages")

    async def delete_all_messages(self, message):
        messages = await message.channel.history().flatten()

        try:
            for i in messages:
                await i.delete()
                print(str(i.content) + " deleted")
        except:
            print("error occured while deleting messages")

    async def get_history(self, message, amount):
        messages = await message.channel.history(limit=amount).flatten()
        # Öffnet die Datei zum Lesen des Inhalts
        with open ("history.txt", "a") as myfile:
            myfile.truncate(0)

            for i in messages:
                # Schreibt den Inhalt der Datei
                myfile.writelines(str(i.author) + " " + str(i.content))
                myfile.writelines("\n")
                myfile.writelines("----")
                myfile.write("\n")
                
                print(i)
        
        await DocumentSender.sendFile(message.channel, "history.txt")
    
    async def get_history_all(self, message):
        messages = await message.channel.history().flatten()
        with open ("history.txt", "a") as myfile:
            myfile.truncate(0)

            for i in messages:
                # Schreibt den Inhalt der Datei
                myfile.writelines(str(i.author) + " " + str(i.content))
                myfile.writelines("\n")
                myfile.writelines("----")
                myfile.write("\n")
                
                print(i)

        await DocumentSender.sendFile(message.channel, "history.txt")


    async def get_history_all_database(self, message):

        with open ("history.txt", "a") as file:
            file.truncate(0)

            file.write(DatabaseConnector.get_history())

        await DocumentSender.sendFile(message.channel, "history.txt")

    async def send_message(self, channel, message):
        embed=discord.Embed(description = message, color=0x0433ff)
        embed.set_author(name="Discord_Bot_IHK")
        #embed.set_thumbnail(url="https://img.icons8.com/color/48/000000/apple-calculator.png")
        await channel.send(embed=embed)

    async def execute_commands(self, message):
        if message.content.startswith("!r"):
            print("User " + str(message.author) + " requested a command!")

            if message.content.startswith("!r random"):
                number1 = message.content.split(' ')[2]
                number2 = message.content.split(' ')[3]
                randomInt = Calculator.get_random(number1, number2)

                await self.send_message(message.channel, "Deine Zufallszahl ist: " + str(randomInt))

            if message.content.startswith("!r help"):
                if message.content.startswith("!r help cmd"):
                    await self.send_help_commands(message)
                elif message.content.startswith("!r help stats"):
                    await self.send_help_stats(message)
                else:
                    await self.send_help(message)

            if message.content.startswith("!r calc"):
                if message.content.startswith("!r calc a"):

                    res = Calculator.calc_advanced(message.content)

                    await self.send_message(message.channel, "Das Ergebnis ist: " + str(res) + "\n(" + message.content + ")")
                else:
                    res = Calculator.calc_easy(message.content)

                    await self.send_message(message.channel, "Das Ergebnis ist: " + str(res) + "\n(" + message.content + ")")

            if message.content.startswith("!r image"):

                url = message.content.split(' ')[2]

                await ImageSender.sendFromURL(message.channel, url)

            if message.content.startswith("!r meme r"):

                await ImageSender.sendFromURL(message.channel, Memes.get_random_meme())

            if message.content.startswith("!r history"):

                amount = message.content.split(' ')[2]

                if amount == 'all':

                    await self.get_history_all(message)

                if amount == "db":

                    await self.get_history_all_database(message)

                else:

                    amount = int(amount)

                await self.get_history(message, amount)

            if message.content.startswith("!r delete"):

                amount = message.content.split(' ')[2]

                if amount == 'all':

                    await self.delete_all_messages(message)

                else:

                    amount = int(amount)

                await self.delete_messages(message, amount)

            if message.content.startswith("!r stats m"):
                if message.content.startswith("!r stats m -u"):
                    res = DatabaseConnector.get_stats_messages_user()

                    await self.send_message(message.channel, "Nachrichten nur von Nutzern: " + str(res))
                elif message.content.startswith("!r stats m -all"):
                    res = DatabaseConnector.get_stats_messages_all()

                    await self.send_message(message.channel, "Nachrichten von allen: " + str(res))
                elif message.content.startswith("!r stats m -d"):
                    date = message.content.split(' ')[4]
                    res = DatabaseConnector.get_stats_messages_date(date)

                    await self.send_message(message.channel, "Nachrichten vom " + str(date)+ " : " + str(res))

            if message.content.startswith("!r logout"):
                await self.send_message(message.channel, "Ich bin dann mal raus! Beep booooop...😴")

                await sys.exit()

MyClient().run(input("Insert your discord key: "))