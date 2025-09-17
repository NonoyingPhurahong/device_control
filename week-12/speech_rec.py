import re, speech_recognition as sr

def c_to_f(c):
    return (c * 9/5) + 32

def f_to_c(f):
    return (f - 32) * 5/9

r = sr.Recognizer()
with sr.Microphone() as mic:
    r.adjust_for_ambient_noise(mic, duration=0.6)
    print("พูดว่า 'สวัสดี' เช่น 'แปลง 37 C เป็น F' หรือ 'แปลง 100 F เป็น C'")

    while True:
        try:
            audio = r.listen(mic, timeout=6, phrase_time_limit=10)
            text = r.recognize_google(audio, language="th-TH")
            print("ได้ยิน :", text)
            
            # ตรวจสอบคำสั่งแปลงอุณหภูมิ
            match = re.search(r"แปลง\s*(\d+)\s*([cCfF])\s*เป็น\s*([cCfF])", text)
            if match:
                value = int(match.group(1))
                from_unit = match.group(2).upper()
                to_unit = match.group(3).upper()
                
                if from_unit == "C" and to_unit == "F":
                    result = c_to_f(value)
                    print(f"{value}°C = {result:.2f}°F")
                elif from_unit == "F" and to_unit == "C":
                    result = f_to_c(value)
                    print(f"{value}°F = {result:.2f}°C")
                else:
                    print("รูปแบบคำสั่งไม่ถูกต้อง หรือยังไม่รองรับการแปลงนี้ค่ะ")
                continue  # ไปเริ่มฟังรอบใหม่

            if text.startswith("สวัสดี"):
                cmd = text.replace("สวัสดี", "", 1).strip()
                m = re.search(r"(\d+)", cmd)
                angle = int(m.group(1)) if m else None
                print("สวัสดี : ", cmd, " | มุม : ", angle)

        except sr.WaitTimeoutError:
            print("ไม่มีเสียงพูดมาได้เลยค่ะ")

        except sr.UnknownValueError:
            print("พูดมาได้เลยค่ะ...")
