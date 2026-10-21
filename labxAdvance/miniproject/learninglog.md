# บันทึกการเรียนรู้ — Turn-Based Battle Game

**โปรเจกต์:** Turn-Based Battle Game (CLI)
**กระบวนการทำงาน:** Kanban, จำกัด WIP = 1, ทำทีละการ์ดต่อรอบ

บันทึกนี้รวบรวมคำสั่ง AI ที่ใช้ การตัดสินใจทางเทคนิค และปัญหาที่พบระหว่างพัฒนาเกมต่อสู้แบบ Turn-based

---

## บันทึกรอบที่ 1: เริ่มต้นโปรเจกต์

**เป้าหมายผลการเรียนรู้:** LO5 (Process Documentation)

**คำสั่ง AI:** "ช่วยออกแบบเกมแนวturn base battle game ง่ายๆให้หน่อย โดยเป็นการคุมผ่านCLI inputเป็นtextเป็นหลัก"

**การตัดสินใจ:**

* เลือกทำ **Turn-Based Battle Game** เพราะเข้าใจง่ายและใช้ Control Flow ได้ชัด
* วางโครงสร้างพื้นฐาน `main.py`

**อุปสรรค:** ยังไม่มี (เริ่มต้นโปรเจกต์)

---

## บันทึกรอบที่ 2: Game Loop และ Control Flow

**เป้าหมาย:** LO3 (Control Flow)

**การตัดสินใจ:**

* ใช้ `while` เป็น game loop
* ใช้ `if/elif/else` ควบคุม action
* แยก Player / Enemy turn

**อุปสรรค:**

* ยังจัด flow ไม่ชัด → ปรับให้เป็น Player → Enemy → Check win

---

## บันทึกรอบที่ 3: ระบบ Attack และ Random

**เป้าหมาย:** LO2 (Collection + Logic)
**คำสั่ง AI:** "ทำระบบ attack ที่ทำให้เกมดูมีความตื่นเต้นมากกว่านี้หน่อย"

**การตัดสินใจ:**

* ใช้ `random.randint()` สุ่ม damage
* HP ลดตาม damage

**อุปสรรค:**

* ❌ `NameError: random is not defined`
  → แก้โดยเพิ่ม `import random`

---

## บันทึกรอบที่ 4: Input Validation

**เป้าหมาย:** LO4 (Defensive Programming)
**คำสั่ง AI:** "ให้เลือก action เป็นตัวเลข"

**การตัดสินใจ:**

* ใช้ dictionary เก็บ skill
* ตรวจสอบ input ด้วย `if choice in skills`

**อุปสรรค:**

* user ใส่ค่าผิด → โปรแกรมพัง
  → แก้ด้วย loop + validate input

---

## บันทึกรอบที่ 5: Skill System (Dictionary)

**เป้าหมาย:** LO1 (Data Structure)
**คำสั่ง AI:** "ใช้ dictionary ในการเก็บskillจะง่ายกว่ามั้ย"

**การตัดสินใจ:**

* เปลี่ยนจาก if เยอะ ๆ → ใช้ `skills = {}`
* เก็บ type และ value ของ skill

**ผลลัพธ์:**

* โค้ดสั้นลง
* เพิ่ม skill ได้ง่าย

---

## บันทึกรอบที่ 6: Defend และ Status System

**เป้าหมาย:** LO1 + LO2
**คำสั่ง AI:** "ทำให้เกมซับซ้อนขึ้น"

**การตัดสินใจ:**

* ใช้ `player_status = {"defend": False}`
* ลด damage ถ้า defend

**อุปสรรค:**

* ลืม reset defend → bug
  → แก้โดย reset หลังใช้

---

## บันทึกรอบที่ 7: Enemy AI

**เป้าหมาย:** LO3 (Logic Design)
**คำสั่ง AI:** "เพิ่ม AI ให้ศัตรู"

**การตัดสินใจ:**

* ถ้า HP ต่ำ → heal
* ถ้าปกติ → random attack/heal

**อุปสรรค:**

* AI เดาง่าย → เพิ่ม randomness

---

## บันทึกรอบที่ 8: Refactor + Clean Code

**เป้าหมาย:** LO5 (Process + Clean Code)

**การตัดสินใจ:**

* แยกฟังก์ชัน `get_player_action()`
* จัด format output ให้อ่านง่าย
* เพิ่ม emoji เพื่อ UX

**ผลลัพธ์:**

* โค้ดอ่านง่ายขึ้น
* UX ดีขึ้น

---

## สรุปผลการเรียนรู้ (Learning Outcomes)

1. **LO1:** ใช้ Dictionary จัดการ skill และ status ได้จริง
2. **LO2:** ใช้ random, variable และ state control
3. **LO3:** เข้าใจ while loop + if/elif/else แบบใช้งานจริง
4. **LO4:** ป้องกัน error จาก user input ได้
5. **LO5:** มีการบันทึก process ครบทุกขั้นตอน

---

## Reflection (สิ่งที่ได้เรียนรู้จริง)

* การใช้ **Dictionary ทำให้โค้ด scalable มาก**
* Control Flow สำคัญมากในเกม
* การ debug (เช่น random error) คือ skill สำคัญ
* การทำ Kanban ช่วยให้ไม่หลุดโฟกัส

---

## ปัญหาที่เจอและวิธีแก้

| ปัญหา           | วิธีแก้       |
| --------------- | ------------- |
| random ไม่ทำงาน | import random |
| input ผิด       | validate      |
| defend bug      | reset status  |
| โค้ดยาว         | refactor      |

---

## แนวทางพัฒนาต่อ

* เพิ่ม critical hit
* เพิ่มหลาย enemy
* เพิ่ม level system
* ทำเป็น GUI (pygame)
