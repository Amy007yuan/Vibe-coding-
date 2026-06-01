import streamlit as st
import PyPDF2
import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-6e5b1dbc4d4c4a7c808da68b1bb8bf74",
    base_url="https://api.deepseek.com/v1"
)

st.set_page_config(page_title="AI财报智能分析Agent", layout="wide")
st.title("📊 AI财报智能分析Agent（DeepSeek）")

# 上传PDF
uploaded_file = st.file_uploader("上传财报PDF", type="pdf")

# 提取PDF文字
def extract_pdf_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# AI分析
def analyze_report(text, question):
    prompt = f"""
    你是一名专业的金融财报分析助手，擅长从财报中提取关键信息。
    请根据以下财报内容回答用户问题，保持专业、简洁、结构化。
    
    财报内容：
    {text[:8000]}
    
    用户问题：{question}
    """
    
    response = client.chat.completions(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content

# 界面逻辑
if uploaded_file:
    with st.spinner("正在解析PDF..."):
        text = extract_pdf_text(uploaded_file)
    
    st.success("✅ 财报解析完成！")
    
    q = st.text_input("💬 向AI提问：", "分析这家公司的盈利能力、风险、成长性")
    if st.button("🚀 开始分析"):
        with st.spinner("DeepSeek AI思考中..."):
            result = analyze_report(text, q)
        st.markdown("### 📌 AI分析结果")
        st.write(result)
else:
    st.info("请上传一份财报PDF开始使用")

st.markdown("---")
st.caption("技术栈：Python + Streamlit + DeepSeek API + RAG")