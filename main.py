import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- 1. 初始化组件 ---
console = Console()

# --- 2. 模拟数据 ---
# 模拟 OR-Tools 的原始输出
OR_TOOLS_RESULT = """
车辆 0: 调度中心 -> 乘客A (距离: 5km) -> 乘客B (距离: 3km) -> 返回
车辆 1: 调度中心 -> 乘客C (距离: 8km) -> 返回
总耗时: 25分钟
"""

# 模拟用户痛点（User Feedback）
USER_PAIN_POINTS = """
1. 乘客反馈：拼车等待时间太长，有时候为了接人绕路太多。
2. 运营反馈：高峰期车辆堆积，低谷期空跑严重。
3. 司机反馈：系统规划的路线红绿灯太多，不好开。
"""

# --- 3. 核心 Agent 逻辑 ---
class SmartDispatchAgent:
    def __init__(self):
        self.model = ChatOpenAI(
            base_url="https://api.deepseek.com",
            api_key=os.getenv"DEEPSEEK_API_KEY",
            model="deepseek-chat",
            temperature=0.5 # 适当提高温度以支持创意分析（如竞品分析）
        )
        self.parser = StrOutputParser()

    def _generate_report(self, prompt_template: str, input_data: str) -> str:
        """通用生成方法"""
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.model | self.parser
        return chain.invoke({"data": input_data})

    def analyze_path_optimization(self):
        """功能一：Robotaxi 路径优化方案分析"""
        console.print("🔍 [bold blue]正在深度分析 Robotaxi 路径优化方案...[/bold blue]")
        
        prompt = """
        你是一名资深的自动驾驶路径规划专家。
        请基于 OR-Tools 的计算结果，进行专业的路径复盘分析。
        
        原始数据：
        {data}
        
        请从以下维度进行分析：
        1. **效率评估**：计算平均每单的绕路比（Detour Ratio）。
        2. **冲突检测**：指出是否存在时间窗冲突风险（例如：接乘客B的时间是否太紧）。
        3. **改进建议**：建议是否需要引入“动态拼车费”来平衡乘客的等待时间。
        
        请用 Markdown 格式输出分析报告。
        """
        
        result = self._generate_report(prompt, OR_TOOLS_RESULT)
        console.print(Panel(result, title="🤖 路径优化分析报告", border_style="blue"))
        return result

    def generate_competitor_analysis(self):
        """功能二：输出竞品分析报告"""
        console.print("📊 [bold green]正在生成 Robotaxi 竞品分析报告...[/bold green]")
        
        prompt = """
        你是一名自动驾驶行业的战略分析师。
        请将我们的调度系统与主流竞品进行对比分析。
        
        我们的系统特点：基于 OR-Tools 的全局最优解，支持实时动态拼车。
        
        请分析以下竞品：
        - Waymo (Cruise)
        - 百度 Apollo (萝卜快跑)
        - Tesla (CyberCab)
        
        请输出一份竞品分析报告，包含以下部分：
        1. **调度策略对比**：我们的策略 vs 竞品策略。
        2. **优劣势分析**：我们的核心优势（如成本控制）和劣势（如算力消耗）。
        3. **市场定位**：针对 Robotaxi 2.0 时代，给出我们的突围建议。
        
        请使用 Markdown 表格进行对比。
        """
        
        result = self._generate_report(prompt, "")
        console.print(Panel(result, title="⚔️ 竞品分析报告", border_style="green"))
        return result

    def convert_pain_to_requirement(self):
        """功能三：用户痛点转换为功能需求"""
        console.print("🛠️ [bold yellow]正在将用户痛点转换为 Agent 功能需求...[/bold yellow]")
        
        prompt = """
        你是一名顶尖的 AI 产品经理 (AIPM)。
        请分析以下用户和司机的痛点，并将其转化为具体的 Agent 功能需求 (PRD)。
        
        痛点数据：
        {data}
        
        转化规则：
        1. 识别痛点类型（体验、效率、安全）。
        2. 将痛点转化为技术指标（例如：将“等待时间长”转化为“最大等待时间约束 T”）。
        3. 设计 Agent 的新功能模块。
        
        请输出一份功能需求文档，包含：
        - 功能名称
        - 触发条件
        - 算法逻辑变更
        """
        
        result = self._generate_report(prompt, USER_PAIN_POINTS)
        console.print(Panel(result, title="📝 Agent 功能需求 PRD", border_style="yellow"))
        return result

# --- 4. 运行演示 ---
if __name__ == "__main__":
    agent = SmartDispatchAgent()
    
    # 依次执行三个任务
    agent.analyze_path_optimization()
    time.sleep(2) # 模拟间隔
    
    agent.generate_competitor_analysis()
    time.sleep(2)
    
    agent.convert_pain_to_requirement()
