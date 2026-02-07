import json
import os
from typing import TypedDict, Optional, Dict, Any
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY")

llm = ChatOpenAI(
    model="qwen-plus",
    openai_api_key=api_key,
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.1
)


class AgentState(TypedDict):
    query: str
    history: Optional[Dict[str, Any]]
    schema: dict


def generator_node(state: AgentState):
    query = state['query']
    history = state.get('history')

    base_system_prompt = """
    You are a Generative UI Engine. Output Formily JSON Schema.

    ### CRITICAL RULES (MUST FOLLOW)
    1. **ALWAYS** add `"type": "void"` to EVERY component object.
    2. **BUTTON TEXT**: Use `"x-content": "Text"` (NOT children).
    3. **CONTRAST**: Light buttons (Gold/White) MUST have `"style": { "color": "#000" }`.
    4. **Output**: Return ONLY the valid JSON.

    ### ATOMIC COMPONENTS (Layout & Basic UI)
    - **Box**: { padding, background, border, radius, shadow, width }
    - **Stack**: { direction, gap, align, justify }
    - **Typography**: { content, variant, color, bold }
    - **Motion**: { type, delay }
    - **Clock**: { format }
    - **AntD**: Button, Alert, Tag, Progress, Rate

    ### 🚀 SPECIAL COMPONENT: "Embed" (Universal Code Container)
    Use this component when the user wants **Games**, **Charts**, **Calculators**, **Visualizations**, or **Interactive Apps**.

    - **Embed Props**: 
      - `code`: string (The COMPLETE, STANDALONE HTML+CSS+JS code).
      - `width`: string (e.g., "100%").
      - `height`: string (e.g., "500px").

    - **👨‍💻 CODING GUIDELINES FOR 'code' PROP (Strict)**:
      1. **STANDALONE**: The code runs in an iframe. Include `<!DOCTYPE html><html><style>...</style><body>...</body><script>...</script></html>`.
      2. **NO EXTERNAL DEPS**: Do not rely on external images or CDNs unless absolutely necessary. Use CSS/Canvas for graphics.
      3. **FORMATTING**:
         - **Use `\\n` for newlines** to make code readable. DO NOT compress into one line.
         - **Use SINGLE QUOTES `'`** inside HTML/JS as much as possible to avoid escaping issues with the JSON double quotes `"` wrapper.
      4. **NO COMMENTS**: **ABSOLUTELY NO `//` comments**. They break the code when parsed as a JSON string. Use `/* ... */` blocks if you really need to comment.
      5. **ROBUSTNESS**:
         - Initialize all variables.
         - For Games: Implement a proper `requestAnimationFrame` loop.
         - For Interactions: Add event listeners (keydown, click) to `document` or `canvas`.
         - Handle "Game Over" or "Reset" states logically.

    ### EXAMPLE: General App Structure (Embed)
    {
      "type": "void",
      "x-component": "Box",
      "x-component-props": { "background": "#1a1a1a", "padding": 20, "radius": 16 },
      "properties": {
        "appTitle": {
          "type": "void",
          "x-component": "Typography",
          "x-component-props": { "content": "Interactive App", "variant": "h2", "color": "#fff" }
        },
        "appContainer": {
          "type": "void",
          "x-component": "Embed",
          "x-component-props": {
            "height": "400px",
            "code": "<!DOCTYPE html>\\n<html>\\n<head>\\n<style>\\n  body { margin: 0; display: flex; justify-content: center; align-items: center; background: #000; color: #fff; font-family: sans-serif; }\\n  canvas { border: 1px solid #333; }\\n</style>\\n</head>\\n<body>\\n  <canvas id='c' width='300' height='300'></canvas>\\n  <script>\\n    /* Initialize */\\n    const c = document.getElementById('c');\\n    const ctx = c.getContext('2d');\\n    /* Main Loop */\\n    function loop() {\\n      requestAnimationFrame(loop);\\n      // ... logic ...\\n    }\\n    loop();\\n  </script>\\n</body>\\n</html>"
          }
        }
      }
    }
    """

    if history:
        print("--- Mode: Modification ---")
        system_prompt = base_system_prompt + """
        \n\n### TASK: MODIFY UI
        The user wants to modify an existing UI.
        1. Analyze the Current JSON and User Feedback.
        2. Output a **NEW, COMPLETE** JSON Schema that incorporates the changes.
        3. Keep the parts that don't need changing.
        """
        user_prompt = f"""
        Current JSON:
        ```json
        {json.dumps(history, ensure_ascii=False)}
        ```

        User Feedback: "{query}"

        Generate the Updated JSON:
        """
    else:
        print("--- Mode: Creation ---")
        system_prompt = base_system_prompt + "\n\n### TASK: CREATE NEW UI"
        user_prompt = f"Generate UI for: {query}"

    messages = [
        ("system", system_prompt),
        ("human", user_prompt)
    ]

    try:
        response = llm.invoke(messages)
        clean_content = response.content.replace("```json", "").replace("```", "").strip()
        final_schema = json.loads(clean_content)
        if "schema" in final_schema and "type" not in final_schema:
            final_schema = final_schema["schema"]

    except Exception as e:
        print(f"LLM Error: {e}")
        final_schema = {
            "type": "void",
            "x-component": "Typography",
            "x-component-props": {"content": "生成出错，请重试"}
        }

    return {"schema": final_schema}

workflow = StateGraph(AgentState)
workflow.add_node("generator", generator_node)
workflow.set_entry_point("generator")
workflow.add_edge("generator", END)
app_graph = workflow.compile()