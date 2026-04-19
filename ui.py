import gradio as gr
# ------------------------------ 
# GRADIO UI 
# ------------------------------ 
def main(): 
  with gr.Blocks(theme=gr.themes.Soft()) as ui: 
    gr.Markdown("<h1 style='text-align:center;'>🏛 LawBot India — IPC Prediction & Legal Guidance</h1>") 
    
    with gr.Column() as input_col: 
      name = gr.Textbox(label="Your Name") 
      case_desc = gr.Textbox(label="Case Description", lines=5) 
      submit = gr.Button("Analyze Case", variant="primary") 
      
    with gr.Column(visible=False) as output_col: 
      result_md = gr.Markdown() 
      clear_btn = gr.Button("Clear") 
      
    def on_submit(n, c): 
      answer = chatbot_response(n, c) 
      return ( gr.update(visible=False), # hide input 
              gr.update(visible=True), # show output 
              gr.update(value=answer) # fill markdown 
             ) 
    def on_clear(): 
      return ( gr.update(visible=True), 
              gr.update(visible=False), 
              "", 
              "" ) 
    submit.click(on_submit, inputs=[name, case_desc], outputs=[input_col, output_col, result_md]) 
    clear_btn.click(on_clear, outputs=[input_col, output_col, name, case_desc]) 
    
    ui.launch()
