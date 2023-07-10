import { createApp } from 'vue'
import App from './App.vue'
import PrimeVue from 'primevue/config';
import axios from 'axios';

import "primevue/resources/themes/lara-light-indigo/theme.css"; //theme
import "primevue/resources/primevue.min.css";//core
import "primeicons/primeicons.css";//icons

import "primeflex/primeflex.css";

import DialogService from 'primevue/dialogservice';

import Menubar from 'primevue/menubar';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   // optional
import Row from 'primevue/row';                   // optional
import Card from 'primevue/card';
import Skeleton from 'primevue/skeleton';
import Divider from 'primevue/divider';
import Splitter from 'primevue/splitter';
import SplitterPanel from 'primevue/splitterpanel';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Checkbox from 'primevue/checkbox';
import Message from 'primevue/message';
import Avatar from 'primevue/avatar';
import AvatarGroup from 'primevue/avatargroup';   //Optional for grouping
import DataView from 'primevue/dataview';
import DataViewLayoutOptions from 'primevue/dataviewlayoutoptions'   // optional
import OverlayPanel from 'primevue/overlaypanel';
import TieredMenu from 'primevue/tieredmenu';
import DynamicDialog from 'primevue/dynamicdialog';
import Dialog from 'primevue/dialog';

const app = createApp(App)

app.use(PrimeVue);
app.use(DialogService);


app.component('Menubar',Menubar);
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('ColumnGroup', ColumnGroup)
app.component('Row', Row)
app.component('Card', Card)
app.component('Skeleton', Skeleton)
app.component('Divider', Divider)
app.component('Splitter', Splitter)
app.component('SplitterPanel', SplitterPanel)
app.component('Button', Button)
app.component('InputText', InputText)
app.component('Password', Password)
app.component('Checkbox', Checkbox)
app.component('Message', Message)
app.component('Avatar', Avatar)
app.component('AvatarGroup', AvatarGroup)
app.component('DataView', DataView)
app.component('DataViewLayoutOptions', DataViewLayoutOptions)
app.component('OverlayPanel', OverlayPanel)
app.component('TieredMenu', TieredMenu)
app.component('DynamicDialog', DynamicDialog)
app.component('Dialog', Dialog)

axios.defaults.baseURL = "https://6c1raj8mpb.execute-api.us-east-1.amazonaws.com/api" 

app.mount('#app')
