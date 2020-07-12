import React from "react"
import { initializeLiff } from "./liffInit"

class BookTable extends React.Component{
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
    }
    this.getResource = this.getResource.bind(this)
    this.row = this.row.bind(this)
  }

  componentDidMount(){
    const idToken = initializeLiff(this.state.liffId, this.getResource)
  }

  getResource(resp){
    if (resp["status"] === "ok"){
      fetch(`/api/${this.state.uri}?idToken=${resp["idToken"]}`)
        .then(res => res.json())
        .then((res) => {
          const timestamps = res["items"].map(x => new Date(x["timestamp"]*1000).toLocaleDateString())
          const rows = res["items"].map(item => this.state.columnNames.map(key => item["bookmeta"][key]))

          this.setState({
            timestamps: timestamps.reverse(),
            bookmetas: rows.reverse(),
            os: resp["os"],
            error: false
          })
        })
        .catch((err) => {
          this.setState({
            timestamps: null,
            bookmetas: null,
            error: true,
            error_msg: err.message
          })
          liff.logout()
        })
    }else{
      this.setState({
        timestamps: null,
        bookmetas: null,
        error: true,
        error_msg: 503
      })
      liff.logout()
    }
  }


  row(){
    const rows = this.state.bookmetas.map((bookmeta, rowNum) => (
      <tr key={rowNum}>
        <td key={0}>
          {this.state.timestamps[rowNum]}
        </td>
        {bookmeta.map((cell, colNum) => (
          <td key={colNum+1}>
            {cell}
          </td>
        ))}
      </tr>
    ))

    return rows
  }



  render(){
    console.log(this.state)
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

export default BookTable
