/** @odoo-module **/
//se hara uso de otras secciones para modificar las funcionalidades de los registros de tareas
import { registry } from '@web/core/registry';

const {Component, useState} = owl;
//creando el componente de owl
export  class owltodolist extends Component {
    //metodo constructor
    setup() {
        this.state=useState({value:1})
    }
}

//siguiendoo la estructura del modulo de conversacionnes (discuss) debemos declarar la plantilla
//todo_list.todolist apunta al template xml que se encuentra en la carpeta de views 
//pero para este caso crearemos una nmueva plantilla en la carpeta de static/src/xml, que copiaremos de discusscontrainier
owltodolist.template = 'owl.todolist';
registry.category('actions').add('owl.action_to_do_list_js', owltodolist);

//el nombre de la plantila la agragremos en t t-name del archivo xml

//debemos agregar el archivo en la vista principal xml todo_list.xml
