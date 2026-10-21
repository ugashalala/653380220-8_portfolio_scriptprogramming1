# บันทึกการเปลี่ยนแปลง (CHANGELOG.md)

การเปลี่ยนแปลงที่สำคัญทั้งหมดของโครงการ Turn-Based Battle Game ถูกบันทึกไว้ในไฟล์นี้ โดยอิงตามกระบวนการพัฒนา Kanban (WIP=1)

---

## [v1.2.0] - 2026-08-06 — Skill System & Status Update

### สิ่งที่เพิ่มเข้ามา

* **Skill Dictionary System:** ใช้ Dictionary ในการจัดเก็บข้อมูล skill เช่น name, type และ value
* **Multiple Skills:** เพิ่ม Action ได้แก่ Attack, Punch of Luck, Heal และ Defend
* **Status System:** เพิ่มระบบ `player_status` สำหรับเก็บสถานะ defend

### สิ่งที่ถูกแก้ไข

* ปรับโครงสร้างโค้ดจาก if/elif จำนวนมาก → ใช้ dictionary-based design
* ทำให้สามารถเพิ่ม skill ใหม่ได้ง่ายขึ้น

---

## [v1.1.0] - 2026-08-06 — Enemy AI & Game Logic

### สิ่งที่เพิ่มเข้ามา

* **Enemy AI (Rule-based):**

  * HP ต่ำ → Heal
  * HP ปกติ → Random Attack / Heal
* **Turn System:** เพิ่มระบบผลัดกันเล่น (Player → Enemy)
* **Win/Lose Condition:** ตรวจสอบ HP เพื่อจบเกม

### สิ่งที่ถูกแก้ไข

* ปรับ flow การเล่นให้เป็นลำดับชัดเจน
* เพิ่มการตรวจสอบสถานะหลังแต่ละ turn

---

## [v1.0.0] - 2026-08-06 — Initial Release

### สิ่งที่เพิ่มเข้ามา

* เปิดตัว Turn-Based Battle Game เวอร์ชันแรก
* ระบบ HP ของ Player และ Enemy
* ระบบ Attack (random damage)
* ใช้ while loop สำหรับ game loop
* ใช้ if/elif/else สำหรับควบคุม logic

---

## [v0.4.0] - 2026-08-05 — Input Validation & Error Handling

### สิ่งที่เพิ่มเข้ามา

* **Input Validation:**

  * ตรวจสอบว่าผู้ใช้กรอกเฉพาะตัวเลือก 1–4
* ป้องกัน invalid input ด้วย loop

### สิ่งที่ถูกแก้ไข

* ลด error จาก user input
* ทำให้โปรแกรมไม่ crash

---

## [v0.3.0] - 2026-08-05 — Random System

### สิ่งที่เพิ่มเข้ามา

* ใช้ `random.randint()` สำหรับสุ่ม damage
* เพิ่มความไม่แน่นอนใน gameplay

### สิ่งที่ถูกแก้ไข

* แก้ปัญหา `NameError: random is not defined`
* เพิ่ม `import random`

---

## [v0.2.0] - 2026-08-05 — Game Structure

### สิ่งที่เพิ่มเข้ามา

* สร้าง game loop (`while`)
* เพิ่มระบบ Turn
* แสดงค่า HP ทุกรอบ

### สิ่งที่ถูกแก้ไข

* ปรับ flow การทำงานของเกมให้ต่อเนื่อง

---

## [v0.1.0] - 2026-08-05 — Project Setup

### สิ่งที่เพิ่มเข้ามา

* สร้างไฟล์ `main.py`
* เริ่มต้นโปรเจกต์ Turn-Based Battle Game
* ตั้งค่าโครงสร้างพื้นฐานของโปรแกรม
* ใช้ Kanban (WIP=1) เป็น workflow
