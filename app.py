"""
幻影哨兵 - 跨模态 Deepfake 智能体研判中心
多模态深度伪造侦测与证据链溯源平台 (SaaS Demo)
"""

import time
import random
import streamlit as st

# ─────────────────────────── 页面全局配置 ───────────────────────────
st.set_page_config(
    page_title="幻影哨兵 - 跨模态 Deepfake 智能体研判中心",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────── 自定义样式 ───────────────────────────
st.markdown("""
<style>
    /* 全局字体与背景微调 */
    .stApp { font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; }

    /* 指标卡片 */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #0f1923 0%, #1a2c3e 100%);
        border: 1px solid #2a4a6b;
        border-radius: 10px;
        padding: 16px 20px;
    }
    [data-testid="stMetric"] label { color: #8ab4f8 !important; }
    [data-testid="stMetric"] [data-testid="stMetricValue"] { color: #ff6b6b !important; font-weight: 700; }

    /* 日志终端样式 */
    .agent-log {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px 16px;
        font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
        font-size: 13px;
        line-height: 1.8;
        color: #c9d1d9;
        max-height: 420px;
        overflow-y: auto;
    }
    .agent-log .manager   { color: #79c0ff; }
    .agent-log .extractor { color: #7ee787; }
    .agent-log .reasoning { color: #d2a8ff; }
    .agent-log .reviewer  { color: #ffa657; }
    .agent-log .critic    { color: #ff7b72; }
    .agent-log .verdict   { color: #f0e68c; font-weight: bold; }
    .agent-log .timestamp { color: #484f58; }

    /* 顶部标题横幅 */
    .hero-banner {
        background: linear-gradient(135deg, #0a1628 0%, #162447 50%, #1f3a5f 100%);
        border: 1px solid #2a4a6b;
        border-radius: 12px;
        padding: 28px 36px;
        margin-bottom: 24px;
    }
    .hero-banner h1 { color: #e6edf3; margin: 0 0 8px 0; font-size: 28px; }
    .hero-banner p  { color: #8b949e; margin: 0; font-size: 14px; line-height: 1.7; }

    /* 证据链区块 */
    .evidence-block {
        background: #0d1117;
        border-left: 3px solid #f85149;
        border-radius: 4px;
        padding: 14px 18px;
        margin: 8px 0;
        font-size: 13.5px;
        line-height: 1.85;
        color: #c9d1d9;
    }
    .evidence-block strong { color: #ffa657; }
    .evidence-block .ts { color: #f85149; font-weight: 600; }

    /* 启动按钮 */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        border: none !important;
        font-size: 17px !important;
        font-weight: 600 !important;
        padding: 12px 0 !important;
        border-radius: 8px !important;
        letter-spacing: 0.5px;
    }

    /* 侧边栏系统状态 */
    .sys-stat {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .sys-stat .label { color: #8b949e; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
    .sys-stat .value { color: #58a6ff; font-size: 22px; font-weight: 700; }
    .sys-stat .bar   { background: #21262d; border-radius: 4px; height: 6px; margin-top: 6px; }
    .sys-stat .fill  { height: 6px; border-radius: 4px; }

    /* 分数圆环（简化版） */
    .score-card {
        text-align: center;
        padding: 20px 10px;
        border-radius: 12px;
        border: 1px solid #30363d;
        background: #0d1117;
    }
    .score-card .score-val {
        font-size: 48px;
        font-weight: 800;
        line-height: 1.1;
    }
    .score-card .score-label {
        font-size: 13px;
        color: #8b949e;
        margin-top: 6px;
    }
    .score-danger  { color: #f85149; }
    .score-warn    { color: #d29922; }
    .score-ok      { color: #3fb950; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────── 侧边栏 ───────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ 幻影哨兵 控制台")
    st.caption("Phantom Sentinel · Control Center")
    st.divider()

    # --- 系统状态监控 ---
    st.markdown("### 📡 系统状态")

    cpu_load = random.randint(42, 67)
    mem_load = random.randint(58, 76)
    gpu_load = random.randint(71, 89)

    st.markdown(f"""
    <div class="sys-stat">
        <div class="label">CPU 负载</div>
        <div class="value">{cpu_load}%</div>
        <div class="bar"><div class="fill" style="width:{cpu_load}%; background:{'#3fb950' if cpu_load < 60 else '#d29922'};"></div></div>
    </div>
    <div class="sys-stat">
        <div class="label">内存占用</div>
        <div class="value">{mem_load}%</div>
        <div class="bar"><div class="fill" style="width:{mem_load}%; background:{'#3fb950' if mem_load < 70 else '#d29922'};"></div></div>
    </div>
    <div class="sys-stat">
        <div class="label">GPU 利用率</div>
        <div class="value">{gpu_load}%</div>
        <div class="bar"><div class="fill" style="width:{gpu_load}%; background:{'#d29922' if gpu_load < 85 else '#f85149'};"></div></div>
    </div>
    """, unsafe_allow_html=True)

    concurrent = random.randint(12, 38)
    st.metric("当前并发任务", f"{concurrent} 个", delta=f"+{random.randint(1,5)} 较上一小时")

    st.divider()

    # --- 控制面板 ---
    st.markdown("### ⚙️ 研判参数配置")

    align_precision = st.select_slider(
        "多模态对齐精度",
        options=["标准 (1x)", "精细 (2x)", "超精细 (4x)", "像素级 (8x)"],
        value="精细 (2x)",
        help="控制音视频特征对齐的时间窗口粒度，精度越高消耗越大",
    )

    debate_rounds = st.slider(
        "Red-Blue Agent 博弈轮数",
        min_value=1, max_value=8, value=4,
        help="红队（攻击）与蓝队（防御）对抗推理的轮次，轮次越多研判越深入",
    )

    cot_depth = st.slider(
        "Chain-of-Thought 推理深度",
        min_value=2, max_value=12, value=6,
        help="控制推理链的最大展开层数",
    )

    st.selectbox(
        "视觉编码器",
        options=["ViT-L/14 (CLIP)", "ViT-H (EVA-02)", "SigLIP-SO400M"],
        index=1,
    )

    st.selectbox(
        "声学编码器",
        options=["Whisper-large-v3", "WavLM-Large", "HuBERT-XL"],
        index=0,
    )

    st.toggle("启用物理引擎约束校验", value=True)
    st.toggle("启用时序因果推理", value=True)

    st.divider()
    st.caption("v0.9.2-beta · 集群: cn-east-2a")
    st.caption("© 2026 幻影哨兵实验室")


# ─────────────────────────── 主区域 ───────────────────────────

# Hero Banner
st.markdown("""
<div class="hero-banner">
    <h1>🛡️ 幻影哨兵 — 跨模态 Deepfake 智能体研判中心</h1>
    <p>
        基于 <strong>时序逻辑长链推理</strong> 与 <strong>音画协同侦测 (V2A / A2V)</strong> 架构，
        通过多智能体红蓝博弈实现对深度伪造内容的自动化取证、溯源与可解释性研判。<br>
        支持视频、音频、音视频混合等多种输入模态，适配金融风控、司法取证、内容安全等场景。
    </p>
</div>
""", unsafe_allow_html=True)

# --- 上传区与启动按钮 ---
col_upload, col_btn = st.columns([3, 1], gap="medium")

with col_upload:
    uploaded_file = st.file_uploader(
        "📂 上传待检测媒体文件",
        type=["mp4", "wav"],
        help="支持 .mp4 视频文件或 .wav 音频文件，最大 500MB",
    )
    if uploaded_file:
        size_mb = uploaded_file.size / (1024 * 1024)
        st.success(f"已接收文件: **{uploaded_file.name}** ({size_mb:.1f} MB)")

with col_btn:
    st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
    run_button = st.button(
        "🚀 启动多智能体深度研判",
        type="primary",
        use_container_width=True,
        disabled=(uploaded_file is None),
    )

# 如果没有上传文件，给个提示
if not uploaded_file:
    st.info("👆 请先上传 .mp4 或 .wav 文件以启用研判流程。")


# ─────────────────────────── 模拟执行过程 ───────────────────────────
if run_button and uploaded_file:
    # 定义 Agent 工作流日志（带时间戳和颜色 class）
    agent_workflow = [
        ("00:00.0", "manager",   "[Manager]       🔍 正在解构多模态特征矩阵，初始化协同管线..."),
        ("00:00.8", "manager",   "[Manager]       📋 已生成任务 DAG：视觉分支 → 声学分支 → 对齐融合 → 博弈研判"),
        ("00:01.5", "extractor", "[Extractor]     🎬 启动视觉流解码，目标帧率: 30fps，关键帧间隔: 120ms"),
        ("00:02.3", "extractor", "[Extractor]     📊 已提取 35,200 维视觉特征向量 (ViT-H/patch14)"),
        ("00:03.1", "extractor", "[Extractor]     🔊 声学流处理中：STFT 窗口 25ms / 帧移 10ms，频带 80-8000Hz"),
        ("00:03.8", "extractor", "[Extractor]     📊 已提取 12,800 维声学频响特征 (WavLM-Large)"),
        ("00:04.2", "reasoning", "[Reasoning]     🧠 启动 Chain-of-Thought 时序对齐推理 (深度: 6 层)..."),
        ("00:04.8", "reasoning", "[Reasoning]     🔗 Phase-1: 视觉-声学时间戳交叉对齐 → 发现 17 处候选异常窗口"),
        ("00:05.4", "reasoning", "[Reasoning]     🔗 Phase-2: 物理约束校验 → 指法运动轨迹 vs 音高变化曲线"),
        ("00:05.9", "reviewer",  "[Reviewer]      ⚔️ 触发红蓝博弈 Round 1/4：Red Agent 标记 00:12.3s 指法断层"),
        ("00:06.3", "critic",    "[Critic]        🔴 Red: 00:12.3s 处左手按弦位置与实际音高偏移 +3.2 半音，违反物理约束"),
        ("00:06.7", "reviewer",  "[Reviewer]      🔵 Blue Agent 尝试反驳：可能是镜头畸变导致的视觉偏差..."),
        ("00:07.0", "critic",    "[Critic]        🔴 Red 反击：同镜头其他时段无畸变，且声谱分析确认该音高异常"),
        ("00:07.3", "reviewer",  "[Reviewer]      ⚔️ Round 2/4：Red Agent 发现 00:23.7s 嘴型与语音节奏不匹配"),
        ("00:07.6", "critic",    "[Critic]        🔴 Red: 唇动频率与语音基频 F0 存在 180ms 相位延迟"),
        ("00:07.9", "reviewer",  "[Reviewer]      ⚔️ Round 3/4：光照一致性校验 → 面部阴影方向与环境光源矛盾"),
        ("00:08.2", "reviewer",  "[Reviewer]      ⚔️ Round 4/4：最终博弈 → Red Agent 累计提交 4 项不可解释伪造证据"),
        ("00:08.5", "verdict",   "[Judge]         ⚖️ 综合研判完成 — Deepfake 置信度: 97.3% | 伪造类型: 音视频协同替换"),
    ]

    # 使用 st.status 展示处理过程
    with st.status("🧠 多智能体研判引擎运行中...", expanded=True) as status:
        log_placeholder = st.empty()
        accumulated_log = ""

        for ts, cls, msg in agent_workflow:
            time.sleep(random.uniform(0.35, 0.65))
            accumulated_log += f'<span class="timestamp">[{ts}]</span> <span class="{cls}">{msg}</span>\n'
            log_placeholder.markdown(
                f'<div class="agent-log">{accumulated_log}</div>',
                unsafe_allow_html=True,
            )

        status.update(label="✅ 研判完成 — 发现严重伪造特征", state="complete", expanded=False)

    st.markdown("---")

    # ─────────────────────────── 结果展示区 ───────────────────────────
    st.markdown("## 📋 综合研判报告")

    # --- 三大核心指标 ---
    score_col1, score_col2, score_col3 = st.columns(3, gap="large")

    with score_col1:
        st.markdown("""
        <div class="score-card">
            <div class="score-val score-danger">12%</div>
            <div class="score-label">综合真实度评分</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("⚠️ 评分 < 30% 自动触发高危预警")

    with score_col2:
        st.markdown("""
        <div class="score-card">
            <div class="score-val score-warn">23%</div>
            <div class="score-label">视觉连续性得分</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("基于逐帧像素一致性与光流分析")

    with score_col3:
        st.markdown("""
        <div class="score-card">
            <div class="score-val score-danger">8%</div>
            <div class="score-label">音画物理逻辑对齐度</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("声学特征 vs 视觉运动的因果匹配")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- 证据链报告 ---
    with st.expander("🔍 证据链溯源报告 (Evidence Chain Report) — 点击展开完整分析", expanded=True):
        st.markdown("### 🔗 多模态时序对齐证据链")

        st.markdown("""
        <div class="evidence-block">
            <strong>📍 证据 #1 — 时间戳 <span class="ts">00:12.3s</span> — 指法-音高物理矛盾</strong><br>
            在该时刻，演奏者左手按压吉他第5品位置（视觉特征：指尖距琴桥约 38.2cm），
            按照标准调弦 (E-A-D-G-B-E) 理论应产生频率约 <strong>329.6 Hz (E4)</strong> 的音高。
            然而声学特征提取显示该时刻实际音频基频为 <strong>293.7 Hz (D4)</strong>，
            偏差达 <strong>3.2 个半音</strong>，超出任何正常演奏偏差范围 (±0.5 半音)。<br>
            <em>物理引擎校验结论：该指法动作不可能产生此音高 → 伪造。</em>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="evidence-block">
            <strong>📍 证据 #2 — 时间戳 <span class="ts">00:23.7s</span> — 唇动-语音相位延迟</strong><br>
            面部关键点追踪显示，说话者嘴唇开合频率为 <strong>3.8 Hz</strong>（对应语速约 228 音节/分钟），
            但语音流的音节检测显示实际语速为 <strong>4.6 Hz</strong>（276 音节/分钟）。
            唇动信号与语音信号之间存在 <strong>180ms 相位延迟</strong>，
            且延迟量在后续 2.3 秒内呈非线性漂移。<br>
            <em>唇音同步分析结论：音频来源与面部动作非同一时刻录制 → 音频替换。</em>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="evidence-block">
            <strong>📍 证据 #3 — 时间戳 <span class="ts">00:31.1s ~ 00:33.8s</span> — 光照环境矛盾</strong><br>
            面部法线贴图重建显示主光源方向为 <strong>方位角 47° / 仰角 62°</strong>（右上方），
            但同帧背景物体阴影分析显示环境主光源为 <strong>方位角 180° / 仰角 35°</strong>（正下方）。
            两个光源方向的夹角达 <strong>127°</strong>，远超自然光照一致性阈值 (±15°)。<br>
            <em>光照一致性校验结论：面部区域与背景处于不同光照环境 → 面部替换。</em>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="evidence-block">
            <strong>📍 证据 #4 — 时间戳 <span class="ts">00:45.6s</span> — 微表情时间连贯性断裂</strong><br>
            面部 Action Unit (AU) 序列分析检测到 AU12（嘴角上扬）在连续两帧间出现
            <strong>强度跳变 0.73</strong>（正常范围 < 0.15），且该跳变恰好发生在视频 GOP 边界。
            同时，眨眼频率在该段落突然从 15 次/分钟 降至 3 次/分钟，随后在 0.5s 内恢复。<br>
            <em>时序连续性分析结论：面部生成模型在关键帧边界出现渲染不一致 → 生成式伪造。</em>
        </div>
        """, unsafe_allow_html=True)

        # 完整报告片段
        st.markdown("### 📝 深度分析摘要")
        st.markdown("""
        本次研判基于 **4 轮红蓝对抗博弈**、**6 层 Chain-of-Thought 推理**，
        共处理 **124,500 个 Context Tokens**。系统对输入媒体进行了全时序、逐帧的多模态交叉验证：

        1. **视觉分支**：提取 35,200 维特征向量，覆盖面部关键点 (468 点)、手部姿态 (21 关节 × 2)、
           光流场、纹理频谱等维度。检测到 3 处时序不连续异常。

        2. **声学分支**：提取 12,800 维频响特征，覆盖 F0 基频轨迹、共振峰 (F1-F4)、
           频谱包络、谐噪比等维度。检测到 2 处声学-语义不一致。

        3. **跨模态对齐**：通过 4x 精度的时序对齐窗口 (±33ms)，
           在视觉特征与声学特征之间发现 **4 处统计显著的物理矛盾**（p < 0.001）。

        4. **博弈研判**：Red Agent 累计提交 7 项伪造证据，Blue Agent 仅成功反驳 3 项，
           最终判定为 **高度伪造内容** (Deepfake Confidence: 97.3%)。

        **伪造类型判定**：音视频协同替换 (Audio-Video Collaborative Replacement)，
        属于高级别的多模态合成攻击，疑似使用最新一代扩散模型 + 神经声码器联合生成。

        **溯源线索**：生成伪影模式与已知的 "EchoForge v3" 模型特征匹配度达 89.2%，
        建议进入深度溯源流程。
        """)

    st.markdown("---")

    # --- Token 消耗统计 ---
    st.markdown("### 📊 本次任务资源消耗")

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric(
            label="单次研判 Context 吞吐",
            value="124,500 Tokens",
            delta="+18.3% 较上次",
            delta_color="inverse",
        )

    with metric_col2:
        st.metric(
            label="累计辩论轮次",
            value="4 轮",
            delta="Red 4 : Blue 0 胜",
        )

    with metric_col3:
        st.metric(
            label="推理耗时",
            value="8.7 秒",
            delta="-1.2s 较基线",
        )

    with metric_col4:
        st.metric(
            label="证据链置信度",
            value="97.3%",
            delta="高置信",
        )

    # 底部声明
    st.markdown("---")
    st.caption(
        "📌 以上结果由幻影哨兵多智能体研判系统生成 · "
        "本演示为 Mock 数据展示，实际生产环境对接真实模型推理引擎 · "
        "报告 ID: RPT-20260511-{:06d}".format(random.randint(100000, 999999))
    )
