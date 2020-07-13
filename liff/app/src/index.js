import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App'
import BookTable from './components/booktable';
import LibraryTable from './components/librarytable';
import Endpoint from './components/endpoint';
import { BrowserRouter, Route } from 'react-router-dom';
import * as serviceWorker from './serviceWorker';

const liffId = "1654371886-xorapzM6"
ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <Route exact path="/" render={() => <App /> }/>
      <Route exact path="/liff/" render={() => <Endpoint liffId={liffId}/> }/>
      <Route exact path="/liff/history" render={() => <BookTable uri={"history"} columnNames={["title", "author", "isbn"] } liffId={liffId}/> }/>
      <Route exact path="/liff/bookmark" render={() => <BookTable uri={"bookmark"} columnNames={["title", "author", "isbn"] } liffId={liffId}/> }/>
      <Route exact path="/liff/library" render={() => <LibraryTable uri={"library"} columnNames={["timestamp", "formal", "libid", "systemid"] } liffId={liffId}/> }/>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
