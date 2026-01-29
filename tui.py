from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, ItemGrid, VerticalScroll,Vertical, VerticalGroup
from textual.widgets import Label, Button, TextArea, Header, Footer, Static, Placeholder

class SecurityApp(App):

    def __init__(self, ip_info, **kwargs):
        super().__init__(**kwargs)
        self.ip_info = ip_info

    CSS_PATH = "tui.tcss"
    TITLE="Network Security"
    SUB_TITLE="v0.1"

    def compose(self) -> ComposeResult:
        self.container = VerticalScroll(id="interfaces")
        #self.container = Placeholder("This is where the interfaces go",id="interfaces") 

        yield Header()
        yield Footer()
        yield Container(
            self.container,
            ItemGrid(
                Button("release ip & renew", classes="button_right"),
                Button("ping 8.8.8.8", classes="button_right"),
                Button("trace 8.8.8.8", classes="button_right"),
                Button("ping google", classes="button_right"),
                Button("custom ping", classes="button_right"),
                Button("custom trace", classes="button_right"),
                id="buttongrid"
            ),
            id="topcontainer")

        yield Horizontal(
            Placeholder("This is where net usage would be stores"),
            id="bottomcontainer")

    def on_mount(self):
        color_index = 1
        interfaces = self.ip_info

        print(self.ip_info)
        
        for iface,ip in interfaces.items():
            if color_index == 1:
                color_id = "red"
            else:
                color_id = "blue"

            self.container.mount(
                ItemGrid(
                    VerticalGroup(
                        Static(f"{iface}: {ip}"), classes="interface"
                    ),
                    classes = color_id 
                )
            )

            color_index *= -1

def runTUI(ip_info):
    app = SecurityApp(ip_info=ip_info)
    app.run()