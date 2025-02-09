from atproto import Client, models
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Input, Label, Header, Footer, Static
from textual.screen import Screen
from textual.binding import Binding

from helpers import create_client
from add import add_users_to_list, add_followers_to_list
from remove import remove_users_from_list, remove_followers_from_list


class User:
    def __init__(self, client):
        self.client = client


class LoginScreen(Screen):
    BINDINGS = [
        Binding("escape", "quit", "quit", show=True),
        Binding("enter", "submit", "login", show=True)
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Label("username:"),
            Input(id="username", placeholder="Enter username"),
            Label("password:"),
            Input(id="password", password=True, placeholder="Enter password"),
        )
        yield Button("login", variant="primary", id="login-button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "login-button":
            self.action_submit()

    def action_submit(self) -> None:
        username = self.query_one("#username").value
        password = self.query_one("#password").value
        if username and password:
            # Here you would call your login function
            # if login_successful:
            self.app.client = create_client(username, password)
            self.app.push_screen(MainScreen())
        else:
            # Show error message
            pass


class MainScreen(Screen):
    BINDINGS = [
        Binding("escape", "quit", "quit", show=True),
        Binding("ctrl+b", "back", "back to login", show=True)
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Label("list spam !", classes="title"),
            Horizontal(
                Container(
                    Label("add users:"),
                    Input(id="add-users", placeholder="user1,user2,user3"),
                    Label("list uri:"),
                    Input(
                        id="list-uri", placeholder="https://bsky.app/profile/user1.bsky.social/lists/list1"),
                    Button("add users", variant="primary", id="add-users-btn"),
                ),
                Container(
                    Label("remove users:"),
                    Input(id="remove-users", placeholder="user1,user2,user3"),
                    Label("list uri:"),
                    Input(
                        id="list-uri", placeholder="https://bsky.app/profile/user1.bsky.social/lists/list1"),
                    Button("remove users", variant="primary",
                           id="remove-users-btn"),
                ),
            ),
            Horizontal(
                Container(
                    Label("add followers of users:"),
                    Input(id="add-followers",
                          placeholder="target_user1,target_user2,target_user3"),
                    Label("list uri:"),
                    Input(
                        id="list-uri", placeholder="https://bsky.app/profile/user1.bsky.social/lists/list1"),
                    Button("add followers", variant="primary",
                           id="add-followers-btn"),
                ),
                Container(
                    Label("remove followers of users:"),
                    Input(id="remove-followers",
                          placeholder="target_user1,target_user2,target_user3"),
                    Label("list uri:"),
                    Input(
                        id="list-uri", placeholder="https://bsky.app/profile/user1.bsky.social/lists/list1"),
                    Button("remove followers", variant="primary",
                           id="remove-followers-btn"),
                ),
            ),
            Static(id="status-message"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        status = self.query_one("#status-message")

        if event.button.id == "add-users-btn":
            users = self.query_one("#add-users").value
            list_uri = self.query_one("#list-uri").value
            if users:
                status.update(f"adding users: {users}")
                add_users_to_list(self.app.client, users.split(','), list_uri)
                status.update(f"added users: {users}")
        elif event.button.id == "remove-users-btn":
            users = self.query_one("#remove-users").value
            list_uri = self.query_one("#list-uri").value
            if users:
                status.update(f"removing users: {users}")
                remove_users_from_list(
                    self.app.client, users.split(','), list_uri)
                status.update(f"removed users: {users}")
        elif event.button.id == "add-followers-btn":
            users = self.query_one("#add-followers").value
            list_uri = self.query_one("#list-uri").value
            if users:
                status.update(f"adding followers of: {users}")
                add_followers_to_list(
                    self.app.client, users.split(','), list_uri)
                status.update(f"added followers of: {users}")
        elif event.button.id == "remove-followers-btn":
            users = self.query_one("#remove-followers").value
            list_uri = self.query_one("#list-uri").value
            if users:
                status.update(f"removing followers of: {users}")
                remove_followers_from_list(
                    self.app.client, users.split(','), list_uri)
                status.update(f"removed followers of: {users}")

    def action_back(self) -> None:
        self.app.pop_screen()


class listfluff(App):
    CSS = """
    Screen {
        align: center middle;
    }

    .title {
        text-align: center;
        margin: 1 0;
        text-style: bold;
    }
    
    .label-bold {
        text-style: bold;
    }

    #login-container {
        width: 60;
        height: auto;
        border: solid green;
        padding: 1 2;
    }

    Container {
        height: auto;
        margin: 1 1;
        padding: 1 1;
    }

    Button {
        margin: 1 0;
        width: 100%;
    }

    #status-message {
        height: 3;
        content-align: center middle;
        text-style: bold;
        color: blue;
    }
    """

    def __init__(self):
        super().__init__()
        self.client = None

    def on_mount(self) -> None:
        self.theme = "tokyo-night"
        self.push_screen(LoginScreen())


if __name__ == "__main__":
    app = listfluff()
    app.run()
