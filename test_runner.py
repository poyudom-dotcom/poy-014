import sys
import os
import subprocess

# ==============================================================================
# ⚙️ ชุดทดสอบข้อสอบทั้ง 5 ข้อ (ข้อละ 4 Test Cases = ข้อละ 4 คะแนน)
# ==============================================================================
EXAM_TEST_CASES = {
    # ข้อ 1: ทักทาย Hello, <name>
    "Examination_1": [
        (["Somchai"], "Hello, Somchai"),
        (["Somsri"], "Hello, Somsri"),
        (["John"], "Hello, John"),
        (["PoY"], "Hello, PoY")
    ],
    # ข้อ 2: ราคาสินค้าเน็ต (ราคา - ส่วนลด)
    "Examination_2": [
        (["100", "20"], "80.0"),
        (["50.5", "10.5"], "40.0"),
        (["250.75", "50.25"], "200.5"),
        (["500", "0"], "500.0")
    ],
    # ข้อ 3: ตรวจสอบผลการสอบ (>=50 Pass, <50 Fail)
    "Examination_3": [
        (["85"], "Pass"),
        (["50"], "Pass"),
        (["49"], "Fail"),
        (["10"], "Fail")
    ],
    # ข้อ 4: ตัดเกรดอย่างง่าย (>=80 A, 60-79 B, <60 C)
    "Examination_4": [
        (["90"], "A"),
        (["80"], "A"),
        (["75"], "B"),
        (["55"], "C")
    ],
    # ข้อ 5: สั่งซื้อสมุด (เล่มละ 20 บาท, >=5 เล่ม ลด 10 บาท)
    "Examination_5": [
        (["1"], "20"),
        (["4"], "80"),
        (["5"], "90"),
        (["10"], "190")
    ]
}

def find_file(base_name):
    """ค้นหาไฟล์รองรับทั้งชื่อที่มีและไม่มี .py"""
    if os.path.exists(f"{base_name}.py"):
        return f"{base_name}.py"
    elif os.path.exists(base_name):
        return base_name
    return None

def run_test(file_path, inputs):
    """รันไฟล์และดึงค่า Output"""
    try:
        input_data = "\n".join(inputs)
        process = subprocess.run(
            [sys.executable, file_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=3,
            encoding='utf-8',
            errors='ignore'
        )
        return process.stdout.strip()
    except Exception:
        return None

def compare_outputs(actual, expected):
    """เปรียบเทียบผลลัพธ์ รองรับทั้งตัวเลขทศนิยมและข้อความ"""
    if actual is None:
        return False
    actual_clean = actual.strip()
    expected_clean = expected.strip()
    
    if actual_clean == expected_clean:
        return True
    
    try:
        return abs(float(actual_clean) - float(expected_clean)) < 1e-5
    except ValueError:
        return False

def main():
    total_score = 0
    max_total_score = 20
    summary_rows = []

    for exam_name, test_cases in EXAM_TEST_CASES.items():
        file_path = find_file(exam_name)
        passed_cases = 0
        total_cases = len(test_cases)
        
        if file_path:
            for inputs, expected in test_cases:
                output = run_test(file_path, inputs)
                if compare_outputs(output, expected):
                    passed_cases += 1
        
        # คะแนนยืดหยุ่นสะสมตามจำนวนเคสที่ผ่าน (ผ่าน 1 เคส = 1 คะแนน)
        score_for_exam = passed_cases 
        total_score += score_for_exam
        
        if passed_cases == total_cases:
            status_icon = "✅ ผ่านครบ"
        elif passed_cases > 0:
            status_icon = "🟡 ผ่านบางส่วน"
        else:
            status_icon = "❌ ไม่ผ่าน"

        summary_rows.append(
            f"| `{exam_name}` | {status_icon} | {passed_cases}/{total_cases} เคส | **{score_for_exam} / 4** |"
        )

    markdown_summary = f"""# 📊 สรุปผลการสอบวิชาเขียนโปรแกรม

| ข้อสอบ | สถานะการตรวจ | ผ่าน Test Cases | คะแนนที่ได้ |
| :--- | :---: | :---: | :---: |
{chr(10).join(summary_rows)}

---

### 🎯 **คะแนนรวมทั้งหมด: {total_score} / {max_total_score} คะแนน**
"""

    print(markdown_summary)

    summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_file:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(markdown_summary)

if __name__ == "__main__":
    main()
