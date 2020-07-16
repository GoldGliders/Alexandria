import React from "react"
import { initializeLiff } from "./liffInit"
import MultiButton from "./multibutton"
import liff from "@line/liff"

class LibraryTable extends React.Component{
  constructor(props){
    super(props)
    this.state = {
      timestamps: [],
      libraries: [],
      uri: this.props.uri,
      columnNames: this.props.columnNames,
      liffId: this.props.liffId,
      os: null,
      error: null,
      error_msg: null
    }
    this.getResource = this.getResource.bind(this)
    this.convertTimestamp = this.convertTimestamp.bind(this)
    this.row = this.row.bind(this)
  }

  componentDidMount(){
    initializeLiff(this.state.liffId, this.getResource)
  }

  getResource(resp){
    if (resp["status"] === "ok"){
      fetch(`/api/${this.state.uri}?idToken=${resp["idToken"]}`)
        .then(res => res.json())
        .then((res) => {
          const rows = res["items"].map(item => this.state.columnNames.map(key => item[key]))

          this.setState({
            timestamps: null,
            libraries: rows,
            os: resp["os"],
            error: false
          })
        })
        .catch((err) => {
          this.setState({
            timestamps: null,
            libraries: null,
            error: true,
            error_msg: err.message
          })
          liff.logout()
        })
    }else{
      this.setState({
        timestamps: null,
        libraries: null,
        error: true,
        error_msg: 503
      })
      liff.logout()
    }
  }


  convertTimestamp(colNum, cell){
    if (this.state.columnNames.indexOf("timestamp") === colNum){
      const converted = new Date(cell*1000).toLocaleDateString()
      return converted
    }else{
      return cell
    }
  }

  row(){
    const rows = this.state.libraries.map((library, rowNum) => (
      <tr key={rowNum}>
        {library.map((cell, colNum) => (
          <td key={colNum}>
            {this.convertTimestamp(colNum, cell)}
          </td>
        ))}
        <td key={library.length}>
          <MultiButton funcName="library" text="remove" formal={library[this.state.columnNames.indexOf("formal")]} libid={library[this.state.columnNames.indexOf("libid")]} idToken={liff.getIDToken()} />
        </td>
      </tr>
    ))

    return rows
  }

  render(){
    if (this.state.error){
      return(
        <div>
          <h1>{this.state.error_msg}</h1>
        </div>
      )
    }else{
      return(
        <div>
          <table>
            <thead>
              <tr>
                {this.state.columnNames.map((key, colNum) => <th key={colNum}>{key}</th>)}
              </tr>
            </thead>
            <tbody>
              {this.row()}
            </tbody>
          </table>
        </div>
      )
    }
  }
}

export default LibraryTable
