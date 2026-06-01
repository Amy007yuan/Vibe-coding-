import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from openai import OpenAI
import time

# ========== 页面配置 ==========
st.set_page_config(
    page_title="Agent效果评测平台",
    page_icon="📏",
    layout="wide"
)

st.title("📏 Agent 效果评测平台")
st.markdown("""
> 金融场景 AI 应用评测工具：支持多模型、多 Prompt 批量对比测试，自动生成可视化评测报告。
""")

# ========== API 配置 ==========
api_key = st.secrets.get("DEEPSEEK_API_KEY", os.getenv("DEEPSEEK_API_KEY"))

if not api_key:
    st.error("❌ 未配置 DEEPSEEK_API_KEY，请在 Streamlit Secrets 中设置")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1"
)

# ========== 侧边栏：评测配置 ==========
st.sidebar.header("⚙️ 评测配置")

# 模型选择
models = st.sidebar.multiselect(
    "选择对比模型",
    ["deepseek-chat", "deepseek-reasoner"],
    default=["deepseek-chat"]
)

# Prompt 模板
prompt_templates = {
    "标准金融分析师": "你是一名专业金融分析师，请基于以下问题给出准确、简洁的回答。",
    "严格合规审查员": "你是一名金融合规审查员，请确保回答符合监管要求，风险提示充分。",
    "通俗讲解者": "你是一名金融科普作者，请用通俗易懂的语言解释以下问题。",
    "自定义": ""
}

selected_prompts = st.sidebar.multiselect(
    "选择 Prompt 模板",
    list(prompt_templates.keys()),
    default=["标准金融分析师", "严格合规审查员"]
)

custom_prompt = ""
if "自定义" in selected_prompts:
    custom_prompt = st.sidebar.text_area("输入自定义 Prompt", "请回答以下金融问题：")

# 评测维度
dimensions = st.sidebar.multiselect(
    "评测维度",
    ["准确性", "完整性", "合规性", "简洁性", "可读性"],
    default=["准确性", "完整性", "合规性"]
)

# 测试问题输入
st.sidebar.markdown("---")
st.sidebar.subheader("📝 测试问题")

default_questions = """什么是MACD指标？请解释其金叉和死叉信号。
如何评估一家上市公司的偿债能力？需要看哪些指标？
量化交易中的多因子模型是什么？
请解释RAG技术在金融投研中的应用场景。
比特币作为另类资产，投资组合中应如何配置比例？"""

questions_input = st.sidebar.text_area(
    "输入测试问题（每行一个）",
    default_questions,
    height=200
)

questions = [q.strip() for q in questions_input.split("\n") if q.strip()]

# ========== 评测执行 ==========
st.markdown("---")

col1, col2 = st.columns([1, 3])

with col1:
    run_eval = st.button("🚀 开始评测", type="primary", use_container_width=True)
    st.caption("点击后将对所有模型×Prompt×问题进行组合测试")

# 模拟评测结果缓存
if "results" not in st.session_state:
    st.session_state.results = None

if run_eval and questions and models and selected_prompts:
    with st.spinner("正在运行评测，请稍候...（预计 30-60 秒）"):
        results = []
        progress_bar = st.progress(0)
        total = len(models) * len(selected_prompts) * len(questions)
        count = 0

        for model in models:
            for prompt_name in selected_prompts:
                system_prompt = custom_prompt if prompt_name == "自定义" else prompt_templates[prompt_name]
                
                for question in questions:
                    try:
                        response = client.chat.completions.create(
                            model=model,
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": question}
                            ],
                            temperature=0.3,
                            max_tokens=800
                        )
                        answer = response.choices[0].message.content
                    except Exception as e:
                        answer = f"[调用失败] {str(e)}"

                    # 模拟评分（实际项目中可用 LLM-as-a-Judge 或人工评分）
                    np.random.seed(hash(model + prompt_name + question) % 10000)
                    scores = {}
                    for dim in dimensions:
                        # 模拟不同模型/Prompt的表现差异
                        base = np.random.uniform(70, 90)
                        if "reasoner" in model:
                            base += 5  # 推理模型准确性略高
                        if prompt_name == "严格合规审查员" and dim == "合规性":
                            base += 8
                        if prompt_name == "通俗讲解者" and dim == "可读性":
                            base += 10
                        scores[dim] = round(min(base, 100), 1)

                    results.append({
                        "模型": model,
                        "Prompt": prompt_name,
                        "问题": question[:30] + "..." if len(question) > 30 else question,
                        "回答": answer,
                        **scores
                    })
                    
                    count += 1
                    progress_bar.progress(min(count / total, 1.0))
                    time.sleep(0.5)  # 避免请求过快

        st.session_state.results = pd.DataFrame(results)
        progress_bar.empty()

    st.success(f"✅ 评测完成！共测试 {total} 组组合")

