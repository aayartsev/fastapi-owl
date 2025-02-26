import { Component, useState, useSubEnv } from "@odoo/owl";
import { Navbar } from "@webclient/navbar";
import { Todoo } from "@todoo/todoo";
import { TodoStore } from "@todoo/todo_store";

export class WebClient extends Component {
    static template = "oxp.WebClient";
    static components = { Navbar };
    setup() {
        this.apps = [
            { id: "todoo", name: "Todoo", Component: Todoo },
        ];
        this.state = useState({
            currentApp: this.apps[0],
        });
        const todoStore = useState(new TodoStore());
        // add store to environment
        useSubEnv({ todoStore });
    }
    selectApp(appId) {
        const newApp = this.apps.find((app) => app.id === appId);
        this.state.currentApp = newApp;
    }
}