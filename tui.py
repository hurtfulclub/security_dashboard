from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, ItemGrid, VerticalScroll, VerticalGroup,Vertical
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Static, Placeholder, Log, Input

from tui_functions import ping8888, trace8888, pinggoogle, pingcustom, tracecustom

class ScreenCustomPing(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Container(
                Horizontal(
                    Input("Address", classes="ipinput", id="ipaddr"),
                    classes="ipinput"
                ),
                Horizontal(
                    Button("Back", id="backbutton"),
                    Button("Ping", id="submitpingbutton"),
                    classes="centerbuttons"
                ),
                    id="custompingwindow"
            ),
            classes="maininput"
        )

class ScreenCustomTrace(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Container(
                Horizontal(
                    Input("Address", classes="ipinput", id="userip"),
                    classes="ipinput"
                ),
                Horizontal(
                    Button("Back", id="backbutton"),
                    Button("Trace", id="submitpingbutton"),
                    classes="centerbuttons"
                ),
                    id="custompingwindow"
            ),
            classes="maininput"
        )

class SecurityApp(App):

    def __init__(self, ip_info, **kwargs):
        super().__init__(**kwargs)
        self.ip_info = ip_info

    CSS_PATH = "tui.tcss"
    TITLE="Network Security"
    SUB_TITLE="v0.1"

    SCREENS = {
        "ping": ScreenCustomPing,
    }


    @work(thread=True)
    def run_ping(self, container):
        for line in ping8888():
            self.call_from_thread(self.add_log_line, line, container)

    @work(thread=True)
    def run_trace (self, container):
        for line in trace8888():
            self.call_from_thread(self.add_log_line, line, container)

    @work(thread=True)
    def run_google (self, container):
        for line in pinggoogle():
            self.call_from_thread(self.add_log_line, line, container)
    
    @work(thread=True)
    def run_customping(self, container, address):
        for line in pingcustom(address):
            self.call_from_thread(self.add_log_line, line, container)

    @work(thread=True)
    def run_customtrace(self, container, address):
        for line in tracecustom(address):
            self.call_from_thread(self.add_log_line, line, container)

    async def add_log_line(self, line, container):
        container.write(line+"\n")

    def compose(self) -> ComposeResult:

        self.container = VerticalScroll(id="interfaces")
        self.pingoutput = Log(id="terminaloutput")

        yield Header()
        yield Footer()
        yield Container(
            self.container,
            ItemGrid(
                Button("ping 8.8.8.8", classes="button_right", id="ping8"),
                Button("trace 8.8.8.8", classes="button_right", id="trace8"),
                Button("ping google", classes="button_right", id="pinggoogle"),
                Button("custom ping", classes="button_right", id="customping"),
                Button("custom trace", classes="button_right", id="customtrace"),
                id="buttongrid"
            ),
            id="topcontainer")

        yield Horizontal(
            self.pingoutput,
            id="bottomcontainer")

    @on(Button.Pressed, "#ping8")
    def ping8888(self):
        self.run_ping(self.pingoutput)

    @on(Button.Pressed, "#trace8")
    def trace8888(self):
        self.run_trace(self.pingoutput)

    @on(Button.Pressed, "#pinggoogle")
    def pinggoogle(self):
        self.run_google(self.pingoutput)

    @on(Button.Pressed, "#customping")
    def customping(self):
        self.push_screen(ScreenCustomPing())

    @on(Button.Pressed, "#customtrace")
    def customtrace(self):
        self.push_screen(ScreenCustomTrace())

    @on(Button.Pressed, "#backbutton")
    def back(self, event: Button.Pressed) -> None:
        self.pop_screen()

    @on(Button.Pressed, "#submitpingbutton")
    def pingaddress(self):
        input = self.app.screen.query_one("#ipaddr")
        self.pop_screen()
        self.run_customping(self.pingoutput, input.value)

    @on(Button.Pressed, "#submitpingbutton")
    def pingaddress(self):
        input = self.app.screen.query_one("#userip")
        self.pop_screen()
        self.run_customtrace(self.pingoutput, input.value)
        
    def on_mount(self):

        #adds inteface containers based on how many interfaces are present on device

        color_index = 1
        interfaces = self.ip_info
        
        for iface,ip in interfaces.items():
            if color_index == 1:
                color_id = "dark"
            else:
                color_id = "light"

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