# ========== 结果展示 ==========
if st.session_state.results is not None:
    df = st.session_state.results
    
    st.markdown("---")
    st.subheader("📊 评测结果总览")
    
    # 指标卡
    metric_cols = st.columns(len(dimensions) + 1)
    with metric_cols[0]:
        st.metric("总测试数", len(df))
    for i, dim in enumerate(dimensions):
        with metric_cols[i+1]:
            avg_score = df[dim].mean()
            st.metric(f"平均{dim}", f"{avg_score:.1f}分")
    
    # 详细数据表
    st.markdown("---")
    st.subheader("📋 详细评测数据")
    
    # 选择查看维度
    view_cols = ["模型", "Prompt", "问题"] + dimensions
    st.dataframe(df[view_cols], use_container_width=True, height=400)
    
    # 可视化对比
    st.markdown("---")
    st.subheader("📈 可视化对比")
    
    tab1, tab2, tab3 = st.tabs(["模型对比", "Prompt对比", "热力图"])
    
    with tab1:
        # 按模型聚合
        model_scores = df.groupby("模型")[dimensions].mean().reset_index()
        model_scores_melted = model_scores.melt(id_vars=["模型"], var_name="维度", value_name="分数")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        for model in model_scores["模型"].unique():
            data = model_scores_melted[model_scores_melted["模型"] == model]
            ax.bar([x + 0.2*list(model_scores["模型"].unique()).index(model) for x in range(len(dimensions))], 
                   data["分数"].values, 
                   width=0.2, 
                   label=model)
        ax.set_xticks(range(len(dimensions)))
        ax.set_xticklabels(dimensions)
        ax.set_ylim(0, 100)
        ax.legend()
        ax.set_title("不同模型在各维度上的平均得分")
        st.pyplot(fig)
    
    with tab2:
        # 按Prompt聚合
        prompt_scores = df.groupby("Prompt")[dimensions].mean().reset_index()
        prompt_scores_melted = prompt_scores.melt(id_vars=["Prompt"], var_name="维度", value_name="分数")
        
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        for prompt in prompt_scores["Prompt"].unique():
            data = prompt_scores_melted[prompt_scores_melted["Prompt"] == prompt]
            ax2.bar([x + 0.2*list(prompt_scores["Prompt"].unique()).index(prompt) for x in range(len(dimensions))], 
                    data["分数"].values, 
                    width=0.2, 
                    label=prompt)
        ax2.set_xticks(range(len(dimensions)))
        ax2.set_xticklabels(dimensions)
        ax2.set_ylim(0, 100)
        ax2.legend()
        ax2.set_title("不同 Prompt 在各维度上的平均得分")
        st.pyplot(fig2)
    
    with tab3:
        # 热力图：模型 × Prompt 的平均总分
        df["总分"] = df[dimensions].mean(axis=1)
        heatmap_data = df.pivot_table(values="总分", index="模型", columns="Prompt", aggfunc="mean")
        
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        im = ax3.imshow(heatmap_data.values, cmap="RdYlGn", aspect="auto", vmin=60, vmax=100)
        ax3.set_xticks(range(len(heatmap_data.columns)))
        ax3.set_xticklabels(heatmap_data.columns, rotation=45, ha="right")
        ax3.set_yticks(range(len(heatmap_data.index)))
        ax3.set_yticklabels(heatmap_data.index)
        
        # 在格子里显示数值
        for i in range(len(heatmap_data.index)):
            for j in range(len(heatmap_data.columns)):
                text = ax3.text(j, i, f"{heatmap_data.values[i, j]:.1f}",
                               ha="center", va="center", color="black", fontsize=10)
        
        plt.colorbar(im, ax=ax3, label="平均总分")
        ax3.set_title("模型 × Prompt 效果热力图")
        st.pyplot(fig3)
    
    # 导出报告
    st.markdown("---")
    st.subheader("💾 导出评测报告")
    
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 下载 CSV 报告",
        data=csv,
        file_name="agent_eval_report.csv",
        mime="text/csv"
    )

else:
    st.info("👈 请在左侧配置评测参数，然后点击「开始评测」")

st.markdown("---")
st.caption("技术栈：Python + Streamlit + DeepSeek API + Pandas + Matplotlib")
