# Turn-Based Battle Game - mini project

โปรแกรมเกมต่อสู้แบบผลัดเทิร์น (Turn-Based Battle) บนเทอร์มินัล พัฒนาด้วยภาษา Python ที่ผู้เล่นสามารถเลือกคำสั่งในแต่ละเทิร์น เช่น Attack, Defend และ Heal เพื่อต่อสู้กับศัตรู (Enemy) โดยระบบจะทำงานจนกว่าฝ่ายใดฝ่ายหนึ่งจะมี HP = 0

---

# Overview
## แนวคิดและการทำงาน

โปรแกรมเป็นเกมต่อสู้แบบ Turn-based ระหว่าง Player และ Enemy โดยผู้เล่นสามารถเลือก Action ในแต่ละรอบ ได้แก่:

* ⚔️ Attack — สร้าง damage แบบสุ่ม
* 🍀 Punch of Luck — damage 0–50 (สุ่มสูง-ต่ำ)
* 💊 Heal — ฟื้น HP
* 🛡️ Defend — ลด damage ในเทิร์นถัดไป

Enemy มีระบบตัดสินใจแบบง่าย (Rule-based AI):

* HP ต่ำ → Heal
* HP ปกติ → สุ่ม Attack / Heal

เกมทำงานผ่าน CLI (Command Line Interface) ไม่ใช้ library ภายนอก

## Real-World Use Cases

* Game Development — พื้นฐานระบบต่อสู้ในเกม RPG
* AI Decision System — ใช้ logic แบบ rule-based
* Simulation System — จำลองการตัดสินใจของ agent
* CLI Application — ตัวอย่างโปรแกรม interactive บน terminal
* Learning Tool — ใช้สอน Control Flow, Loop, Data Structure

## Learning Outcomes
| LO  | คำอธิบาย                                                    |
| --- | ----------------------------------------------------------- |
| LO1 | Data Structure — ใช้ Dictionary จัดการ skill และ status |
| LO2 | Collection Manipulation — จัดการข้อมูล HP และ state     |
| LO3 | Control Flow — ใช้ while loop + if/elif/else            |
| LO4 | Defensive Programming — ตรวจสอบ input                   |
| LO5 | Process Logging — บันทึก Learning Log                   |

---

# Development Workflow
## Kanban Backlog

| รอบ | การ์ด               | หมวด    | LO  | สถานะ |
| --- | ------------------- | ------- | --- | ----- |
| 1   | ตั้งค่าโปรเจกต์     | Setup   | LO5 | ✅     |
| 2   | ออกแบบ Skill System | Data    | LO1 | ✅     |
| 3   | สร้าง Game Loop     | Flow    | LO3 | ✅     |
| 4   | ทำระบบ Attack/Heal  | Logic   | LO2 | ✅     |
| 5   | Input Validation    | Safety  | LO4 | ✅     |
| 6   | Enemy AI            | Logic   | LO3 | ✅     |
| 7   | Defend System       | State   | LO1 | ✅     |
| 8   | Refactor + Log      | Process | LO5 | ✅     |

**สถานะ:** Done 8/8

---

# Group Assessments

|ผู้ประเมิน|ประเมิน อัครพงษ์|ประเมิน ภาสุ|ประเมิน ณัฐพัชร์|
|---|---|---|---|
|นายอัครพงษ์ ศรีโฉม|10|10|10|
|นายภาสุ สมมีย์|10|10|10|
|นายณัฐพัชร์ คงสวัสดิ์|10|10|10|

---

## ⚙️ How to Run
```bash
run code cell ตัวสุดท้ายเพื่อเป็นการรันเกม
แต่ในการ run ครั้งแรกควร run code cell ทั้งหมดที่มีก่อนเพื่อไม่ให้ตัวเกมเกิดการ error 
```

---

# Example Output

```text
--- Turn 1 ---
❤️ Player HP: 100 | 👾 Enemy HP: 100

Choose action:
[1] Attack ⚔️
[2] Punch of Luck 🍀
[3] Heal 💊
[4] Defend 🛡️

⚔️ You used punchofluck and deal 46 damage!
👾 Enemy attacks and deals 27 damage!
```
