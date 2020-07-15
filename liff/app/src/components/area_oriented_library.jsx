import React from "react"
import { initializeLiff } from "./liffInit"
import liff from "@line/liff"

class LibrarySelect extends React.Component{
  constructor(props){
    super(props)
    this.state = {
      liffId: this.props.liffId,
      scopeField: ["北海道","東北","関東","中部","近畿", "中国", "四国","九州・沖縄"],
      selectedField: "地域",
      selectedArea: null,
      selectedPref: null,
      selectedCity: null,
      selectedLibrary: null,
      libraryColumns: ["systemname", "libkey", "libid"],
      url: "/api/onelibrary",
      level: 0,
      error: false,
      error_msg: null
    }
    this.getScope = this.getScope.bind(this)
    this.putLibrary = this.putLibrary.bind(this)
    this.scopeButton = this.scopeButton.bind(this)
    this.libraryTable = this.libraryTable.bind(this)
    this.scopeTable = this.scopeTable.bind(this)
  }

  componentDidMount(){
    initializeLiff(this.state.liffId, ()=>{})
  }

  getScope(fieldValue, url, level){
    level = level + 1
    let fieldName = ""
    switch (level){
      case 1:
        fieldName = "?area"
        break

      case 2:
        fieldName = "&pref"
        break

      case 3:
        fieldName = "&city"
        break

      case 4:
        fieldName = "&library"
        break
    }

    url = url + `${fieldName}=${fieldValue}`
    fetch(`${url}&level=${level}`)
      .then(res => res.json())
      .then((res) => {
        let response = {}
        let field = ""
        switch (level){
          case 1:
            response = {selectedArea: fieldValue}
            break

          case 2:
            response = {selectedPref: fieldValue}
            break

          case 3:
            response = {selectedCity: fieldValue}
            break

          case 4:
            response = {selectedLibrary: fieldValue}
            break
        }

        this.setState(
          Object.assign(
            response,
            {scopeField: res["items"], selectedField: fieldValue, url: url, level: level, error: false}
          )
        )
      })
      .catch((err) => {
        liff.logout()
        this.setState({error: true, error_msg: err.message})
      })
  }

  putLibrary(libid, idToken){
    console.log(libid, idToken)
    fetch("/api/library", {
      method: "PUT",
      body: JSON.stringify({
        libid: libid,
        idToken: idToken
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })
      .then(res => res.json())
      .then((res) => {
        console.log(res)
        this.setState({selectedLibrary: libid})
      })
      .catch((err) => {
        this.setState({
          error: true,
          error_msg: err.message
        })
        liff.logout()
      })
  }

  scopeButton(){
    const table = this.state.scopeField.map((fieldValue, num) => (
      <tr key={num}>
        <td>
          <button onClick={() => {
            this.getScope(fieldValue, this.state.url, this.state.level)
          }}>
            {fieldValue}
          </button>
        </td>
      </tr>
    )
    )
    return table
  }


  libraryTable = () => {
    return (<div>
      <table>
        <thead>
          <tr>
            {this.state.libraryColumns.map((col, num)=> (<th key={num}>{col}</th>))}
          </tr>
        </thead>
        <tbody>
          {this.state.scopeField.map((fieldValue, rownum) => (
            <tr key={rownum}>
              {this.state.libraryColumns.map((col, colnum) => (<td key={colnum}>{fieldValue[col]}</td>))}
              <td>
                <button onClick={() => {
                  this.putLibrary(fieldValue["libid"], liff.getIDToken())
                }}>
                  select
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>)
  }

  scopeTable = () => {
    return (<div>
      <table>
        <thead>
          <tr>
            <th>{this.state.selectedField}</th>
          </tr>
        </thead>
        <tbody>
          {this.scopeButton()}
        </tbody>
      </table>
    </div>)
  }

  render(){
    if (this.state.error){
      return(
        <div>
          <h1>{this.state.error_msg}</h1>
        </div>
      )
    }else if (this.state.level == 3){
      return this.libraryTable()
    }else{
      return this.scopeTable()
    }
  }
}

export default LibrarySelect
