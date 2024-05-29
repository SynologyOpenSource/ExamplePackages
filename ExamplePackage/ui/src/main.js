import Vue from 'vue';
import App from './App.vue';
import './styles/index.css';

SYNO.namespace('SYNO.SDS.App.ExamplePackage');

SYNO.SDS.App.ExamplePackage.Instance = Vue.extend({
    components: { App },
    template: '<App/>',
});
