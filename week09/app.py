import streamlit as st
from dsl_runner import dsl_to_python, run_dsl

st.title("日本語プログラミング DSL アプリ")

with st.sidebar:
    st.header("使い方ガイド")
    st.markdown("""
**できること（例）**

- `x を 3 にする` → `x = 3`
- `x を x + 1 にする` → `x = x + 1`
- `x を表示する` → `print(x)`
- `「こんにちは」と表示する` → `print("こんにちは")`
- `x が 5 より大きいなら「大きい」と表示する`
- `3 回くりかえす：「こんにちは」と表示する`
- `x が偶数なら「偶数です」と表示する`
- `x が奇数なら「奇数です」と表示する`
- `もし x が 5 より大きいなら「大きい」そうでなければ「小さい」と表示する`

**注意点**

- 全角の「」を使ってください（例：`「〜」と表示する`）
- 現在は1文ずつの処理です（複数行のネストや関数は非対応）
- 1つの文は1行で書いてください

                """)

dsl_input = st.text_area("日本語でプログラムを書いてみよう：", height=200)

if st.button("実行"):
    st.subheader("変換されたPythonコード")
    python_code = dsl_to_python(dsl_input)
    st.code(python_code, language="python")

    st.subheader("実行結果")
    result = run_dsl(dsl_input)
    st.write(result)