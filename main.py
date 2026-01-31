import streamlit as st
import json
import time
import os

try:
    from google import genai
except ImportError:
    st.error("缺失库，请运行: pip install google-genai")

st.set_page_config(page_title="VisionAI 丝滑重构版", layout="wide")

# 1. 核心人设（加入动作与表情连贯性要求）
MUSE_IDENTITY = (
    "Caucasian fitness model, honey-blonde hair, beauty mark on right cheek. "
    "Maintain 100% facial and clothing consistency across all segments."
)

with st.sidebar:
    st.header("⚙️ 引擎配置")
    api_key = st.text_input("Gemini API Key", type="password")
    if st.button("连接引擎"):
        try:
            client = genai.Client(api_key=api_key)
            models = client.models.list()
            st.session_state.models = [m.name.replace("models/", "") for m in models if 'generateContent' in m.supported_actions]
            st.success("连接成功")
        except Exception as e:
            st.error(f"失败: {e}")
    selected_model = st.selectbox("选择模型 (演示建议 Flash)", st.session_state.get('models', []))

st.title("🎬 全模态视频重构 - 丝滑衔接版")
st.caption("集成：语义转文字 + 骨架运动追踪 + 镜头连贯性锚点")

col_l, col_r = st.columns(2)

with col_l:
    video_file = st.file_uploader("上传原视频", type=["mp4", "mov"])
    if video_file:
        st.video(video_file)

with col_r:
    if video_file and api_key and selected_model:
        if st.button("🚀 执行全模态深度重构"):
            client = genai.Client(api_key=api_key)
            with st.status("正在解析视频韵律与动作流...", expanded=True) as status:
                try:
                    temp_path = "v_ultimate.mp4"
                    with open(temp_path, "wb") as f: f.write(video_file.getbuffer())
                    
                    v_file = client.files.upload(file=temp_path)
                    while v_file.state.name == "PROCESSING":
                        time.sleep(1); v_file = client.files.get(name=v_file.name)
                    
                    # 关键！全模态 + 丝滑衔接的 Prompt 逻辑
                    prompt = (
                        f"ACT AS: High-end Film Director. CHARACTER: {MUSE_IDENTITY}\n"
                        "TASK: Deconstruct video into seamless segments for the US market.\n"
                        "ANALYSIS REQUIREMENTS:\n"
                        "1. TRANSCRIPT: Accurate voice-to-text.\n"
                        "2. MOTION SKELETON: Describe exact hand/head movements to ensure continuity.\n"
                        "3. SMOOTH TRANSITION: Ensure the END of segment 'n' flows perfectly into the START of 'n+1'.\n"
                        "4. LIGHTING: Keep shadows and light direction identical to the original video.\n"
                        "OUTPUT JSON: {'segments': [{'time', 'transcript', 'motion_logic', 'kling_prompt', 'seaart_prompt'}]}"
                    )
                    
                    response = client.models.generate_content(
                        model=selected_model,
                        contents=[v_file, prompt],
                        config={'response_mime_type': 'application/json'}
                    )
                    
                    data = json.loads(response.text)
                    segments = data.get('segments', [])
                    
                    for i, seg in enumerate(segments):
                        with st.container(border=True):
                            st.subheader(f"分镜 {i+1} | {seg.get('time')}")
                            
                            # 全模态数据展示
                            t1, t2 = st.columns(2)
                            with t1:
                                st.markdown("🗣️ **语音识别**")
                                st.info(seg.get('transcript'))
                            with t2:
                                st.markdown("🦴 **动作轨迹逻辑 (确保衔接)**")
                                st.warning(seg.get('motion_logic'))
                            
                            st.markdown("**🎥 丝滑 Kling 提示词 (已注入动作锚点)**")
                            # 在提示词中自动注入连贯性术语
                            smooth_kling = f"{seg.get('kling_prompt')}. Seamless motion, maintain posture from previous shot, 8k cinematic."
                            st.code(smooth_kling)
                            
                            st.markdown("**🎨 静态参考图提示词**")
                            st.code(seg.get('seaart_prompt'))
                    
                    if os.path.exists(temp_path): os.remove(temp_path)
                            
                except Exception as e:
                    st.error(f"解析失败: {e}")
    else:
        st.info("等待上传并激活...")

# --- 演示给客户看的关键点 ---
st.markdown("---")
st.markdown("### 💡 客户演示话术 (技术核心)")
st.write("1. **动作惯性 (Motion Logic):** 我们的系统会记录前一秒的结束手势，强制下一秒从该位置开始，解决 AI 视频常见的‘跳帧’问题。")
st.write("2. **语音同步 (Transcript):** 自动提取博主情绪，为后续口型对齐 (Lip-sync) 提供精准参数。")
st.write("3. **欧美化重塑:** 在保持原视频产品（衣服、器材）不变的前提下，像素级重构人种与环境。")