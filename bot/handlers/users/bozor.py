from data.config import ADMINS 
from filters.admins import IsAdmin,IsSuperAdmin
from loader import dp,db,bot
from aiogram import types
from aiogram.types import *
import requests
from requests.auth import HTTPBasicAuth
import json
import json
from aiogram import types
from loader import dp  
import re
from aiogram import types

import io
import json
import re
from PIL import Image
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




async def get_product_by_barcode(user_input):
    try:
        with open('updated_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        return "Xatolik: updated_data.json fayli topilmadi!"
    except json.JSONDecodeError:
        return "Xatolik: JSON fayl noto‘g‘ri formatda!"

    found_products = []
    
    if user_input.isdigit():  
        for product in data["inventory"]:
            barcode = product.get("barcodes", "") or ""
            inventory_code = product.get("code", "") or ""  

            last_6_digits = barcode[-6:] if len(barcode) >= 6 else barcode
            inventory_digits = "".join(re.findall(r'\d+', inventory_code))

            if user_input in barcode or user_input == last_6_digits or user_input in inventory_digits:
                found_products.append(product)

    else:
        user_input_lower = user_input.lower()
        exact_match = []
        partial_match = []

        for product in data["inventory"]:
            article_code = (product.get("article_code", "") or "").lower()
            name = (product.get("name", "") or "").lower()

            if user_input_lower == article_code or user_input_lower == name:
                exact_match.append(product)
            elif user_input_lower in article_code or user_input_lower in name:
                partial_match.append(product)

        found_products.extend(exact_match)
        found_products.extend(partial_match)

    return found_products if found_products else None

# Matn orqali mahsulotni qidirish
@dp.message_handler(IsAdmin(), content_types=types.ContentType.TEXT, state='*')
async def get_text(message: types.Message):
    user_input = message.text.strip()
    tim = await message.answer(text="⏳")

    found_products = await get_product_by_barcode(user_input)

    if isinstance(found_products, str):  # Xatolik xabari bo'lsa
        await tim.delete()
        await message.answer(found_products)
        return

    if found_products:
        await tim.delete()
        response_text = "📌 Topilgan mahsulotlar:\n\n"
        for idx, product in enumerate(found_products, start=1):
            response_text += (
                f"🔹 <b>{idx}.</b>\n"
                f"🆔 Product ID: {product.get('product_id')}\n"
                f"🔢 Code: <code>{product.get('code')}</code>\n"
                f"📛 Name: {product.get('name')}\n"
                f"✏️ Short Name: <code>{product.get('short_name')}</code>\n"
                f"🛒 Article Code: <code>{product.get('article_code') or 'Mavjud emas'}</code>\n"
                f"📌 Barcodes: <code>{product.get('barcodes') or 'Mavjud emas'}</code>\n"
                f"💰 Narxlar:\n"
                f"📑 Sahifalar Soni:1\n"
                f"🇺🇿 UZS: {product.get('price_uzs', 'Noma’lum')}\n"
                f"🇺🇸 USD: {product.get('price_usd', 'Noma’lum')}\n\n"
            )

            barcode = str(product.get('barcodes'))
            price = product.get('price_uzs', 'Noma’lum')
            if isinstance(barcode, str) and '|' in barcode:
                barcode = barcode.split("|")[0]


            if price != "Noma'lum" and price is not None and price != "None":
                await message.answer(response_text)
            
            response_text = ""
            if idx > 9:
                return

        if response_text:
            await message.answer(response_text, parse_mode="Markdown")
    else:
        await tim.delete()
        await message.answer("❌ Bunday mahsulot mavjud emas!")

import io
import json
import re
from PIL import Image
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup

@dp.message_handler(IsAdmin(), content_types=types.ContentType.PHOTO, state='*')
async def get_photo(message: types.Message):
    tim = await message.answer(text="📸 Shtrix-kod skan qilinmoqda...")

    photo = message.photo[-1]
    photo_bytes = io.BytesIO()
    await photo.download(destination_file=photo_bytes)

    photo_bytes.seek(0)
    image = Image.open(photo_bytes)

    # Rasmni PNG formatiga o'zgartirish
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)

    # ZXing API-ga rasmni yuborish
    files = {"f": ("image.png", buffered, "image/png")}
    response = requests.post("https://zxing.org/w/decode", files=files, timeout=10)

    # HTML-ni parslash
    soup = BeautifulSoup(response.text, "html.parser")
    raw_text_td = soup.find("td", string="Raw text")

    if raw_text_td:
        barcode_text = raw_text_td.find_next_sibling("td").get_text(strip=True)
        found_products = await get_product_by_barcode(barcode_text)

        if isinstance(found_products, str):
            await tim.delete()
            await message.answer(found_products)
            return

        if found_products:
            await tim.delete()
            response_text = f"📌 QR-kod: <code>{barcode_text}</code>\n\n📌 Topilgan mahsulotlar:\n\n"
            for idx, product in enumerate(found_products, start=1):
                response_text += (
                    f"🔹 <b>{idx}.</b>\n"
                    f"🆔 Product ID: {product.get('product_id')}\n"
                    f"🔢 Code: <code>{product.get('code')}</code>\n"
                    f"📛 Name: {product.get('name')}\n"
                    f"✏️ Short Name: <code>{product.get('short_name')}</code>\n"
                    f"🛒 Article Code: <code>{product.get('article_code') or 'Mavjud emas'}</code>\n"
                    f"📌 Barcodes: <code>{product.get('barcodes') or 'Mavjud emas'}</code>\n"
                    f"💰 Narxlar:\n"
                    f"📑 Sahifalar Soni:1\n"
                    f"🇺🇿 UZS: {product.get('price_uzs', 'Noma’lum')}\n"
                    f"🇺🇸 USD: {product.get('price_usd', 'Noma’lum')}\n\n"
                )

                barcode = str(product.get('barcodes'))
                price = product.get('price_uzs', 'Noma’lum')
                if isinstance(barcode, str) and '|' in barcode:
                    barcode = barcode.split("|")[0]


                if price != "Noma'lum" and price is not None and price != "None":
                    await message.answer(response_text)

                response_text = ""
                if idx > 9:
                    return

            if response_text:
                await message.answer(response_text, parse_mode="Markdown")
        else:
            await tim.delete()
            await message.answer("❌ Bunday shtrix-kodli mahsulot mavjud emas!")
    else:
        await tim.delete()
        await message.answer("❌ Rasm ichida shtrix-kod topilmadi!")
