import React from "react"
import {initializeLiff, get_bookmeta} from "./components/liffInit"

export default class BookTable extends React.Component{
  constructor(props){
    super(props)
    this.state = {
      timestamps: [],
      bookmetas: [],
      uri: this.props.uri,
      columnNames: this.props.columnNames,
      liffId: this.props.liffId,
      os: null,
      error: null,
      erro_msg: null
      //"1654371886-xorapzM6"
    }
  }

  componentDidMount(){
    const idToken = initializeLiff(this.state.liffId)
    if (idToken["status"] === "ok"){
      const resp = get_bookmeta(idToken, this.state.uri, this.state.columnNames)

      if (resp["status"] === "ok"){
        this.setState({
          timestamps: resp["timestamps"],
          bookmetas: resp["bookmetas"],
          os: resp["os"],
          error: false
        })
      }else{
        this.setState({
          os: resp["os"],
          error: true,
          error_msg: resp["status"]
        })
      }
    }else{
        this.setState({
          error: true,
          error_msg: "503"
        })
    }
  }


  row(){
    const cells = (
      this.state.bookmetas.map((cell, colNum) => (
        <td key={colNum}>
          {cell}
        </td>
      ))
    )

    this.state.bookmetas.map((bookmeta, rowNum) => {
      return (
        <tr key={rowNum}>
          <td key={rowNum}>
            {this.state.timestamps[rowNum]}
          </td>
          {cells}
        </tr>
          )
    })
  }



  render(){
    return(
      <div>
        <table>
          <thead>
            <tr>
              <th>timestamp</th>
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
