import reflex as rx
from typing import List, Dict, Any
import requests

class State(rx.State):
    data: List[Dict[str, Any]] = []
    data_fetched: bool = False
    
    def fetch_cat_data(self):
        try:
            cat_data = requests.get("https://cat-fact.herokuapp.com/facts/")
            cat_data.raise_for_status()
            self.data = cat_data.json()
            self.data_fetched = True
        except requests.RequestException as e:
            print(f"An error occured: {e}")
            self.data = []
            self.data_fetched = False

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.box(
        rx.heading("Hello World!", size="7"),
        rx.link(
            rx.button("Fetch data...", cursor="pointer"),
            href="/cat-fact/facts",
            is_external=False,
        ),
        spacing="5",
        justify="center",
        min_height="100vh",
        width="100%",
        padding="1em",
    )
    
def cat_facts() -> rx.Component:
    # Render the data dynamically
    def render_fact(fact: Dict[str, Any]):
        return rx.table.row(
            rx.table.cell(fact["text"]),
            rx.table.cell(str(fact["status"])),
            rx.table.cell(fact["createdAt"]),
            align="center",
        )
    # Display data         
    return rx.flex(
        rx.heading("Cat Facts"),
        rx.flex(
            rx.text("Search query:"),
            rx.input(),
            rx.button("Search", cursor="pointer"),
            justify="end",
            spacing="2",
        ),
        rx.cond(
            State.data, 
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Fact"),
                        rx.table.column_header_cell("Verified"),
                        rx.table.column_header_cell("Created On"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(State.data, render_fact)
                )
            ), 
            rx.text("Loading...")
        ),
        direction="column",
        spacing="5",
        padding="1em"
    )


app = rx.App()
app.add_page(index)
app.add_page(cat_facts, route="/cat-fact/facts")
