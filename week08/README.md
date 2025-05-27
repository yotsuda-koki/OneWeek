# GraphDrawer

**GraphDrawer** は、Python + PyScript + SymPy + Matplotlib を使って、**ブラウザ上で関数のグラフ描画**や**微分・積分表示**ができる軽量Webアプリです。  
数式を入力して、ワンクリックで元の関数・微分・積分のグラフを切り替え、LaTeX で美しく数式表示します。

---

## 主な機能

- 数式を入力してリアルタイムにグラフ描画
- **元の関数／微分／積分** をボタンで切り替え
- LaTeX形式で美しい数式表示（MathJax使用）
- 完全クライアントサイド動作（PyScript）

---

## 使用例

- `sin(x)` → 三角関数の描画  
- `exp(-x**2)` → ガウス分布のような曲線  
- `x**3 + 2*x - 5` → 多項式関数  

---

## ファイル構成

| ファイル名       | 説明                      |
|------------------|---------------------------|
| `index.html`     | アプリ本体（PyScriptで完結） |

---

## 使用方法

1. このリポジトリをクローンまたはZIPでダウンロード  
2. `index.html` をダブルクリック or ブラウザで開く  
3. 数式を入力し、`元の関数 / 微分 / 積分` ボタンを押すだけ！

> サーバー不要・インストール不要・オフライン可！

---

## 使用技術

- [PyScript 2025.3.1](https://pyscript.net/)
- [SymPy](https://www.sympy.org/)
- [Matplotlib](https://matplotlib.org/)
- [MathJax](https://www.mathjax.org/)

---
