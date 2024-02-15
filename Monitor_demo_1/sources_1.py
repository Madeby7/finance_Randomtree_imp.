import numpy as np 
import pandas as pd
import random

list1 = ["mahmut", "Tuncer", "Huseyin", "ahmet"]

liste_2 = ["Elma", "Armut", "Muz", "Portakal", "Mandalina", "Limon", "Kiraz", "Erik", "Şeftali", "Kayısı",
         "Kavun", "Karpuz", "Domates", "Salatalık", "Biber", "Patlıcan", "Kabak", "Patates", "Soğan", "Sarımsak",
         "Ispanak", "Marul", "Maydanoz", "Dereotu", "Nane", "Biberiye", "Kekik", "Adaçayı", "Rezene", "Defne yaprağı",
         "Zencefil", "Zerdeçal", "Tarçın", "Kakule", "Vanilya", "Karanfil", "Muskat", "Kimyon", "Kişniş", "Sumak",
         "Pul biber", "Karabiber", "Acı biber", "Kekik", "Biberiye", "Nane", "Maydanoz", "Dereotu", "Soğan", "Sarımsak",
         "Patates", "Kabak", "Patlıcan", "Biber", "Salatalık", "Domates", "Karpuz", "Kavun", "Kayısı", "Şeftali", "Erik",
         "Kiraz", "Limon", "Mandalina", "Portakal", "Muz", "Armut", "Elma", "Ananas", "Mango", "Kivi", "Çilek", " ahududu",
         "Yaban mersini", "Böğürtlen", "Karadut", " üzüm", "Kavun", "Karpuz", "Domates", "Salatalık", "Biber",
         "Patlıcan", "Kabak", "Patates", "Soğan", "Sarımsak", "Maydanoz", "Dereotu", "Nane", "Biberiye", "Kekik",
         "Zencefil", "Zerdeçal", "Tarçın", "Kakule", "Vanilya", "Karanfil", "Muskat", "Kimyon", "Kişniş", "Sumak",
         "Pul biber", "Karabiber", "Acı biber", "Kekik", "Biberiye", "Nane", "Maydanoz", "Dereotu", "Soğan", "Sarımsak",
         "Patates", "Kabak", "Patlıcan", "Biber", "Salatalık", "Domates", "Karpuz", "Kavun", "Kayısı", "Şeftali", "Erik",
         "Kiraz", "Limon", "Mandalina", "Portakal", "Muz", "Armut", "Elma"]



ogrenciler = []

for i in range(100):
    isim = random.choice(["Ahmet", "Ayşe", "Mehmet", "Fatma", "Ali", "Elif", "Can", "Su", "Deniz", "Efe"])
    soyisim = random.choice(["Yılmaz", "Demir", "Can", "Kaya", "Aydın", "Öztürk", "Çetin", "Karataş", "Yıldırım", "Doğan"])
    id = random.randint(1000, 9999)

    ogrenci = {"ID": id, "name": f"{isim} {soyisim}"}
    ogrenciler.append(ogrenci)

print(ogrenciler)

liste_3 = ogrenciler