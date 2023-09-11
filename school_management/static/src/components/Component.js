/* @odoo-module */
import { registry } from "@web/core/registry";

const { Component, useState, xml} = owl;
console.log('MY Module');
class A extends Component {
    setup() {
        this.state = useState({ Hello: 'Hello Everyone' });
    }
}

A.template = 'school_management.A';

class B extends Component {
  
    static template = xml`<span><h4>Hello Odoo</h4></span>`;
}

class Form extends Component {
    static template = "Form";
  
    setup() {
      this.state = useState({
        text: "",
        othertext: "",
        number: "",
        color: "",
        bool: false
      });
    }
  }

class Hi extends Component {
    static template = "Hi";
    
    setup() {
        this.state = useState({ word: 'Hello'});
    }

    toggle() {
        this.state.word === 'Hi' ? 'Hello' : 'Hi';
    }
}

class Task extends Component {
    static template = "Task";

    
    static props = ["task"]

    toggleTask(){
        this.props.task.isCompleted = !this.props.task.isCompleted
    }
}

class Root extends Component {
    static template = "Root";
    

    static components = (Task)

    setup() {
        this.state = useState({
            name: "",
            color: "#OOFF00",
            isCompleted: false,
        });

        this.Task = useState([])
    }

    addTask() {
        if (!this.state.name){
            alert("Please provide name of the task.")
            return
        }

        const id = Math.random().toString().substring(2,12)


        this.Task.push({
            id:id,
            name:this.state.name,
            color:this.state.color,
            isCompleted: false,
        })

        let state = this.state
        this.state = {...state, name:"", color:"#fff000"}

        console.log(this.Task)
    }
}


class Parent extends Component {
    static template = 'Parent';
    static components = { A, B, Form, Hi, Task, Root }
    state = useState({ form_render:""});
    
    get myComponent() {
        if (this.state.form_render === "a") {
            return A;
        }
        else if(this.state.form_render === "b") {
            return B;
        }
        else if(this.state.form_render === "form") {
            return Form;
        }
        else if(this.state.form_render === "root") {
            return Root;
        }
        else{
            return Hi;
        }
    }
}

registry.category('actions').add('component_client_action', Parent);