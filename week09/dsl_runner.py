import re

def dsl_to_python(dsl_code: str) -> str:
    lines = dsl_code.strip().split('\n')
    python_lines = []

    for line in lines:
        line = line.strip()

        # [xを5にする] または [xをx+1にする]
        m = re.match(r"(.+?) を (.+?) にする", line)
        if m:
            var, val = m.groups()
            python_lines.append(f"{var.strip()} = {val.strip()}")
            continue

        # xを表示する
        m = re.match(r"(.+?) を表示する", line)
        if m:
            var = m.group(1).strip()
            python_lines.append(f"print({var})")
            continue

        # 「こんにちは」を表示する
        m = re.match(r"「(.+?)」と表示する", line)
        if m:
            msg = m.group(1)
            python_lines.append(f'print("{msg}")')
            continue

        # xが5より大きいなら「大きい」と表示する
        m = re.match(r"(.+?) が (.+?) より大きいなら「(.+?)」と表示する", line)
        if m:
            var, val, msg = m.groups()
            python_lines.append(f"if {var.strip()} > {val.strip()}: print(\"{msg}\")")
            continue

        # xが5以下なら「小さい」と表示する
        m = re.match(r"(.+?) が (.+?) 以下なら「(.+?)」と表示する", line)
        if m:
            var, val, msg = m.groups()
            python_lines.append()

        # 「3回くりかえす：「こんにちは」と表示する」
        m = re.match(r"(\d+) 回くりかえす：(.+?)", line)
        if m:
            count, inner = m.groups()
            inner_py = dsl_to_python(inner)[0:]
            python_lines.append(f"for _ in range({count}): {inner_py}")
            continue

        python_lines.append("# 未対応の構文: " + line)

        # 偶数判定
        m = re.match(r"(.+?) が偶数なら「(.+?)」と表示する", line)
        if m:
            var,msg = m.groups()
            python_lines.append(f"if {var.strip()} % 2 == 0: print(\"{msg}\")")
            continue

        # 奇数判定
        m = re.match(r"(.+?) が奇数なら「(.+?)」と表示する", line)
        if m:
            var, msg = m.groups()
            python_lines.append(f"if {var.strip()} % 2 != 0: print(\"{msg}\")")
            continue

        # if-else構文
        m = re.match(r"もし (.+?) が (.+?) より大きいなら「(.+?)」そうでなければ「(.+?)」と表示する", line)
        if m:
            var, val, msg_true, msg_false = m.groups()
            python_lines.append(f"if {var.strip()} > {val.strip()}: print(\"{msg_true}\")")
            python_lines.append(f"else: print(\"{msg_false}\")")
            continue

    return "\n".join(python_lines)

def run_dsl(dsl_code: str) -> str:
    python_code = dsl_to_python(dsl_code)
    try:
        exec_globals = {}
        exec(python_code, exec_globals)
        return "実行成功"
    except Exception as e:
        return f"実行エラー: {e}"