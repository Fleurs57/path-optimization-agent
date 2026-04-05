import streamlit as st
import time
import os
from main import SmartDispatchAgent  # 导入我们刚刚重构的 Agent 类

# --- 页面配置 ---
st.set_page_config(page_title="余莹的 AI 调度系统", page_icon="🚗", layout="wide")

# --- 自定义 CSS (美化界面) ---
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
    color: #4F8BF9;
}
.stAlert {
    font-weight: bold;
}
/* 优化代码块样式 */
.stCodeBlock {
    border-radius: 10px;
    background-color: #f8f9fa;
}
</style>
""", unsafe_allow_html=True)

# --- 标题 ---
st.title("🚗 AI 自动驾驶调度中心")
st.markdown("### 专业级车队管理与路径优化系统 (支持多模式分析)")

# --- 侧边栏配置 ---
with st.sidebar:
    st.image("https://via.placeholder.com/150", use_column_width=True)
    st.header("⚙️ 系统参数")
    
    # 模式选择器 (核心新增功能)
    st.subheader("🔍 分析模式")
    mode = st.radio(
        "选择 Agent 的任务",
        options=["path", "competitor", "product"],
        format_func=lambda x: {
            "path": "📊 路径优化分析",
            "competitor": "⚔️ 竞品战略分析",
            "product": "🛠️ 痛点转产品需求"
        }[x],
        key="mode_selector"
    )
    
    # API Key 输入
    # 优先从环境变量读取，防止每次重启都要输入
    default_key = os.getenv("DEEPSEEK_API_KEY", "")
    api_key = st.text_input("DeepSeek API Key", value=default_key, type="password")
    
    # 根据模式调整 Creativity
    if mode == "competitor":
        temperature = st.slider("报告发散度", 0.0, 1.0, 0.7) # 竞品分析需要更多创意
    else:
        temperature = st.slider("AI 创造力", 0.0, 1.0, 0.3) # 逻辑分析保持严谨
    
    st.success("✅ 状态：已连接 DeepSeek R1")
    
    # 显示当前选择的模式
    st.info(f"当前模式：{st.session_state.mode_selector}")

# --- 主界面 ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 输入原始数据")
    
    # 根据模式动态改变输入框的提示
    input_labels = {
        "path": "OR-Tools 原始计算结果",
        "competitor": "当前系统/竞品描述 (可选)",
        "product": "用户/司机痛点反馈"
    }
    
    placeholder_texts = {
        "path": "车辆 0: 调度中心 -> 乘客A (5km) -> 乘客B (3km)\n车辆 1: 调度中心 -> 乘客C (8km)\n总耗时: 25分钟",
        "competitor": "我们是一家初创 Robotaxi 公司，使用全局优化算法...",
        "product": "乘客觉得等待时间太长，司机觉得路线难开。"
    }
    
    input_data = st.text_area(
        input_labels[mode],
        height=300,
        value=placeholder_texts[mode],
        help="请输入相关数据，AI 将基于此进行分析"
    )

with col2:
    st.subheader("📄 AI 生成报告")
    # 使用 Markdown 容器来展示结果，支持流式输出
    result_placeholder = st.container()
    status_text = st.empty() # 用于显示状态

# --- 执行按钮与逻辑 ---
if st.button("🚀 一键生成分析报告", use_container_width=True, type="primary"):
    if not input_data.strip():
        st.warning("请先输入数据！")
    elif not api_key.startswith("sk-"):
        st.error("请输入有效的 DeepSeek API Key！")
    else:
        try:
            # 1. 初始化 Agent (传入 API Key 和 Temperature)
            # 注意：这要求 main.py 中的 SmartDispatchAgent __init__ 支持接收参数
            # 如果你的 main.py 是写死的，需要先修改 main.py 的初始化逻辑
            agent = SmartDispatchAgent(api_key=api_key, temperature=temperature)
            
            # 2. 根据侧边栏选择执行不同任务
            # 清空之前的显示
            with result_placeholder:
                st.markdown("---")
            
            # 模拟思考过程
            status_text.info("🧠 DeepSeek Agent 正在调用思维链 (CoT)...")
            time.sleep(1)
            
            # 准备输出容器
            report_container = result_placeholder.empty()
            
            # 3. 流式输出 (模拟打字机效果)
            # 因为原 main.py 可能是直接返回字符串，我们在这里模拟流式
            final_result = ""
            
            if mode == "path":
                status_text.info("📊 正在分析路径优化...")
                final_result = agent.analyze_path_optimization(input_data) # 假设方法接收 input_data 参数
                
            elif mode == "competitor":
                status_text.info("⚔️ 正在生成竞品分析...")
                final_result = agent.generate_competitor_analysis(input_data)
                
            elif mode == "product":
                status_text.info("🛠️ 正在转化产品需求...")
                final_result = agent.convert_pain_to_requirement(input_data)

            # 模拟打字机效果输出
            display_text = ""
            for char in final_result:
                display_text += char
                report_container.markdown(f"**📝 分析报告：**\n\n{display_text}")
                time.sleep(0.005) # 控制打字速度
            
            # 最终状态
            status_text.success("✅ 报告生成完成！")

        except Exception as e:
            status_text.error(f" 系统错误：{str(e)}")
            st.code(f"错误详情：{e}\n\n请检查 API Key 是否正确，或 DeepSeek 官网是否正常。", language="text")

# --- 底部 ---
st.markdown("---")
st.caption("🚀 Powered by Streamlit & DeepSeek API | 项目架构：余莹")