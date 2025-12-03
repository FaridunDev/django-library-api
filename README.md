# 📚 Django Library API (Kitoblar va Reytinglarni Boshqarish)

Ushbu loyiha **Django REST Framework (DRF)** asosida yaratilgan bo‘lib, kutubxona tizimi uchun to‘liq funksional RESTful API hisoblanadi. Loyiha kitoblar, mualliflar, janrlar, nashriyotlar va foydalanuvchilar tomonidan qoldirilgan reytinglarni boshqarishga mo‘ljallangan.

Loyihaning muhiti **Docker** yordamida izolyatsiya qilingan va ishlab chiqarishga mos keluvchi **PostgreSQL** ma'lumotlar bazasidan foydalanadi.

---

## ✨ Asosiy Xususiyatlar

* **To'liq CRUD operatsiyalari:** `Author`, `Book`, `Genre`, `Publisher`, `Review`.  
* **RESTful API:** Django REST Framework yordamida barcha endpointlar standartlashtirilgan.  
* **PostgreSQL Baza:** Katta hajmli ma’lumotlar uchun optimallashtirilgan.  
* **Test Qamrovi:** 17 ta test orqali barcha modellar va API endpointlari sinovdan o‘tgan.  
* **Docker Tayyorligi:** Docker va Docker Compose orqali tezkor ishga tushirish.  
* **Xavfsizlik:** Barcha yozish/o'chirish/o'zgartirish endpointlari autentifikatsiya bilan himoyalangan.  
* **Tezlik:** Django QuerySet’lari tufayli tezkor so‘rovlar va javob vaqti.  

---

## 🛠️ Ishga Tushirish Qo‘llanmasi (Docker)

Loyihani ishga tushirish uchun quyidagilar o‘rnatilgan bo‘lishi kerak:  

* **Docker**  
* **Docker Compose V2**  

### 1️⃣ Repozitoriyani klonlash
```bash
git clone https://github.com/FaridunDev/django-library-api.git
cd django-library-api
