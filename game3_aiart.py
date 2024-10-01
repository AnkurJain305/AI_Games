import streamlit as st
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

# Configuration settings
class CFG:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    seed = 42
    generator = torch.Generator(device).manual_seed(seed)
    image_gen_steps = 10
    image_gen_model_id = "stabilityai/stable-diffusion-2"
    image_gen_size = (256, 256)
    image_gen_guidance_scale = 9

# Load the model (cached in memory)
@st.cache_resource
def load_model():
    return StableDiffusionPipeline.from_pretrained(
        CFG.image_gen_model_id, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    ).to(CFG.device)

# Image generation function
def generate_image(prompt, model):
    image = model(
        prompt, num_inference_steps=CFG.image_gen_steps,
        generator=CFG.generator,
        guidance_scale=CFG.image_gen_guidance_scale
    ).images[0]
    
    image = image.resize(CFG.image_gen_size)
    return image

# AI Art Generator game function
def ai_art_generator_game():
    model = load_model()

    # User input for the text prompt
    prompt = st.text_input("Enter a prompt for AI-generated digital art (e.g., 'abstract fractal geometry', 'neon cyberpunk city'):")

    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating AI art..."):
                try:
                    # Generate the AI-based art using the Stable Diffusion model
                    image = generate_image(prompt, model)

                    # Display the generated image
                    st.image(image, caption="Generated AI Art", use_column_width=True)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a prompt!")
