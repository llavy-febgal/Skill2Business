import gradio as gr
from prompts import skill_to_business_prompt, follow_up_prompt

# Store last output for follow-up questions
history = {"last_response": ""}

def chatbot_response(skill, biz_type, solo_only):
    if skill.lower().startswith("tell me more about idea"):
        return follow_up_prompt(history["last_response"], skill)

    filters = {
        "biz_type": biz_type,
        "solo": solo_only,
    }

    try:
        result = skill_to_business_prompt(skill, filters)
        history["last_response"] = result
        return result
    except Exception as e:
        return f"Something went wrong: {e}"

with gr.Blocks() as demo:
    gr.Markdown("## 🎯 Skill2Business AI\n*Turn your skills into income streams.*")

    with gr.Row():
        skill_input = gr.Textbox(
            label="What's your skill?",
            placeholder="e.g. Knitting, Coding, Fitness, Music...",
        )
        filter_type = gr.Dropdown(
            label="Business Type",
            choices=["Any", "Online", "Offline", "Hybrid"],
            value="Any"
        )
        solo_only = gr.Checkbox(label="Solo-friendly only", value=False)

    submit_btn = gr.Button("Generate Ideas")
    output = gr.Textbox(label="💡 Monetization Ideas", lines=20, show_copy_button=True)

    submit_btn.click(fn=chatbot_response, inputs=[skill_input, filter_type, solo_only], outputs=output)

demo.launch()
