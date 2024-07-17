#!/usr/bin/env python

import sys
import gradio as gr
from travel_mapper.TravelMapper import TravelMapperForUI, load_secrets, assert_secrets
from travel_mapper.user_interface.capture_logs import PrintLogCapture
from travel_mapper.user_interface.utils import generate_generic_leafmap
from travel_mapper.user_interface.constants import EXAMPLE_QUERY


def read_logs():
    sys.stdout.flush()
    with open("output.log", "r") as f:
        return f.read()
# reads and returns the content of the "output.log" file.

def main():
    # The main function to launch the Application.
    secrets = load_secrets()
    assert_secrets(secrets)
    # Using the load_secrets() function, it loads API keys and uses assert_secrets() to confirm their existence.
    travel_mapper = TravelMapperForUI(
        openai_api_key=secrets["OPENAI_API_KEY"],
        google_maps_key=secrets["GOOGLE_MAPS_API_KEY"],
        google_palm_api_key=secrets["GOOGLE_PALM_API_KEY"],
    )
    sys.stdout = PrintLogCapture("output.log")

    # Using the help of Gradio as a template to build the UI.
    app = gr.Blocks()
    generic_map = generate_generic_leafmap()

    with app:
        gr.Markdown("## Team-16 Generates Personalised Travel Itineraries")
        with gr.Tabs():
            # Map View Tab
            with gr.TabItem("Map View"):
                with gr.Row():
                    with gr.Column():
                        text_input_map = gr.Textbox(EXAMPLE_QUERY, label="Travel Prompt:", lines=4)
                        radio_map = gr.Radio(value="gpt-3.5-turbo", choices=["gpt-3.5-turbo", "gpt-4", "models/text-bison-001"], label="models")
                        query_validation_text = gr.Textbox(label="Validation of Prompt:", lines=2)

                    with gr.Column():
                        map_output = gr.HTML(generic_map, label="Travel map")
                        itinerary_output = gr.Textbox(value="The Itinerary will be generated here", label="Itinerary", lines=3)
                map_button = gr.Button("Generate")

            # Non Map View Tab
            with gr.TabItem("Non-Map View"):
                with gr.Row():
                    with gr.Column():
                        text_input_no_map = gr.Textbox(value=EXAMPLE_QUERY, label="Travel Prompt:", lines=3)
                        radio_no_map = gr.Radio(value="gpt-3.5-turbo", choices=["gpt-3.5-turbo", "gpt-4", "models/text-bison-001"], label="Model choices")
                        query_validation_no_map = gr.Textbox(label="Validation of Prompt:", lines=2)

                    with gr.Column():
                        text_output_no_map = gr.Textbox(value="The Itinerary will be generated here", label="Itinerary:", lines=3)
                text_button = gr.Button("Generate")

        map_button.click(
            travel_mapper.generate_with_leafmap,
            inputs=[text_input_map, radio_map],
            outputs=[map_output, itinerary_output, query_validation_text],
        )
        # Input and Output commands for Map View and Non Map View Respectively.
        text_button.click(
            travel_mapper.generate_without_leafmap,
            inputs=[text_input_no_map, radio_no_map],
            outputs=[text_output_no_map, query_validation_no_map],
        )

    app.launch()


if __name__ == "__main__":
    main()
