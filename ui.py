import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/predict"

def get_response(name, case_desc):
    response = requests.post(API_URL, json={
        "name": name,
        "case_description": case_desc
    })

    data = response.json()

    return f"""
### 👤 {data['user']}

### 📝 Category:
{data['category']}

### ⚖ IPC Sections:
{", ".join(data['ipc_sections'])}

### 📘 Summary:
{data['summary']}

### 👨‍⚖ Lawyer:
{data['recommended_lawyer']}
"""

def main():
    with gr.Blocks() as ui:
        gr.Markdown("# ⚖ AI Legal Case Predictor")

        name = gr.Textbox(label="Name")
        case = gr.Textbox(label="Case Description")

        output = gr.Markdown()
        btn = gr.Button("Analyze")

        btn.click(get_response, inputs=[name, case], outputs=output)

    ui.launch()

if __name__ == "__main__":
    main()
