import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import BookTable from './components/booktable';
import LibraryTable from './components/librarytable';
import OptionTable from './components/optiontable';
import Endpoint from './components/endpoint';
import LibrarySelect from './components/area_oriented_library';
import { BrowserRouter, Route } from 'react-router-dom';
import * as serviceWorker from './serviceWorker';
import Container from "@material-ui/core/Container"

const liffId = process.env.REACT_APP_liffId
const api_url = "https://api.alexandria-app.tk"

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <Container>
        <Route exact path="/" render={() => <Endpoint liffId={liffId}/> }/>
        <Route exact path="/history" render={() => <BookTable uri={"history"} columnNames={["title", "author", "isbn"] } liffId={liffId} api_url={api_url}/> }/>
        <Route exact path="/bookmark" render={() => <BookTable uri={"bookmark"} columnNames={["title", "author", "isbn"] } liffId={liffId} api_url={api_url}/> }/>
        <Route exact path="/library" render={() => <LibraryTable uri={"library"} columnNames={["timestamp", "formal", "libid", "systemid"] } liffId={liffId} api_url={api_url}/> }/>
        <Route exact path="/onelibrary" render={() => <LibrarySelect liffId={liffId} api_url={api_url}/> }/>
        <Route exact path="/option" render={() => <OptionTable liffId={liffId} api_url={api_url}/> }/>
      </Container>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
