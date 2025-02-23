import { Component } from "@odoo/owl";
import { TodoList } from "@todoo/todo_list";
import { useTodoStore } from "@todoo/todo_store";
import { Layout } from "@layout";

export class Todoo extends Component {
    static template = "oxp.Todoo";
    static components = { TodoList, Layout };

    setup() {
        this.nextId = 1;
        this.store = useTodoStore();
    }

    addNewList() {
        const id = this.nextId++;
        this.store.createList();
    }
}